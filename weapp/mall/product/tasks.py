# -*- coding: utf-8 -*-

from core.exceptionutil import unicode_full_stack
from django.conf import settings
from watchdog.utils import watchdog_error
import json
from celery import task
from core import upyun_util
from modules.member.models import Member
from mall import models
from . import utils
from datetime import datetime
from export_job.models import ExportJob
import os
import xlsxwriter

@task(bing=True)
def update_sync_product_status(product, request, is_group=False):
    is_update = None
    update_data = []
    # 规格
    standard_model, custom_models = utils.extract_product_model(request)
    swipe_images = json.loads(request.POST.get('swipe_images', '[]'))
    if len(custom_models) > 0:
        utils.delete_weizoom_mall_sync_product(request, product, utils.MALL_PRODUCT_HAS_MORE_MODEL)
        return
    # 属性
    product_standard_model = models.ProductModel.objects.filter(product_id=product.id, name='standard')[0]
    properties = request.POST.get('properties')
    properties = json.loads(properties) if properties else []
    property_ids = set([property['id'] for property in properties])
    existed_property_ids = set([
        property.id for property in models.ProductProperty.objects.filter(
            product_id=product.id)
        ])

    if product.name != request.POST.get('name', '').strip():
        is_update = True
        update_data.append(u'商品名称')
    if product.promotion_title != request.POST.get('promotion_title', '').strip():
        is_update = True
        update_data.append(u'促销标题')
    min_limit = request.POST.get('min_limit', '0').strip()
    if not min_limit.isdigit():
        min_limit = 0
    if product.min_limit != int(min_limit):
        is_update = True
        update_data.append(u'起购数量')
    if product.bar_code != request.POST.get('bar_code', '').strip():
        is_update = True
        update_data.append(u'商品条码')
    if product.detail != request.POST.get('detail', '').strip():
        is_update = True
        update_data.append(u'商品详情')
    if product_standard_model.price != float(standard_model['price']):
        is_update = True
        update_data.append(u'商品价格')
    if product_standard_model.weight != float(standard_model['weight']):
        is_update = True
        update_data.append(u'商品重量')
    if product_standard_model.user_code != standard_model['user_code']:
        is_update = True
        update_data.append(u'商品编码')
    if property_ids != existed_property_ids:
        is_update = True
        update_data.append(u'商品属性')
    if set([image['url'] for image in product.swipe_images]) != set([image['url'] for image in swipe_images]):
        is_update = True
        update_data.append(u'商品图片')

    if is_update:
        utils.update_weizoom_mall_sync_product_status(request, product, update_data)


@task(bind=True, time_limit=7200, max_retries=2)
def send_review_export_job_task(self, exportjob_id, filter_data_args, sort_attr, type):

    export_jobs = ExportJob.objects.filter(id=exportjob_id)

    if type == 2:
        filename = "product_review_{}.xlsx".format(exportjob_id)
        dir_path_excel = "excel"
        dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_excel)
        file_path = "{}/{}".format(dir_path,filename)
        workbook   = xlsxwriter.Workbook(file_path)
        table = workbook.add_worksheet()
        try:
            product_name = ''
            product_user_code = ''
            if filter_data_args.has_key("product_name"):
                product_name = filter_data_args.pop("product_name")
            if filter_data_args.has_key("product_user_code"):
                product_user_code = filter_data_args.pop("product_user_code")
            product_reviews = models.ProductReview.objects.filter(**filter_data_args).order_by("-created_at")
            if product_name:
                product_reviews = product_reviews.filter(order_has_product__product__name__contains=product_name)
            if product_user_code:
                product_review_list = []
                for product_review in product_reviews:
                    product_model = models.ProductModel.objects.filter(name=product_review.order_has_product.product_model_name,product_id=product_review.product_id)[0]
                    if product_user_code == product_model.user_code:
                        product_review_list.append(product_review)
                product_reviews = product_review_list
            reviews_info = [u'用户ID', u'用户名',u'商品名称',u'订单号',
                 u'姓名',u'电话',u'评价时间',u'状态',u'产品评星',u'评价内容',u'图片链接']
            for i in range(len(reviews_info)):
                table.write(0, i, reviews_info[i])
            try:
                review_count = product_reviews.count()
            except:
                review_count = len(product_reviews)
            export_jobs.update(count=review_count)
            review_count_write = 0
            for product_review in product_reviews:
                member_id = product_review.member_id
                try:
                   member = Member.objects.filter(id=member_id)[0]
                except:
                    continue
                nike_name = member.username
                try:
                    nike_name = nike_name.decode('utf8')
                except:
                    nike_name = member.username_hexstr
                product = models.Product.objects.filter(id=product_review.product_id)[0]
                product_name = product.name
                # order_id = product_review.order_id
                order = models.Order.objects.filter(id=product_review.order_id)[0]
                order_id = order.order_id
                ship_name = order.ship_name
                ship_tel = order.ship_tel
                created_at = product_review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                status = models.PRODUCT_REVIEW_STATUS[int(product_review.status)+1][1]
                product_score = product_review.product_score
                review_detail = product_review.review_detail
                pic_links = []
                product_review_pictures = models.ProductReviewPicture.objects.filter(product_review=product_review)
                for product_review_picture in product_review_pictures:
                    pic_links.append(product_review_picture.att_url)

                product_review_list = [ member_id,
                                nike_name,
                                product_name,
                                order_id,
                                ship_name,
                                ship_tel,
                                created_at,
                                status,
                                product_score,
                                review_detail,
                            ]
                product_review_list.extend(pic_links)
                review_count_write += 1
                for i in range(len(product_review_list)):
                    table.write(review_count_write, i, product_review_list[i])

                export_jobs.update(processed_count=review_count_write,update_at=datetime.now())
            workbook.close()
            upyun_path = '/upload/excel/{}'.format(filename)
            yun_url = upyun_util.upload_image_to_upyun(file_path, upyun_path)
            export_jobs.update(status=1,file_path=yun_url,update_at=datetime.now())

        except:
            notify_message = "导出商品评论任务失败,response:{}".format(unicode_full_stack())
            export_jobs.update(status=2,is_download=1)
            watchdog_error(notify_message)

