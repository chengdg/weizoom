# -*- coding: utf-8 -*-
import json
from celery import task

from mall import models
from . import utils

@task(bing=True)
def update_sync_product_status(product, request):
    is_update = None
    update_data = []
    # 规格
    standard_model, custom_models = utils.extract_product_model(request)
    swipe_images = json.loads(request.POST.get('swipe_images', '[]'))
    if len(custom_models) > 0:
        utils.delete_weizoom_mall_sync_product(request, product.id)
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
    elif product.promotion_title != request.POST.get('promotion_title', '').strip():
        is_update = True
        update_data.append(u'促销标题')
    elif product.user_code != request.POST.get('user_code', '').strip():
        is_update = True
        update_data.append('商品编码')
    elif product.bar_code != request.POST.get('bar_code', '').strip():
        is_update = True
        update_data.append('商品条码')
    elif product.detail != request.POST.get('detail', '').strip():
        is_update = True
        update_data.append('商品详情')
    elif product_standard_model.price != float(standard_model['price']):
        is_update = True
        update_data.append('商品价格')
    elif product_standard_model.weight != float(standard_model['weight']):
        is_update = True
        update_data.append('商品重量')
    elif product_standard_model.user_code != standard_model['user_code']:
        is_update = True
        update_data.append('商品编码')
    elif property_ids != existed_property_ids:
        is_update = True
        update_data.append('商品属性')
    elif set([image['url'] for image in product.swipe_images]) != set([image['url'] for image in swipe_images]):
        is_update = True
        update_data.append('商品图片')
    else:
        pass
    if is_update:
        utils.update_weizoom_mall_sync_product_status(product.id)