# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator

from mall.models import *
from mall import module_api as mall_module_api
import module_api
from util import *


PRODUCT_TYPES = [PRODUCT_DEFAULT_TYPE, PRODUCT_INTEGRAL_TYPE]
########################################################################
# get_products: 获取product列表
########################################################################
@arguments_required('token')
@session_required
def get_products(request):
	token = request.GET.get('token', '').strip()

	products = []
	other_mall_products = []
	product_types = PRODUCT_TYPES
	user =  request.user
	webapp_id = user.get_profile().webapp_id

	search_type = request.GET.get('search_type', '0')
	start_time = request.GET.get('start_time', None)
	end_time = request.GET.get('end_time', None)
	if int(search_type) == 0:
		if start_time and end_time:
			products = Product.objects.filter(owner=user, is_deleted = False, update_time__gte=start_time, update_time__lt=end_time)
			total_count = products.count()
		elif start_time:
			products = Product.objects.filter(owner=user, is_deleted = False, update_time__gte=start_time)
			total_count = products.count()
		elif end_time:
			products = Product.objects.filter(owner=user, is_deleted = False, update_time__lt=end_time)
			total_count = products.count()
		else:
			products = Product.objects.filter(owner=user, is_deleted = False)
			total_count = products.count()
	else:
		products = Product.objects.filter(owner=user, is_deleted = False)
		total_count = products.count()
	
	#products = Product.objects.filter(owner=request.user, is_deleted = False)
	other_mall_products, other_mall_product_ids = mall_module_api.get_weizoom_mall_partner_products_and_ids(webapp_id)
		
	products = list(products)
	if other_mall_products:
		# 未审核置顶
		unapproved_products = list()
		audited_products = list()
		for product in other_mall_products:
			if hasattr(product, 'is_checked') and product.is_checked:
				audited_products.append(product)
			else:
				unapproved_products.append(product)
		unapproved_products.sort()
		audited_products.sort()
		
		products = (list(unapproved_products))+products+(list(audited_products))

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, products = paginator.paginate(products, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	#获取product关联的category集合
	id2product = dict([(product.id, product) for product in products])
	product_ids = []
	for product in products:
		product.categories = []
		id2product[product.id] = product
		product_ids.append(product.id)


	category_ids = []
	category2products = {}
	current_category_ids = [category.id for category in ProductCategory.objects.filter(owner=user)]
	for relation in CategoryHasProduct.objects.filter(category_id__in=current_category_ids, product_id__in=product_ids):
		category_id = relation.category_id
		product_id = relation.product_id
		category_ids.append(category_id)
		category2products.setdefault(category_id, []).append(product_id)
	for category in ProductCategory.objects.filter(id__in=category_ids):
		for product_id in category2products[category.id]:
			id2product[product_id].categories.append({
				'name': category.name
			})
			
	# 构造返回数据
	Product.fill_display_price(products)
	items = []

	for product in products:
		if other_mall_product_ids and product.id in other_mall_product_ids:
			product.is_from_other_mall = True
			if not hasattr(product, 'is_checked'):
				product.is_checked = WeizoomMallHasOtherMallProduct.objects.get(product_id=product.id).is_checked
		else:
			product.is_from_other_mall = False
			product.is_checked = '-'

		product.swipe_images = []
		for swipe_image in ProductSwipeImage.objects.filter(product_id=product_id):
			product.swipe_images.append({
				'url': swipe_image.url
			})
		product.swipe_images_json = json.dumps(product.swipe_images)

		items.append({
			'id': product.id,
			'name': product.name,
			'thumbnails_url': product.thumbnails_url,
			'categories': product.categories,
			'price': product.display_price,
			'update_time': datetime.strftime(product.update_time, '%Y-%m-%d %H:%M'),
			'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M')
		})

	response = create_response(200)
	response.data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'search_type':search_type
	}
	return response.get_response()

@arguments_required('token', 'product_id')
@session_required
def get_product(request):
	token = request.GET.get('token', '').strip()

	product_id = request.GET.get('product_id', None)
	try:
		if product_id and Product.objects.filter(id=product_id).count() > 0:
			product = Product.objects.get(id=product_id)
			product.fill_display_price([product])
			product.categories = [{'NAME': c.category.name} for c in CategoryHasProduct.objects.filter(product=product)]
			product.fill_model()
			product.swipe_images = []
			for swipe_image in ProductSwipeImage.objects.filter(product_id=product_id):
				product.swipe_images.append({
					'url': swipe_image.url
				})
			product_json = {'id': product.id,
				'name': product.name,
				'thumbnails_url': product.thumbnails_url,
				'categories': product.categories,
				'price': product.display_price,
				'update_time': datetime.strftime(product.update_time, '%Y-%m-%d %H:%M'),
				'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M'),
				'product_module': product.models
				}
			if product.is_use_custom_model:
				models = []
				for model in product.models:
					if model['name'] is not 'standard':
						model_names = []		

						for property in model['property_values']:
							print property
							model_names.append(property.get('name'))
						del model['property_values']
						model['value'] = u' '.join(model_names)
						models.append(model)
				product_json['product_module'] = models
			else:
				product_json['product_module'] = product.models

			response = create_response(200)
			response.data = {
				'items': [product_json],
			}
			return response.get_response()
		elif product_id:
			response = create_response(540)
			response.errMsg = u'商品不存在'
			return response.get_response()	
		else:	
			response = create_response(541)
			response.errMsg = u'输入product_id'
			return response.get_response()	
	except:
		response = create_response(590)
		response.errMsg = u'系统异常'
		return response.get_response()
	


