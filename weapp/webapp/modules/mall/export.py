# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from webapp import module_views as webapp_module_views
from mall.models import WeizoomMall

from mall.models import ProductCategory, Product, Order
import module_api

NAV = {
	'section': u'微信商城',
	'navs': [
		# Termite GENERATED START: webapp_template_info


		# MODULE START: productcategory
		{
			'name': 'mall-category',
			'title': u'商品分类',
			'url': '/mall/editor/productcategories/',
		},
		# MODULE END: productcategory


		# MODULE START: product
		{
			'name': 'mall-product',
			'title': u'商品列表',
			'url': '/mall/editor/products/',
		},
		{
			'name': 'mall-orders',
			'title': u'订单管理',
			'url': '/mall/editor/orders/',
		},
		{
			'name': 'mall-settings',
			'title': u'其他选项',
			'url': '/mall/editor/mall_settings/',
		},
		# MODULE END: product
		# Termite GENERATED END: webapp_template_info
	]
}


PAGES = [
	{
		'name': ProductCategory._meta.verbose_name,
		'value': ProductCategory._meta.module_name
	},
	{
		'name': Product._meta.verbose_name,
		'value': Product._meta.module_name
	},
	 {
		'name': Order._meta.verbose_name,
		'value': Order._meta.module_name
	}
]

########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.user.username == 'manager':
		second_navs = []
		second_navs.append(NAV)
		second_navs.append({
			'section': u'项目',
			'navs': [{
				'name': u'项目管理',
				'url': '/webapp/',
				'title': u'项目管理'
			}]
		})
	else:
		second_navs = webapp_module_views.get_modules_page_second_navs(request)

	return second_navs


########################################################################
# get_link_targets: 检查product名是否有重复
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=mall&webapp_owner_id=%d' % request.workspace.owner_id
	has_data_category_filter = (request.GET.get('data_category_filter', None) != None)

	#获得category集合
	if has_data_category_filter:
		categories = []
	else:
		categories = [{'text': u'全部', 'value': './?module=mall&model=products&action=list&category_id=0&%s' % workspace_template_info}]
	for category in ProductCategory.objects.filter(owner=request.user):
		categories.append({
			'text': category.name, 
			'value': './?module=mall&model=products&action=list&category_id=%d&%s' % (category.id, workspace_template_info),
			'meta': {
				'id': category.id,
				'name': category.name,
				'type': 'product_category'
			}
		})

	if not has_data_category_filter:
		#获得product集合
		products = []
		#获得本商户的商品
		temp_products = list(Product.objects.filter(owner=request.user, is_deleted=False, type='object'))
		if request.user.is_weizoom_mall:
			#获取微众商城中其他商户的商品
			other_mall_products,other_mall_product_ids = module_api.get_verified_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
			#合并商品
			temp_products.extend(other_mall_products)
		temp_products.sort(lambda x,y: cmp(y.display_index, x.display_index))

		Product.fill_display_price(temp_products)
		for product in temp_products:
			products.append({
				'text': product.name, 
				'value': './?module=mall&model=product&action=get&rid=%d&%s' % (product.id, workspace_template_info),
				'meta': {
					'pic_url': product.thumbnails_url,
					'name': product.name,
					'price': product.display_price,
					'id': product.id
				}
			})

		#获得页面
		pages = []
		pages.append({'text': u'商品列表页', 'value': './?module=mall&model=products&action=list&category_id=0&%s' % workspace_template_info})
		if request.user.is_weizoom_mall:
			pages.append({'text': u'我的购物车', 'value': './?module=mall&model=shopping_cart&action=show&%s' % workspace_template_info})
		pages.append({'text': u'我的订单', 'value': './?module=mall&model=order_list&action=get&%s' % workspace_template_info})

		response.data = [
			{
				'name': u'商品分类',
				'data': categories
			}, {
				'name': u'商品',
				'data': products
			},
			{
				'name': u'页面',
				'data': pages
			}
		]
	else:
		response.data = [
			{
				'name': u'商品分类',
				'data': categories
			}
		]
	return response.get_response()



######################################################################
# create_order: 创建订单
######################################################################
def create_order(request):
	response = create_response(200)
	response.data = {
		'order_id': 101
	}

	return response.get_response()