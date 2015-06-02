# -*- coding: utf-8 -*-
"""@package mall.product_pay_interface_views
支付接口模块的页面的实现文件

目前有以下三种支付接口
 - 货到付款
 - 微信支付
 - 微众卡

每一种类型的支付接口都有两部分信息:
 - 支付接口的通用信息：这部分在PayInterface model中实现
 - 支付接口的特定信息：比如微信支付需要微信的一些认证信息，这些信息在各自的Config model中实现，比如对于微信支付，就是UserWeixinPayOrderConfig，在PayInterface model中，有一个属性related_config_id，指向特定的信息
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
from core.restful_url_route import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV


@view(app='mall', resource='pay_interfaces', action='get')
@login_required
def get_pay_interfaces(request):
	"""
	支付接口列表页面
	"""
	# if PayInterface.objects.filter(owner=request.user).count() == 0:
	# 	#初始化所有的支付接口
	# 	for pay_interface_type in VALID_PAY_INTERFACES:
	# 		PayInterface.objects.create(
	# 			owner = request.user,
	# 			type = pay_interface_type,
	# 			description = '',
	# 			is_active = False
	# 		)
	# else:
	pay_interface_types = [pay_interface.type for pay_interface in PayInterface.objects.filter(owner=request.user)]

	for pay_type_id in VALID_PAY_INTERFACES:
		if pay_type_id not in pay_interface_types:
			PayInterface.objects.create(
				owner = request.user,
				type = pay_type_id,
				description = '',
				is_active = False
			)
	
	pay_interfaces = list(PayInterface.objects.filter(owner=request.user))
	if request.user.can_use_weizoom_card():
		pay_interfaces = filter(lambda pay_interface: pay_interface.type != PAY_INTERFACE_WEIZOOM_COIN, pay_interfaces)
	for pay_interface in pay_interfaces:
		pay_interface.name = PAYTYPE2NAME[pay_interface.type]
		if pay_interface.type in [PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_ALIPAY] and pay_interface.related_config_id == 0:
			pay_interface.should_create_related_config = True
		else:
			pay_interface.should_create_related_config = False

		#获取接口对应的配置项
		if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY and pay_interface.related_config_id != 0:
			related_config = UserWeixinPayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
			configs = []
			if related_config.pay_version == 0:
				configs = [{
					"name":u"接口版本", "value":"v2"
				}, {
					"name":u"AppID", "value":related_config.app_id
				}, {
					"name":u"合作商户ID", "value":related_config.partner_id
				}, {
					"name":u"合作商户密钥", "value":related_config.partner_key
				}, {
					"name":u"支付专用签名串", "value":related_config.paysign_key
				}]
			else:
				configs = [{
					"name":u"接口版本", "value":"v3"
				}, {
					"name":u"AppID", "value":related_config.app_id
				}, {
					"name":u"AppSecret", "value":related_config.app_secret
				}, {
					"name":u"商户号MCHID", "value":related_config.partner_id
				}, {
					"name":u"APIKEY密钥", "value":related_config.partner_key
				}]
			pay_interface.configs = configs

		if pay_interface.type == PAY_INTERFACE_ALIPAY and pay_interface.related_config_id != 0:
			related_config = UserAlipayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
			configs = [{
					"name":u"合作者身份ID", "value":related_config.partner
				}, {
					"name":u"交易安全检验码", "value":related_config.key
				}, {
					"name":u"支付宝公钥", "value":related_config.ali_public_key
				}, {
					"name":u"商户私钥", "value":related_config.private_key
				}, {
					"name":u"邮箱", "value":related_config.seller_email
				}]
			pay_interface.configs = configs

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_config_second_navs(request),
		'second_nav_name': export.MALL_CONFIG_PAYINTERFACE_NAV,
		'pay_interfaces': pay_interfaces
	})
	return render_to_response('mall/editor/pay_interfaces.html', c)


def __add_weixin_pay_config(request):
	"""
	添加微信支付配置
	"""
	if int(request.POST.get('pay_version', 0)) == 0:
		config = UserWeixinPayOrderConfig.objects.create(
			owner = request.user,
			app_id = request.POST.get('app_id', ''),
			pay_version = request.POST.get('pay_version', 0),
			app_secret = request.POST.get('app_secret', ''),
			partner_id = request.POST.get('partner_id', ''),
			partner_key = request.POST.get('partner_key', ''),
			paysign_key = request.POST.get('paysign_key', ''),
		)
	else:
		config = UserWeixinPayOrderConfig.objects.create(
			owner = request.user,
			app_id = request.POST.get('app_id', ''),
			pay_version = request.POST.get('pay_version', 0),
			app_secret = request.POST.get('app_secret', ''),
			partner_id = request.POST.get('mch_id', ''),
			partner_key = request.POST.get('api_key', ''),
			paysign_key = request.POST.get('paysign_key', ''),
		)

	return config.id

# def __add_ali_pay_config(request):
# 	UserAlipayOrderConfig.objects.create(
# 		owner = request.user,
# 		partner = request.POST.get('partner', ''),
# 		key = request.POST.get('key', ''),
# 		private_key = request.POST.get('private_key', ''),
# 		ali_public_key = request.POST.get('ali_public_key', ''),
# 		# input_charset = request.POST.get('partner_key', ''),
# 		# sign_type = request.POST.get('paysign_key', ''),
# 		seller_email = request.POST.get('seller_email', ''),
# 		)
########################################################################
# __add_alipay_config: 添加支付宝配置
########################################################################
def __add_alipay_config(request):
	config = UserAlipayOrderConfig.objects.create(
		owner=request.user,
		partner = request.POST.get('partner', ''),
		key = request.POST.get('key', ''),
		private_key = request.POST.get('private_key', ''),
		ali_public_key = request.POST.get('ali_public_key', ''),
		seller_email = request.POST.get('seller_email', '')
	)

	return config.id


def __update_weixin_pay_config(request, pay_interface):
	"""
	更新微信支付配置
	"""
	if int(request.POST.get('pay_version', 0)) == 0:
		UserWeixinPayOrderConfig.objects.filter(owner=request.user, id=pay_interface.related_config_id).update(
			app_id = request.POST.get('app_id', ''),
			app_secret = request.POST.get('app_secret', ''),
			pay_version = request.POST.get('pay_version', 0),
			partner_id = request.POST.get('partner_id', ''),
			partner_key = request.POST.get('partner_key', ''),
			paysign_key = request.POST.get('paysign_key', '')
		)
	else:
		UserWeixinPayOrderConfig.objects.filter(owner=request.user, id=pay_interface.related_config_id).update(
			app_id = request.POST.get('app_id', ''),
			pay_version = request.POST.get('pay_version', 0),
			app_secret = request.POST.get('app_secret', ''),
			partner_id = request.POST.get('mch_id', ''),
			partner_key = request.POST.get('api_key', ''),
			paysign_key = request.POST.get('paysign_key', ''),
		)

def __update_alipay_config(request, pay_interface):
	config = UserAlipayOrderConfig.objects.filter(owner=request.user, id=pay_interface.related_config_id).update(
		partner = request.POST.get('partner', ''),
		key = request.POST.get('key', ''),
		private_key = request.POST.get('private_key', ''),
		ali_public_key = request.POST.get('ali_public_key', ''),
		seller_email = request.POST.get('seller_email', '')
	)

@view(app='mall', resource='pay_interface', action='create')
@login_required
def create_pay_interface(request):
	"""
	创建支付接口页面

	不同类型的支付接口需要调用不同的__add_{pay_interface}_config函数进行支付接口特定数据的创建
	"""
	pay_interface_id = request.GET['id']
	pay_interface = PayInterface.objects.get(id=pay_interface_id)
	if request.POST:
		#type = int(request.POST.get('type', '0'))
		if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
			related_config_id = __add_weixin_pay_config(request)
		elif pay_interface.type == PAY_INTERFACE_ALIPAY:
			related_config_id = __add_alipay_config(request)
		else:
			related_config_id = 0

		PayInterface.objects.filter(id=pay_interface_id).update(
			is_active = True,
			related_config_id = related_config_id
		)

		return HttpResponseRedirect('/mall/pay_interfaces/get/')
	else:
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_config_second_navs(request),
			'second_nav_name': export.MALL_CONFIG_PAYINTERFACE_NAV,
			'pay_interface_id': pay_interface_id,
			'pay_interface': pay_interface
		})
		return render_to_response('mall/editor/edit_pay_interface.html', c)


@view(app='mall', resource='pay_interface', action='update')
@login_required
def update_pay_interface(request):
	"""
	更新支付接口页面

	不同类型的支付接口需要调用不同的__update_{pay_interface}_config函数进行支付接口特定数据的创建

	@param id 支付接口id
	"""
	pay_interface_id = request.GET['id']
	if request.POST:
		pay_interface = PayInterface.objects.get(id=pay_interface_id)

		if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
			__update_weixin_pay_config(request, pay_interface)
		elif pay_interface.type == PAY_INTERFACE_ALIPAY:
			__update_alipay_config(request, pay_interface)
		else:
			pass

		return HttpResponseRedirect('/mall/pay_interfaces/get/')
	else:
		#获取指定的pay interface
		pay_interface = PayInterface.objects.get(owner=request.user, id=pay_interface_id)
		if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
			related_config = UserWeixinPayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
		elif pay_interface.type == PAY_INTERFACE_ALIPAY:
			related_config = UserAlipayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
		else:
			related_config = None
		pay_interface.related_config = related_config

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_config_second_navs(request),
			'second_nav_name': export.MALL_CONFIG_PAYINTERFACE_NAV,
			'pay_interface': pay_interface,
		})
		return render_to_response('mall/editor/edit_pay_interface.html', c)