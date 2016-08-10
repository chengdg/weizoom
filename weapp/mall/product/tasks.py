# -*- coding: utf-8 -*-

from core.exceptionutil import unicode_full_stack
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
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

@task(bind=True, time_limit=7200, max_retries=2)
def send_product_export_job_task(self, exportjob_id, filter_data_args, type):
    export_jobs = ExportJob.objects.filter(id=exportjob_id)
    
    filename = "product_{}.xlsx".format(exportjob_id)
    dir_path_excel = "excel"
    dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_excel)
    file_path = "{}/{}".format(dir_path,filename)
    workbook   = xlsxwriter.Workbook(file_path)
    table = workbook.add_worksheet()
    try:
        mall_type = int(filter_data_args['mall_type'])
        if mall_type:
            head_format=workbook.add_format()
            # head_format.set_bold() # 设置粗体字
            head_format.set_font_color('white')
            head_format.set_bg_color('#5A9BD5') # 背景颜色
            head_list = [u'商品ID', u'商品编号', u'供货商', u'商品名称', u'商品规格名称', u'商品价格', u'商品最低价格', u'采购价', u'商品毛利', u'商品最低毛利', u'扣点类型', 
            u'规格库存', u'最低库存', u'总库存', u'分组', u'总销量', u'总销售额', u'上架时间']
            table.write_row('A1' , head_list, head_format)
            tmp_line = 1

            cell_format=workbook.add_format()
            cell_format.set_align('vcenter') #垂直居中

            if type == 4:
                owner = User.objects.get(id=filter_data_args['woid'])
                products = models.Product.objects.belong_to(mall_type, owner, models.PRODUCT_SHELVE_TYPE_ON)
                
                # product_id2onshelvetime = for product_id_sync_at in product_id_sync_ats
                models.Product.fill_details(owner, products, {
                    "with_product_model": True,
                    "with_model_property_info": True,
                    "with_selected_category": True,
                    'with_image': False,
                    'with_property': True,
                    'with_sales': True
                })
                products = utils.filter_products(None, products, filter_data_args)

                product_ids = [product.id for product in products]
                product_id2onshelvetime = dict(models.ProductPool.objects.filter(product_id__in=product_ids).values_list('product_id', 'sync_at'))

                product_count = len(product_ids)
                export_jobs.update(count=product_count)
                processed_count = 0 
                for product in products:
                    processed_count += 1
                    export_jobs.update(processed_count=processed_count, update_at=datetime.now())
                    product_sales = models.OrderHasProduct.objects.filter(product_id=product.id, promotion_id=0, order__status=models.ORDER_STATUS_SUCCESSED, order__origin_order_id__lte=0).aggregate(Sum('number'))['number__sum']
                    product_sales_money = models.OrderHasProduct.objects.filter(product_id=product.id, promotion_id=0, order__status=models.ORDER_STATUS_SUCCESSED, order__origin_order_id__lte=0).aggregate(Sum('total_price'))['total_price__sum']
                    if not product_sales:
                        product_sales = 0
                    if not product_sales_money:
                        product_sales_money = 0
                    onshelvetime = product_id2onshelvetime.get(product.id, '')
                    #供货商提前取

                    try:
                        if product.supplier:
                            supplier = Supplier.objects.get(id=product.supplier)
                            supplier_name = supplier.name
                            supplier_name_export = u'自[{}]'.format(supplier_name)
                        else:
                            supplier_store = UserProfile.objects.get(user_id=product.supplier_user_id)
                            supplier_name_export = u'同[{}]'.format(supplier_store.store_name)
                    except:
                        supplier_name_export = ''
                    point_type = '' #扣点类型先为空

                    categories = []
                    if product.categories:
                        for product_category in product.categories:
                            categories.append(product_category['name'])
                    categories_str = ' '.join(categories)
                    if product.is_use_custom_model:
                        merge_row = [] #合并单元格使用

                        low_price = product.display_price
                        gross_profit_lowest = 0 #最低商品毛利
                        gross_profits = [] #商品毛利集合
                        stocks_lowest = 0
                        stocks_list = []
                        total_stocks = product.total_stocks

                        models_count = len(product.models)
                        tmp_models_count = 0 
                        for model in product.custom_models:
                            tmp_line += 1
                            merge_row.append(tmp_line-1)
                            model_name = []
                            for key,value in model['property2value'].items():

                                model_name.append( key +':'+ value['name'])
                            model_name_str = ' '.join(model_name)
                            purchase_price = float(model['price']) - float(model['gross_profit'])
                            gross_profit = model['gross_profit']
                            gross_profits.append(gross_profit)

                            if model['stock_type'] == 1:
                                stocks = model['stocks']
                                stocks_list.append(stocks)
                            elif model['stock_type'] == 0:
                                stocks = u'无限'




                            alist = [product.id, model['user_code'], supplier_name_export, product.name, model_name_str, model['price'], low_price, purchase_price, gross_profit, '', point_type, stocks,
                            '', total_stocks, categories_str, product_sales, product_sales_money, onshelvetime]

                            tmp_models_count += 1
                            if tmp_models_count == models_count:
                                if gross_profits:
                                    gross_profit_lowest = list(set(gross_profits))[0]
                                alist[9] = gross_profit_lowest

                                if stocks_list:
                                    stocks_lowest = list(set(stocks_list))
                                alist[12] = stocks_lowest
                            
                            table.write_row("A{}".format(tmp_line), alist, cell_format)
                        #合并单元格
                        # list(set(merge_row))
                        if models_count > 1:
                            merge_columns = [2, 3, 6, 9,10, 12,13,14,15,16,17]
                            for i in merge_columns:
                                table.merge.append((merge_row[0], i, merge_row[-1],i))

                    else:
                        tmp_line += 1
                        model = product.standard_model

                        total_stocks = product.total_stocks

                        alist = [product.id, model['user_code'], supplier_name_export, product.name, product.name, model['price'], model['price'], float(model['price'])-float(model['gross_profit']) , model['gross_profit'], model['gross_profit'], point_type, total_stocks,
                            total_stocks, total_stocks, categories_str, product_sales, product_sales_money, onshelvetime]

                        table.write_row("A{}".format(tmp_line), alist, cell_format)




    except:
        notify_message = "导出商品任务失败,response:{}".format(unicode_full_stack())
        export_jobs.update(status=2,is_download=1)
        watchdog_error(notify_message)

    workbook.close()
    upyun_path = '/upload/excel/{}'.format(filename)
    yun_url = upyun_util.upload_image_to_upyun(file_path, upyun_path)
    export_jobs.update(status=1,file_path=yun_url,update_at=datetime.now())