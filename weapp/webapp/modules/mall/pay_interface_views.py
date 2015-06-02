# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string
import copy

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.dateutil import get_today

from excel_response import ExcelResponse

from account.models import *
from models import *
from modules.member.models import IntegralStrategySttings
from market_tools.tools.weizoom_card.models import *

import export
import module_api

COUNT_PER_PAGE = 20

FIRST_NAV_NAME = 'webapp'
MALL_SETTINGS_NAV = 'mall-settings'


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


########################################################################
# __update_alipay_config: 更新支付宝配置
########################################################################
def __update_alipay_config(request, pay_interface):
	UserAlipayOrderConfig.objects.filter(owner=request.user, id=pay_interface.related_config_id).update(
		partner = request.POST.get('partner', ''),
		key = request.POST.get('key', ''),
		private_key = request.POST.get('private_key', ''),
		ali_public_key = request.POST.get('ali_public_key', ''),
		seller_email = request.POST.get('seller_email', '')
	)


########################################################################
# __add_tenpay_config: 添加财付通配置
########################################################################
def __add_tenpay_config(request):
	config = UserTenpayOrderConfig.objects.create(
		owner=request.user,
		partner = request.POST.get('tenpay_partner', ''),
		key = request.POST.get('tenpay_key', '')
	)

	return config.id


########################################################################
# __update_tenpay_config: 更新财付通配置
########################################################################
def __update_tenpay_config(request, pay_interface):
	UserTenpayOrderConfig.objects.filter(owner=request.user, id=pay_interface.related_config_id).update(
		partner = request.POST.get('tenpay_partner', ''),
		key = request.POST.get('tenpay_key', '')
	)


########################################################################
# __add_weixin_pay_config: 添加微信支付配置
########################################################################
def __add_weixin_pay_config(request):
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


########################################################################
# __update_weixin_pay_config: 更新微信支付配置
########################################################################
def __update_weixin_pay_config(request, pay_interface):
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

def __remove_weizoom_card_pay(request, existed_pay_interfaces):
	if (PAY_INTERFACE_WEIZOOM_COIN in existed_pay_interfaces) and (AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.user.id) is False):
		existed_pay_interfaces.remove(PAY_INTERFACE_WEIZOOM_COIN)
	# if (PAY_INTERFACE_WEIZOOM_COIN in existed_pay_interfaces) and (request.user.is_weizoom_mall is False):
	# 	existed_pay_interfaces.remove(PAY_INTERFACE_WEIZOOM_COIN)

def __get_pay_inferface_by_id(pay_inferface_id):
	try:
		return PayInterface.objects.get(id=pay_inferface_id)
	except:
		return None

########################################################################
# add_pay_interface: 添加支付接口
########################################################################
@login_required
def add_pay_interface(request):
	if request.POST:
		type = int(request.POST.get('type', '0'))
		if type == PAY_INTERFACE_ALIPAY:
			related_config_id = __add_alipay_config(request)
		elif type == PAY_INTERFACE_TENPAY:
			related_config_id = __add_tenpay_config(request)
		elif type == PAY_INTERFACE_WEIXIN_PAY:
			related_config_id = __add_weixin_pay_config(request)
		else:
			related_config_id = 0

		PayInterface.objects.create(
			owner = request.user,
			type = type,
			description = request.POST.get('description', ''),
			is_active = (request.POST.get('is_active', 'false') == 'true'),
			related_config_id = related_config_id
		)

		return HttpResponseRedirect('/mall/editor/mall_settings/')
	else:
		
		user_pay_interfaces = PayInterface.objects.filter(owner=request.user)
		existed_pay_interfaces = copy.copy(VALID_PAY_INTERFACES)
		__remove_weizoom_card_pay(request, existed_pay_interfaces)

		for user_pay_interface in user_pay_interfaces:
			if user_pay_interface.type in existed_pay_interfaces:
				existed_pay_interfaces.remove(user_pay_interface.type)

		pay_interfaces = []
		for existed_pay_interface in existed_pay_interfaces:
			pay_interfaces.append({
				'name': PAYTYPE2NAME[existed_pay_interface],
				'type': existed_pay_interface
			})

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MALL_SETTINGS_NAV,
			'pay_interfaces' : pay_interfaces
		})
		return render_to_response('mall/editor/edit_pay_interface.html', c)


