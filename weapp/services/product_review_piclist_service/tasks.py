#coding:utf8
"""
@package services.product_review_piclist.tasks
异步处理商品评论的回复
"""
from datetime import datetime, timedelta
import time

from django.conf import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info

from mall.promotion import models as promotion_models
from mall import models as mall_models
import json
from celery import task
from account.views import save_base64_img_file_local_for_webapp,save_and_zip_base64_img_file_for_mobileApp

@task
def upload_pic_list(request, data_dict,product_review,order_has_product_id):
    picture_list = data_dict.get('picture_list', None)
    if picture_list:
        picture_list = json.loads(picture_list)
        picture_model_list = []

        for picture in picture_list:
            att_url=save_and_zip_base64_img_file_for_mobileApp(request, picture)
            mall_models.ProductReviewPicture(
                product_review=product_review,
                order_has_product_id=order_has_product_id,
                att_url=att_url
            ).save()
            watchdog_info(u"create_product_review after save img  %s" %\
                (att_url), type="mall", user_id=request.webapp_owner_id)