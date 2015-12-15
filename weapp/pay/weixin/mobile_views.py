# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import time
from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack

from watchdog.utils import *

from mall.models import Order, OrderHasProduct, PayInterface, Product
from account.models import UserWeixinPayOrderConfig, UserProfile
from weixin.user.models import ComponentAuthedAppid

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]

def index(request):
	woid = request.GET.get('woid', None)
	order_id = request.GET.get('order_id', None)
	pay_interface_id = request.GET.get('pay_id', None)
	is_oauthed = ('code' in request.GET)
	if not woid or not order_id or not pay_interface_id:
		return HttpResponse('woid or order_id or pay_interface_id is none')
	
	# 记录支付开始时间
	pay_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	msg = u'weixin pay, stage:[start], order_id:{}, time:{}'.format(order_id, pay_start_time)
	watchdog_info(msg)
	
	# 获取支付参数开始时间
	get_pay_params_start_time = int(time.time() * 1000)
	
	data= {}
	try:
		user_profile = UserProfile.objects.get(user_id=woid)
		
		pay_interface = PayInterface.objects.get(id=pay_interface_id)
		weixin_pay_config = UserWeixinPayOrderConfig.objects.get(id=pay_interface.related_config_id)
		order = Order.objects.get(order_id=order_id)
		try:
			component_authed_appid = ComponentAuthedAppid.objects.filter(authorizer_appid=appid, user_id=woid)[0]
			component_info = component_authed_appid.component_info
			component_appid = component_info.app_id
		except:
			component_appid = ''
		data['component_appid'] = component_appid
		data['app_id'] = weixin_pay_config.app_id
		data['partner_id'] = weixin_pay_config.partner_id
		data['partner_key'] = weixin_pay_config.partner_key
		data['paysign_key'] = weixin_pay_config.paysign_key
		data['app_secret'] = weixin_pay_config.app_secret
		data['pay_version'] = weixin_pay_config.pay_version
		data['total_fee_display'] = order.final_price
		data['total_fee'] = int(order.final_price * 100)	
		if data['pay_version'] == 0 or (bool(is_oauthed) and data['pay_version'] != 0):
			product_ids = [r.product_id for r in OrderHasProduct.objects.filter(order_id=order.id)]
			product_names = ','.join([product.name for product in Product.objects.filter(id__in=product_ids)])
			if len(product_names) > 127:
				product_names = product_names[:127]
			
			if order.edit_money:
				data['order_id'] = '{}-{}'.format(order_id, str(order.edit_money).replace('.','').replace('-',''))
			else:
				data['order_id'] = order_id
			data['domain'] = user_profile.host
			data['webapp_owner_id'] = woid
			data['pay_interface_type'] = pay_interface.type
			data['pay_interface_related_config_id'] = pay_interface.related_config_id
			data['product_names'] = product_names
			data['user_ip'] = request.META['REMOTE_ADDR']
			data['hide_non_member_cover'] = True
			data['callback_module'] = request.POST.get('callback_module', None)
	except:
		print unicode_full_stack()
		error_msg = u'weixin pay, stage:[get pay params], result:\n{}, exception:\n{}'.format(data, unicode_full_stack())
		watchdog_error(error_msg)
	
	# 支付参数获取结束时间
	get_pay_params_end_time = int(time.time() * 1000)
	msg = u'weixin pay, stage:[get pay params], order_id:{}, consumed:{}ms, result:\n{}'.format(order_id, (get_pay_params_end_time - get_pay_params_start_time), data)
	watchdog_info(msg)
	
	c = RequestContext(request, data)
	if data['pay_version'] == 0:
		return render_to_response('%s/index.html' % TEMPLATE_DIR, c)
	else:
		return render_to_response('%s/index_v3.html' % TEMPLATE_DIR, c)
	