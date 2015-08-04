# -*- coding: utf-8 -*-
"""@package mall.product_api_views
商品管理模块的API的实现文件
"""

# import time
# from datetime import timedelta, datetime, date
# import urllib, urllib2
# import os
# import json
# import MySQLdb
# import random
# import string
# import operator

# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.shortcuts import render_to_response
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib import auth
# from django.db.models import Q, F
# from django.db.models.aggregates import Sum, Count

# import models as mall_models
# from models import *
# from core import paginator
# import export
# from core.restful_url_route import *
# from core.jsonresponse import create_response
# from core import search_util
# import signals as mall_signals


# COUNT_PER_PAGE = 10

# PRODUCT_FILTERS = {
# 	'product': [{
# 			'comparator': lambda product, filter_value: filter_value in product.name,
# 			'query_string_field': 'name'
# 		}, {
# 			'comparator': lambda product, filter_value: product.sales >= int(filter_value),
# 			'query_string_field': 'lowSales'
# 		}, {
# 			'comparator': lambda product, filter_value: product.sales <= int(filter_value),
# 			'query_string_field': 'highSales'
# 		}, {
# 			'comparator': lambda product, filter_value: (int(filter_value) == -1) or (int(filter_value) in [category['id'] for category in product.categories if category['is_selected']]),
# 			'query_string_field': 'category'
# 		}, {
# 			'comparator': lambda product, filter_value: filter_value == product.bar_code,
# 			'query_string_field': 'barCode'
# 		}, {
#             'comparator': lambda product, filter_value: product.created_at >= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
#             'query_string_field': 'startDate'
#         }, {
#             'comparator': lambda product, filter_value: product.created_at <= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
#             'query_string_field': 'endDate'
#         }],
# 	'model': [{
# 			'comparator': lambda model, filter_value: model['price'] >= float(filter_value),
# 			'query_string_field': 'lowPrice'
# 		}, {
# 			'comparator': lambda model, filter_value: model['price'] <= float(filter_value),
# 			'query_string_field': 'highPrice'
# 		}, {
# 			'comparator': lambda model, filter_value: model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT or model['stocks'] >= int(filter_value),
# 			'query_string_field': 'lowStocks'
# 		}, {
# 			'comparator': lambda model, filter_value: model['stocks'] <= int(filter_value),
# 			'query_string_field': 'highStocks'
# 		}
# 	]
# }


# def __filter_products(request, products):
# 	has_filter = search_util.init_filters(request, PRODUCT_FILTERS)
# 	if not has_filter:
# 		#没有filter，直接返回
# 		return products

# 	filtered_products = []
# 	products = search_util.filter_objects(products, PRODUCT_FILTERS['product'])
# 	if not products:
# 		#product filter没有通过，跳过该promotion
# 		print 'end in product filter'
# 		return filtered_products
# 	else:
# 		print 'pass product filter'

# 	for product in products:
# 		models = search_util.filter_objects(product.models, PRODUCT_FILTERS['model'])
# 		if models:
# 			print 'pass model filter'
# 			filtered_products.append(product)
# 		else:
# 			print 'end in model filter'

# 	return filtered_products

pass
# @api(app='mall', resource='products', action='get')
# @login_required
# def get_products(request):
# 	"""
# 	获取商品列表

# 	Method: GET
# 	"""
# 	type = request.GET['type']

# 	#处理排序
# 	sort_attr = request.GET.get('sort_attr', None)
# 	if not sort_attr:
# 		sort_attr = '-display_index'

# 	#处理商品分类
# 	if type == 'offshelf':
# 		products = Product.objects.filter(owner=request.manager, shelve_type=PRODUCT_SHELVE_TYPE_OFF, is_deleted=False)
# 	elif type == 'onshelf':
# 		products = Product.objects.filter(owner=request.manager, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted=False)
# 	elif type == 'recycled':
# 		products = Product.objects.filter(owner=request.manager, shelve_type=PRODUCT_SHELVE_TYPE_RECYCLED, is_deleted=False)
# 	else:
# 		products = Product.objects.filter(owner=request.manager, is_deleted=False)

# 	#未回收的商品
# 	products = products.order_by(sort_attr)

# 	products = list(products)
# 	Product.fill_details(request.manager, products, {
# 		"with_product_model": True,
# 		"with_model_property_info": True,
# 		"with_selected_category": True,
# 		'with_image': False,
# 		'with_property': True,
# 		'with_sales': True
# 	})
# 	products = __filter_products(request, products)

# 	#进行分页
# 	count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
# 	cur_page = int(request.GET.get('page', '1'))
# 	pageinfo, products = paginator.paginate(products, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

# 	#构造返回数据
# 	items = []
# 	for product in products:
# 		product_dict = product.format_to_dict()
# 		product_dict['is_self'] = (request.manager.id == product.owner_id)
# 		items.append(product_dict)

# 	data = dict()
# 	response = create_response(200)
# 	response.data = {
# 		'items': items,
# 		'pageinfo': paginator.to_dict(pageinfo),
# 		'sortAttr': sort_attr,
# 		'data': data
# 	}
# 	return response.get_response()

pass
########################################################################
# get_products_filter_params: 获取商品过滤参数
########################################################################
# @api(app='mall', resource='products_filter_params', action='get')
# @login_required
# def get_products_filter_params(request):
# 	"""
# 	获取商品过滤参数

# 	Method: GET

