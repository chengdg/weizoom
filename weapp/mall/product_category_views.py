# # -*- coding: utf-8 -*-

# """@package mall.product_category_views
# 商品分类模块的页面的实现文件
# """

# import time
# from datetime import timedelta, datetime, date
# import urllib, urllib2
# import os
# import json
# import MySQLdb
# import random
# import string

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
# import export
# from core.restful_url_route import *


# COUNT_PER_PAGE = 20
# FIRST_NAV = export.PRODUCT_FIRST_NAV


# @view(app='mall', resource='product_categories', action='get')
# @login_required
# def get_product_categories(request):
# 	"""
# 	商品分类列表页面
# 	"""
# 	#获取category集合
# 	product_categories = list(ProductCategory.objects.filter(owner=request.manager))

# 	#获取与category关联的product集合
# 	category_ids = [category.id for category in product_categories]
# 	relations = CategoryHasProduct.objects.filter(category_id__in=category_ids)
# 	category2products = {}
# 	relation2time = {}
# 	product_ids = set()
# 	for relation in relations:
# 		category2products.setdefault(relation.category_id, []).append(relation.product_id)
# 		relation2time['%s_%s' % (relation.category_id, relation.product_id)] = relation.created_at
# 		product_ids.add(relation.product_id)

# 	products = list(product for product in Product.objects.filter(owner=request.manager, id__in=product_ids) if not product.is_deleted)
# 	Product.fill_display_price(products)
# 	id2product = dict([(product.id, product) for product in products])

# 	empty_list = []
# 	today = datetime.today()
# 	for category in product_categories:
# 		category.products = []
# 		for product_id in category2products.get(category.id, empty_list):
# 			if not product_id in id2product:
# 				continue
# 			product = id2product[product_id]
# 			relation = '%s_%s' % (category.id, product_id)
# 			product.join_category_time = relation2time.get(relation, today)
# 			category.products.append(id2product[product_id])
# 		category.products.sort(lambda x,y: cmp(y.id, x.id))

# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV,
# 		'second_navs': export.get_second_navs(request),
# 		'second_nav_name': export.PRODUCT_MANAGE_CATEGORY_NAV,
# 		'product_categories': product_categories,
# 	})
# 	return render_to_response('mall/editor/product_categories.html', c)
