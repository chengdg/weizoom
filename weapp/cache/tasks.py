# -*- coding: utf-8 -*-
from __future__ import absolute_import
from operator import attrgetter
import time
import urllib2

import itertools
from django.conf import settings
from django.db.models import signals

import cache
from account.models import UserProfile
from utils import cache_util
from mall.models import WeizoomMall, ProductCategory, CategoryHasProduct
from mall import module_api as mall_api
from mall import models as mall_models
from mall.promotion import models as promotion_models
from mall.promotion.models import PROMOTION_TYPE_FLASH_SALE
from django.core.exceptions import ObjectDoesNotExist
import json
from django.db.models import Q

from watchdog.utils import watchdog_info
from weapp.hack_django import post_update_signal, post_delete_signal
from celery import task


@task(bind=True, time_limit=7200, max_retries=2)
def update_product_list_cache_task(self,webapp_owner_id):

    product_models = __get_product_models_for_list(webapp_owner_id)

    categories = ProductCategory.objects.filter(owner_id=webapp_owner_id)

    product_ids = [product_model.id for product_model in product_models]
    category_has_products = CategoryHasProduct.objects.filter(product__in=product_ids)
    product2categories = dict()
    for relation in category_has_products:
        product2categories.setdefault(relation.product_id, set()).add(relation.category_id)

    categories = [{"id": category.id, "name": category.name} for category in categories]

    from django.contrib.auth.models import User
    webapp_owner = User.objects.get(id=webapp_owner_id)
    mall_models.Product.fill_details(webapp_owner=webapp_owner, products=product_models, options={
            "with_price": True,
            "flash_sale": True,
            "with_selected_category": True
        })

    product_datas = []

    for product in product_models:

        if 'http:' in product.thumbnails_url:
            thumbnails_url = product.thumbnails_url
        else:
            thumbnails_url = '%s%s' % (settings.IMAGE_HOST, product.thumbnails_url)

        product_datas.append({
            "id": product.id,
            "name": product.name,
            "is_member_product": product.is_member_product,
            "display_price": product.display_price,
            "promotion_js": json.dumps(product.promotion),
            "thumbnails_url": thumbnails_url,
            "categories": list(product2categories.get(product.id, []))
        })

    # for product_data in product_datas:
    #     product_data['categories'] = list(product2categories.get(product_data['id'], []))

    data = {
        "products": product_datas,
        "categories": categories
    }
    watchdog_info({
        'msg_id': 'set_product_list_cache',
        'woid': webapp_owner_id,
        'data': data
    })
    key = 'webapp_products_categories_{wo:%s}' % webapp_owner_id
    api_key = 'api' + key
    cache_util.set_cache(api_key, data)


def __get_product_models_for_list(webapp_owner_id):
    mall_type = UserProfile.objects.get(user_id=webapp_owner_id).webapp_type
    products = None

    if mall_type:
        pool_products = mall_models.ProductPool.objects.filter(woid=webapp_owner_id, status=mall_models.PP_STATUS_ON)
        pool_product2display_index = dict([(p.product_id, p.display_index) for p in pool_products])
        if pool_product2display_index:

            # products1 = mall_models.Product.select().where(
            #     (mall_models.Product.id << pool_product2display_index.keys()) |
            #     ((mall_models.Product.owner == webapp_owner_id) & (
            #     mall_models.Product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON) & (
            #      mall_models.Product.is_deleted == False) & (
            #      mall_models.Product.type.not_in([mall_models.PRODUCT_DELIVERY_PLAN_TYPE])))).order_by(
            #     mall_models.Product.display_index, -mall_models.Product.id)

            products = mall_models.Product.objects.filter(Q(id__in=pool_product2display_index.keys()) | Q(owner_id=webapp_owner_id,
                                                                                               shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON,
                                                                                               is_deleted=False)).exclude(
                type__in=[mall_models.PRODUCT_DELIVERY_PLAN_TYPE]).order_by(
                'display_index', '-id')

            # 处理排序 TODO bert 优化
            product_list = []
            for product in products:
                if product.id in pool_product2display_index.keys():
                    product.display_index = pool_product2display_index[product.id]
                if product.display_index == 0:
                    product.display_index = 99999999
                product_list.append(product)
            product_list.sort(lambda x, y: cmp(x.display_index, y.display_index))

            products = product_list

    if products is None:
        products = mall_models.Product.objects.filter(
            owner=webapp_owner_id,
            shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON,
            is_deleted=False).order_by('display_index', '-id')

        products_0 = products.filter(display_index=0)
        products_not_0 = products.exclude(display_index=0)
        products = list(itertools.chain(products_not_0, products_0))

    return products