# 	@return 如下格式的json
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
# 	{
# 		categories: [{
# 			id: 1,
# 			name: "分类1"
# 		}, {
# 			"id: 2,
# 			name: "分类2"
# 		}, {
# 			......
# 		}]
# 	}
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 	"""
# 	categories = []
# 	for category in ProductCategory.objects.filter(owner=request.manager):
# 		categories.append({
# 			"id": category.id,
# 			"name": category.name
# 		})

# 	response = create_response(200)
# 	response.data = {
# 		'categories': categories
# 	}
# 	return response.get_response()

pass
# @api(app='mall', resource='product_shelve_type', action='batch_update')
# @login_required
# def batch_update_product_shelve_type(request):
# 	"""
# 	批量更新一批商品的上架状态

# 	Method: POST

# 	@param ids 商品id列表
# 	@param shelve_type 上架类型
# 		- onshelf：上架
# 		- offshelf: 下架
# 		- recycled: 回收站
# 		- delete: 删除
# 	"""

# 	ids = request.POST.getlist('ids[]', [])
# 	if not ids:
# 		return create_response(200).get_response()

# 	first_product = Product.objects.get(id=ids[0])
# 	prev_shelve_type = first_product.shelve_type

# 	shelve_type = request.POST['shelve_type']
# 	if shelve_type == 'onshelf':
# 		shelve_type = PRODUCT_SHELVE_TYPE_ON
# 	elif shelve_type == 'offshelf':
# 		shelve_type = PRODUCT_SHELVE_TYPE_OFF
# 	elif shelve_type == 'recycled':
# 		shelve_type = PRODUCT_SHELVE_TYPE_RECYCLED

# 	if shelve_type == 'delete':
# 		Product.objects.filter(id__in=ids).update(shelve_type=-1, is_deleted=True)
# 	else:
# 		Product.objects.filter(id__in=ids).update(shelve_type=shelve_type, is_deleted=False)

# 	if prev_shelve_type == PRODUCT_SHELVE_TYPE_ON and shelve_type != PRODUCT_SHELVE_TYPE_ON:
# 		#商品不再处于上架状态，发出product_not_online signal
# 		product_ids = [int(id) for id in ids]
# 		mall_signals.products_not_online.send(sender=Product, product_ids=product_ids, request=request)

# 	response = create_response(200)
# 	return response.get_response()

# @api(app='mall', resource='product_shelve_type', action='update')
# @login_required
# def update_product_shelve_type(request):
# 	"""
# 	更新单个商品的上架状态

# 	Method: POST

# 	@param ids 商品id列表
# 	@param shelve_type 上架类型
# 		- onshelf：上架
# 		- offshelf: 下架
# 		- recycled: 回收站
# 		- delete: 删除
# 	"""
# 	id = request.POST['id']
# 	if not id:
# 		return create_response(200).get_response()

# 	shelve_type = request.POST['shelve_type']
# 	if shelve_type == 'onshelf':
# 		shelve_type = PRODUCT_SHELVE_TYPE_ON
# 	elif shelve_type == 'offshelf':
# 		shelve_type = PRODUCT_SHELVE_TYPE_OFF
# 	elif shelve_type == 'recycled':
# 		shelve_type = PRODUCT_SHELVE_TYPE_RECYCLED

# 	product = Product.objects.filter(id=id)
# 	prev_shelve_type = product[0].shelve_type
# 	if shelve_type == 'delete':
# 		product.update(shelve_type=-1, is_deleted=True)
# 	else:
# 		if request.manager.id == product[0].owner_id:
# 			if shelve_type != PRODUCT_SHELVE_TYPE_ON:
# 				product.update(shelve_type=shelve_type, weshop_status=shelve_type, is_deleted=False)
# 			else:
# 				product.update(shelve_type=shelve_type, is_deleted=False)
# 		else:
# 			product.update(weshop_status=shelve_type)

# 	if prev_shelve_type == PRODUCT_SHELVE_TYPE_ON and shelve_type != PRODUCT_SHELVE_TYPE_ON:
# 		#商品不再处于上架状态，发出product_not_offline signal
# 		product_ids = [int(id)]
# 		mall_signals.products_not_online.send(sender=Product, product_ids=product_ids, request=request)

# 	response = create_response(200)
# 	return response.get_response()


########################################################################
# update_product_model_stocks: 更新商品标准规格库存
########################################################################
# @api(app='mall', resource='product_model_stocks', action='update')
# @login_required
# def update_product_model_stocks(request):
# 	"""
# 	更新商品规格库存

# 	Method: POST

# 	@param model_infos 需要更新的商品规格信息，格式如下
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
# 	{
# 		[{
# 			id: 1,
# 			stock_type: "limit", //库存类型
# 			stocks: 3 //库存数量
# 		}, {
# 			id: 2,
# 			stock_type: "unlimit",
# 			stocks: 0
# 		}, {
# 			......
# 		}]
# 	}
# 	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 	"""
# 	model_infos = json.loads(request.POST.get('model_infos', '[]'))
# 	for model_info in model_infos:
# 		stock_type = PRODUCT_STOCK_TYPE_LIMIT if model_info['stock_type'] == 'limit' else PRODUCT_STOCK_TYPE_UNLIMIT
# 		product_model_id = model_info['id']
# 		stocks = 0 if stock_type == PRODUCT_STOCK_TYPE_UNLIMIT else model_info['stocks']
# 		ProductModel.objects.filter(id=product_model_id).update(stock_type=stock_type, stocks=stocks)

# 	response = create_response(200)
# 	return response.get_response()
