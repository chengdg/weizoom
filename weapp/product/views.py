# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
import module_api as weapp_product_api
from webapp.models import Workspace
from market_tools import ToolModule
from core.jsonresponse import create_response, JsonResponse
from mall.models import MallConfig


FIRST_NAV_NAME = 'product'
SECOND_NAV_NAME = 'webapp'


#===============================================================================
# show_products: 显示Product列表
#===============================================================================
@login_required
def show_products(request):
	products = Product.objects.all()

	id2webapp = dict([(workspace.id, workspace.name) for workspace in Workspace.objects.filter(owner=request.user)])
	name2markettool = dict([(module.module_name, module.settings.TOOL_NAME) for module in ToolModule.all_tool_modules()])

	product2usercount = {}
	for relation in UserHasProduct.objects.all():
		product_id = relation.product_id
		if product_id in product2usercount:
			product2usercount[product_id] = product2usercount[product_id] + 1
		else:
			product2usercount[product_id] = 1

	for product in products:
		product.webapp_modules = [id2webapp[int(id)] for id in product.webapp_modules.split(',') if id]
		product.market_tool_modules = [name2markettool[name] for name in product.market_tool_modules.split(',') if name]
		product.user_count = product2usercount.get(product.id, 0)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': None,
		'products': products
	})
	return render_to_response('product/products.html', c)


########################################################################
# add_product: 添加Weapp Product
########################################################################
def __extract_checkboxes(post, prefix):
	values = []
	for name in post:
		if name.startswith(prefix):
			values.append(post['name'])

	return values

@login_required
def add_product(request):
	if request.POST:
		webapp_modules = ','.join([request.POST[name] for name in request.POST if name.startswith('webapp_')])
		market_tool_modules = ','.join([request.POST[name] for name in request.POST if name.startswith('market_tool_')])
		name = request.POST.get('name', '').strip()
		price = request.POST.get('price', '').strip()
		footer = request.POST.get('footer', '').strip()
		max_mall_product_count = request.POST.get('max_mall_product_count', '').strip()
		remark = request.POST.get('remark', '').strip()

		product = None
		product_id = int(request.POST.get('product_id', -1))
		if product_id > 0:
			product = Product.objects.get(id = product_id)
		if product:
			product.name = name
			product.price = price
			product.footer = footer
			product.max_mall_product_count = max_mall_product_count
			product.webapp_modules = webapp_modules
			product.market_tool_modules = market_tool_modules
			product.remark = remark
			product.save()

			user_ids = set([r.owner_id for r in UserHasProduct.objects.filter(product_id=product_id)])
			MallConfig.objects.filter(owner_id__in=user_ids).update(max_product_count=max_mall_product_count)
		else:
			product = Product.objects.create(
				name = name,
				price = price,
				footer = footer,
				max_mall_product_count = max_mall_product_count,
				webapp_modules = webapp_modules,
				market_tool_modules = market_tool_modules,
				remark = remark
			)

		return HttpResponseRedirect('/product/products/')
	else:
		product_id = int(request.GET.get('id', -1))
		product = None
		if product_id > 0:
			product = Product.objects.get(id=product_id)

		webapp_modules = []
		for module in Workspace.objects.filter(owner=request.user):
			webapp_modules.append({
				'name': module.name,
				'value': module.id
			})


		market_tool_modules = []
		for module in ToolModule.all_tool_modules():
			checked = False
			if product:
				if module.module_name in product.market_tool_modules:
					checked = True
			market_tool_modules.append({
				'name': module.settings.TOOL_NAME,
				'value': module.module_name,
				'checked': checked
			})

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': None,
			'footers': PRODUCT_FOOTERS,
			'webapp_modules': webapp_modules,
			'market_tool_modules': market_tool_modules,
			'product': product
		})
		return render_to_response('product/edit_product.html', c)


#===============================================================================
# install_product: 为用户安装product
#===============================================================================
@login_required
def install_product(request):
	product_id = request.POST['product_id']
	user_id = request.POST['user_id']

	weapp_product_api.install_product_for_user(User.objects.get(id=user_id), product_id)

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# show_product_users: 显示Product的用户列表
#===============================================================================
@login_required
def show_product_users(request):
	product_id = request.GET['product_id']

	user_ids = set([r.owner_id for r in UserHasProduct.objects.filter(product_id=product_id)])
	
	all_users = []
	for user in User.objects.all():
		if user.username == 'admin' or user.username == 'manager':
			continue
		all_users.append(user)

	product_users = [user for user in all_users if user.id in user_ids]

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': None,
		'product_id': product_id,
		'all_users': all_users,
		'product_users': product_users,
	})
	return render_to_response('product/product_users.html', c)