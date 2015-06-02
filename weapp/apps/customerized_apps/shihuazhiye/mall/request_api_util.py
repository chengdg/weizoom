# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import copy

from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core import chartutil
from watchdog.utils import watchdog_info, watchdog_error
from core.exceptionutil import full_stack, unicode_full_stack
from core.alipay.alipay_submit import *
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
from account.models import UserProfile
from modules.member.models import *
from modules.member.util import *
import httplib
from webapp.modules.mall.models import *
from webapp.modules.mall import util as mall_util
from webapp.modules.mall import signals as mall_signals
from webapp.modules.mall import request_api_util
from modules.member import util as member_util
from modules.member import module_api as member_module_api
from account.models import *

from tools.regional.models import City, Province, District
from tools.regional.views import get_str_value_by_string_ids
from core.send_order_email_code import *
from market_tools.tools.weizoom_card import models as weizoom_card_model
import util as shihuazhiye_util

########################################################################
#save_order: 保存订单
########################################################################
def save_order(request):
	#request.POST['ship_address'] = request.POST['post'] + ',' + request.POST['ship_address'] + ',' + request.POST['recommend']
	response = request_api_util.save_order(request)
	#print response
	#print response.content.data
	new_response = json.loads(response.content)
	#print response
	data = new_response['data']
	if data.get('order_id', None):
		order_id = data['order_id']
		order = Order.objects.get(order_id=order_id)
		order.ship_address = order.ship_address+','+request.POST['post']+','+request.POST['recommend']
		order.save()
	return response


########################################################################
# pay: 订单支付api
########################################################################
def pay_order(request):
	order_to_pay = None	
	profile = request.user_profile
	webapp_user = request.webapp_user

	order_id = request.POST.get('order_id', None)
	if order_id is None:
		response = create_response(400)
		response.errMsg = u'订单不存在'
		return response.get_response()

	try:
		order_to_pay = Order.objects.get(id=order_id)
	except:
		response = create_response(500)
		response.errMsg = u'获取订单失败'
		response.innerErrMsg = full_stack()
		return response.get_response()
	
	interface_id = int(request.POST.get('interface_id', 0))
	pay_interface = PayInterface.objects.get(id=interface_id)
	pay_url = shihuazhiye_util.pay(pay_interface, order_to_pay, request.webapp_owner_id)
	if pay_url:
		response = create_response(200)
		response.data.url = pay_url
	else:
		response = create_response(500)
		response.errMsg = u'支付失败'
		stack = unicode_full_stack()
		response.innerErrMsg = full_stack()
	
	return response.get_response()
	

WAIT_BUYER_PAY = 'WAIT_BUYER_PAY'
WAIT_SELLER_SEND_GOODS='WAIT_SELLER_SEND_GOODS'
TRADE_FINISHED = 'TRADE_FINISHED'
TRADE_CLOSED = 'TRADE_CLOSED'
WAIT_BUYER_CONFIRM_GOODS = 'WAIT_BUYER_CONFIRM_GOODS'
