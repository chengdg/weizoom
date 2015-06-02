# -*- coding: utf-8 -*-

"""@package mall.product_category_api_views
商品分类模块的API的实现文件
"""

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

import models as mall_models
from models import *
import export
from core import paginator
from core.restful_url_route import *
from core.jsonresponse import create_response


COUNT_PER_PAGE = 20
FIRST_NAV = export.PRODUCT_FIRST_NAV


@api(app='mall', resource='category_products', action='get')
@login_required
def get_category_products(request):
	"""
	获得商品分类的可选商品列表

	可选商品指的是还不属于当前分类的商品

		可选商品集合 ＝ manager的所有商品集合 － 已经在分类中的商品集合

	Method: GET

	@param id 分类id
	"""
	category_id = int(request.GET['id'])
	name_query = request.GET.get('name', None)

	#获取商品集合
	products = [product for product in Product.objects.filter(owner=request.manager) if not product.is_deleted]
	if name_query:
		products = [product for product in products if name_query in product.name]

	if category_id != -1:
		#获取已在分类中的商品
		relations = CategoryHasProduct.objects.filter(category_id=category_id)
		existed_product_ids = set([relation.product_id for relation in relations])

		#获取没在分类中的商品集合(分类的可选商品集合)
		products = filter(lambda product: (not product.id in existed_product_ids), products)
	
	products.sort(lambda x,y: cmp(x.id, y.id))

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, products = paginator.paginate(products, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	Product.fill_display_price(products)
	result_products = []
	for product in products:
		relation = '%s_%s' % (category_id, product.id)
		result_products.append({
			"id": product.id,
			"name": product.name,
			"display_price": product.display_price,
			"status": product.status,
			"sales": -1,
			"update_time": product.update_time.strftime("%Y-%m-%d")
		})
	result_products.sort(lambda x,y: cmp(y['id'], x['id']))
	
	response = create_response(200)
	response.data = {
		'items': result_products,
		'pageinfo': paginator.to_dict(pageinfo),
		'sortAttr': '',
		'data': {}
	}
	return response.get_response()


########################################################################
# create_product_category: 创建商品分类
########################################################################
@api(app='mall', resource='product_category', action='create')
@login_required
def create_product_category(request):
	"""
	创建商品分类

	Method: POST

	@param name 分类名
	@param product_ids 属于该分类的商品id集合
	"""
	if request.POST:
		product_category = ProductCategory.objects.create(
			owner = request.manager,
			name = request.POST.get('name', '').strip()
		)
		#product_category.display_index = 0-product_category.id
		product_ids = request.POST.getlist('product_ids[]')
		product_category.product_count = len(product_ids)
		product_category.save()

		for product_id in product_ids:
			CategoryHasProduct.objects.create(product_id=product_id, category=product_category)

		return create_response(200).get_response()


@api(app='mall', resource='product_category', action='update')
@login_required
def update_product_category(request):
	"""
	更新商品分类

	Method: POST

	@param id 分类id
	@param name 新的分类名
	@param product_ids 新的属于该分类的商品id集合
	"""
	category_id = request.POST['id']
	product_ids = request.POST.getlist('product_ids[]')

	ProductCategory.objects.filter(id=category_id).update(
		name = request.POST.get('name', '').strip(),
		product_count = len(product_ids)
	)
		
	#重建<category, product>关系
	for product_id in product_ids:
		CategoryHasProduct.objects.create(product_id=product_id, category_id=category_id)

	return create_response(200).get_response()


@api(app='mall', resource='product_category', action='delete')
@login_required
def delete_product_category(request):
	"""
	删除商品分类

	Method: POST

	@param id 分类id
	"""
	id = request.POST['id']

	ProductCategory.objects.filter(owner=request.manager, id=id).delete()

	return create_response(200).get_response()


@api(app='mall', resource='product_in_category', action='delete')
@login_required
def delete_product_in_category(request):
	"""
	从商品分类删除一个商品

	Method: POST

	@param category_id 分类id
	@param product_id 商品id
	"""
	product_id = request.POST['product_id']
	category_id = request.POST['category_id']

	CategoryHasProduct.objects.filter(product_id=product_id, category_id=category_id).delete()

	return create_response(200).get_response()