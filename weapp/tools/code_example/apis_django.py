# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
try:
    import Image
except:
    from PIL import Image

from django.template import Context, RequestContext
from django.conf import settings

from models import *
from core.jsonresponse import create_response, JsonResponse
import pagestore as pagestore_manager
from mall.models import *


######################################################################
# get_category: 获取商品分类详情
######################################################################
def get_category(request):
	category_id = request.display_info['datasource_record_id']
	category = Productcategory.objects.get(id=category_id)

	product_ids = [r.product_id for r in CategoryHasProduct.objects.filter(category=category)]

	products = []
	for product in Product.objects.filter(id__in=product_ids):
		products.append({
			'item__title': product.name,
			'item__detail': product.price,
			'item__image': product.pic_url,
			'item__link': './?module=mall&model=%s&rid=%s' % (Product._meta.module_name, product.id)
		})

	data = {
		'category': {'id': category.id},
		'product_list': {
			'data_groups': [{
				'datas': products
			}]
		},
		'name': {'text': category.name}
	}
	return data


######################################################################
# get_product: 获得商品详情
######################################################################
def get_product(request):
	product_id = request.display_info['datasource_record_id']
	product = Product.objects.get(id=product_id)
	
	print 'apis 22'

	return {
		'product': {'id': product_id},
		'name': {'text': product.name},
		'content': {'html': product.detail},
		'image': {'image': product.pic_url},
		'price': {'text': product.price}
	}