########################################################################
# update_pay_interface: 更新支付接口
########################################################################
@login_required
def update_pay_interface(request, pay_interface_id):
	if request.POST:
		pay_interface = PayInterface.objects.get(id=pay_interface_id)

		if pay_interface.type == PAY_INTERFACE_ALIPAY:
			__update_alipay_config(request, pay_interface)
		elif pay_interface.type == PAY_INTERFACE_TENPAY:
			__update_tenpay_config(request, pay_interface)
		elif pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
			__update_weixin_pay_config(request, pay_interface)
		else:
			pass

		PayInterface.objects.filter(id=pay_interface_id).update(
			description = request.POST.get('description', ''),
			is_active = (request.POST.get('is_active', 'false') == 'true')
		)

		return HttpResponseRedirect('/mall/editor/mall_settings/')
	else:
		pay_interface = PayInterface.objects.get(owner=request.user, id=pay_interface_id)
		if pay_interface.type == PAY_INTERFACE_ALIPAY:
			related_config = UserAlipayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
		elif pay_interface.type == PAY_INTERFACE_TENPAY:
			related_config = UserTenpayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
		elif pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
			related_config = UserWeixinPayOrderConfig.objects.get(owner=request.user, id=pay_interface.related_config_id)
		else:
			related_config = None
		pay_interface.related_config = related_config

		existed_pay_interfaces = copy.copy(VALID_PAY_INTERFACES)
		__remove_weizoom_card_pay(request, existed_pay_interfaces)
		pay_interfaces = []
		for existed_pay_interface in existed_pay_interfaces:
			pay_interfaces.append({
				'name': PAYTYPE2NAME[existed_pay_interface],
				'type': existed_pay_interface
			})

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MALL_SETTINGS_NAV,
			'pay_interfaces': pay_interfaces,
			'pay_interface': pay_interface,
		})
		return render_to_response('mall/editor/edit_pay_interface.html', c)


########################################################################
# delete_pay_interface: 删除支付接口
########################################################################
@login_required
def delete_pay_interface(request, pay_interface_id):
	pay_interface = PayInterface.objects.get(id=pay_interface_id)
	if pay_interface.type == PAY_INTERFACE_ALIPAY:
		UserAlipayOrderConfig.objects.filter(id=pay_interface.related_config_id).delete()
	elif pay_interface.type == PAY_INTERFACE_TENPAY:
		UserTenpayOrderConfig.objects.filter(id=pay_interface.related_config_id).delete()
	elif pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
		UserWeixinPayOrderConfig.objects.filter(id=pay_interface.related_config_id).delete()
	else:
		pass

	# 更新商品的货到付款
	if pay_interface.type == PAY_INTERFACE_COD:
		module_api.update_products_pay_interface_cod(request.user.id)

	PayInterface.objects.filter(id=pay_interface_id).delete()
	
	return HttpResponseRedirect('/mall/editor/mall_settings/')


########################################################################
# active_pay_interface: 启用支付接口
########################################################################
@login_required
def active_pay_interface(request, pay_interface_id):
	PayInterface.objects.filter(id=pay_interface_id).update(is_active=True)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# inactive_pay_interface: 停用支付接口
########################################################################
@login_required
def inactive_pay_interface(request, pay_interface_id):
	pay_interface = __get_pay_inferface_by_id(pay_interface_id)
	# 更新商品的货到付款
	if pay_interface and pay_interface.type == PAY_INTERFACE_COD:
		module_api.update_products_pay_interface_cod(request.user.id)

	PayInterface.objects.filter(id=pay_interface_id).update(is_active=False)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
# MODULE END: postagesettings
# Termite GENERATED END: views