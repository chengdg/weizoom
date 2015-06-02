# -*- coding: utf-8 -*-
	#from webapp.modules.mall.models import MallConfig
	#from webapp.modules.mall.models import MallConfig

#import time
#from datetime import timedelta, datetime, date
#import urllib, urllib2
#import os
import json
#import shutil

#from django.http import HttpResponseRedirect, HttpResponse
#from django.template import Context, RequestContext
#from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
#from django.shortcuts import render_to_response
#from django.contrib.auth.models import User, Group, Permission
#from django.contrib import auth
#from django.db.models import Q, F
from django.test import Client

#from tools.regional import views as regional_util
from core.jsonresponse import decode_json_str
#from core.exceptionutil import unicode_full_stack
#from core import dateutil
from cache import product_cache

from models import *
from webapp.models import Workspace
from webapp.modules.mall.models import MallConfig


def __add_user_modules(user, modules):
	"""
	为user添加webapp modules
	"""
	if Workspace.objects.filter(owner=user).count() > 0:
		#已经存在，不重新安装
		if settings.MODE == 'develop':
			print 'no need to add user module'
		return True

	#模拟POST，进行用户模块选择操作
	params = {
		'user_id': user.id,
		'modules': json.dumps(modules)
	}

	client = Client()
	if settings.MODE == 'develop':
		print 'add user module for %s with %s' % (user.username, params)
	html_response = client.post('/webapp/api/user_module/add/', params)
	print html_response

	#从response中抽取返回的文本
	jsonresponse = decode_json_str(html_response.content)
	if jsonresponse['code'] != 200:
		error_msg = jsonresponse.get('errMsg', '') + ' ' + jsonresponse.get('innerErrMsg', '')
		raise ValueError(u"开模块失败:{}".format(error_msg.decode('utf-8')))

	return True


def install_product_for_user(user, product_id):
	"""
	为user安装product
	"""
	from django.contrib.auth.models import Permission
	from django.contrib.auth.models import Group
	from django.contrib.contenttypes.models import ContentType
	from market_tools.models import OperatePermission

	can_dump_log = (settings.MODE == 'develop')

	product = Product.objects.get(id=product_id)
	# ctype = ContentType.objects.get_for_model(OperatePermission)
	# permissions = []
	# for market_tool_module in product.market_tool_modules.split(','):
	# 	if not market_tool_module:
	# 		continue

	# 	permission_name = market_tool_module
	# 	try:
	# 		permission = Permission.objects.get(codename=permission_name, content_type=ctype)
	# 	except:
	# 		if can_dump_log:
	# 			print 'create permission for: ', permission_name
	# 		permission = Permission.objects.create(name="Can operate %s" % permission_name, codename=permission_name, content_type=ctype)
	# 	permissions.append(permission)
	# user.user_permissions = permissions

	if UserHasProduct.objects.filter(owner=user).count() > 0:
		UserHasProduct.objects.filter(owner=user).update(product=product)
	else:
		UserHasProduct.objects.create(
			owner = user, 
			product = product
		)

	MallConfig.objects.filter(owner=user).update(max_product_count=product.max_mall_product_count)

	#安装webapp modules
	__add_user_modules(user, [item for item in product.webapp_modules.split(',') if item])



def has_permission_to_access(user, path):
	"""
	判断user是否有权限访问指定的path
	"""
	if '/market_tools/' == path:
		return True

	if '/market_tools/' in path:
		beg = path.find('/market_tools/') + len('/market_tools/')
		end = path.find('/', beg)
		market_tool_name = path[beg:end]

		if not hasattr(user, 'market_tool_modules'):
			user.market_tool_modules = get_market_tool_modules_for_user(user)

		if market_tool_name in user.market_tool_modules:
			return True
		else:
			return False

	return True


def get_market_tool_modules_for_user_id(user_id):
	"""
	获得user_id拥有的market tool module集合
	"""
	try:
		user = User.objects.get(id=user_id)
		return get_market_tool_modules_for_user(user)
	except:
		return set()


def get_market_tool_modules_for_user(user):
	"""
	获得user拥有的market tool module集合
	"""
	if hasattr(user, 'market_tool_modules'):
		return user.market_tool_modules
	else:
		try:
			# 之前的操作方式(用于对比，deprecated)
			#product = UserHasProduct.objects.get(owner=user).product

			# 从缓存中读入product数据。(TODO: 什么时候令缓存中的数据失效？)
			product = product_cache.get_user_product(user)
			if product is None:
				return set()
			market_tool_modules = [item for item in product.market_tool_modules.split(',') if item]
			return set(market_tool_modules)
		except:
			return set()


def get_product_name(product_id):
	"""
	获取product名字
	"""
	product = Product.objects.get(id=product_id)

	return product.name


def get_product_for_user(user):
	"""
	获取user对应的product
	"""
	try:
		return UserHasProduct.objects.get(owner=user).product
	except:
		return {'footer': 0} #0代表weizoom footer

