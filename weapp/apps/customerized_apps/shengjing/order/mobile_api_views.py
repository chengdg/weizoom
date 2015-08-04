# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

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

from core.alipay.alipay_submit import *
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
from core.alipay.alipay_notify import AlipayNotify
from core.alipay.alipay_submit import AlipaySubmit
from account.models import UserProfile

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert, watchdog_fatal

from modules.member import module_api as member_module_api

from shengjing.crm_api import api_views as crm_apis
from shengjing.user_center.util import get_binding_info_by_member

from apps.register import mobile_api

#订单状态
ORDER_USING = 0	#使用中
ORDER_USED = 1 #已使用
ORDER_ALL = 2 #全部

BILL_UNUSED = 0	#未开发票
BILL_USED = 1	#已开发票

################################################
# 获取账单明细
################################################
@mobile_api(resource='order_list', action='get')
def list_order(request):
	company = request.GET.get('company')

	#得到会员信息
	member = None
	if hasattr(request, 'member'):
		member = request.member
	else:
		member_id = request.GET.get('member_id', '')
		try:
			member = member_module_api.get_member_by_id(int(member_id))
		except:
			response = create_response(500)
			response.errmsg = u'获取不到会员信息'
			return response.get_response()
	binding_member, member_info = get_binding_info_by_member(member)

	if not crm_apis.is_leader(member_info.phone_number, company):
		response = create_response(200)
		data = {}
		data['is_leader'] = False
		data['info'] = u'您尚未购买盛景课程<br/>或者您不是企业决策人'
		response.data = data
		return response.get_response()
			
	order_status = request.GET.get('status', ORDER_USING)	#订单状态
	

	#获取人次卡
	cards = None
	try:
		cards = crm_apis.get_time_person_cards(member_info.phone_number, company, int(order_status))
	except:
		alert_message = u'获取时间卡信息失败.\n couse: {}'.format(unicode_full_stack())
		watchdog_alert(alert_message)

	has_orders = True
	if cards == None or len(cards) == 0:
		has_orders = False

	response = create_response(200)
	data = {}
	data['has_orders'] = has_orders
	data['is_leader'] = True
	data['cards'] = cards
	response.data = data
	return response.get_response()