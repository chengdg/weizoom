# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random

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

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_debug
from core.exceptionutil import unicode_full_stack

from core.alipay.alipay_submit import *
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
from core.alipay.alipay_notify import AlipayNotify
from core.alipay.alipay_submit import AlipaySubmit
from account.models import UserProfile
from market_tools.tools.coupon.util import consume_coupon
from account.views import save_base64_img_file_local_for_webapp
from models import *


########################################################################
# join_activity:
########################################################################
def join_activity(request):
	weapp_user = request.webapp_user
	member = weapp_user.get_member_by_webapp_user_id(weapp_user.id)
	activity_id = request.POST['activity_id']

	try:
		activity = Activity.objects.get(id=activity_id)
	except:
		response = create_response(500)
		response.errMsg = u'该活动不存在'
		response.innerErrMsg = full_stack()
		return response.get_response()
		
	if not activity.is_non_member:
		if member is None:
			response = create_response(500)
			response.errMsg = u'您还不是会员'
			return response.get_response()

	username = ''
	phone_number = ''
	if request.POST:
		try:
			response = create_response(200)
			if activity.is_enable_offline_sign:
				sign_code = _create_activity_sign_code(request.webapp_user.id, activity.id)
				ActivityUserCode.objects.create(
					owner_id = request.webapp_owner_id,
					activity = activity,
					webapp_user_id = weapp_user.id,
					sign_code = sign_code
				)
				response.data.sign_code = sign_code
			items = ActivityItem.objects.filter(activity=activity)
			for item in items:
				input_name = '{}-{}'.format(item.id, item.type)
				if item.type == ACTIVITYITEM_TYPE_IMAGE:
					file = request.POST[input_name]
					if file:
						value = save_base64_img_file_local_for_webapp(request, file)
					else:
						value = ''
				else:
					value = request.POST.get(input_name, '')
	
				if item.title == u'姓名':
					username = value
				if item.title == u'手机号':
					phone_number = value

				ActivityItemValue.objects.create(
					owner_id = request.webapp_owner_id,
					webapp_user_id= weapp_user.id,
					item = item,
					activity = activity,
					value = value
				)
			try:
				#是否开启线下签到
				is_enable_offline_sign = activity.is_enable_offline_sign
				if not is_enable_offline_sign and member:
					member.update_member_info(username, phone_number)
					#给予奖励
					#无奖励
					if activity.prize_type == -1:
						pass
					#优惠券
					elif activity.prize_type == 1:
						rule_id = activity.prize_source
						# coupons = create_coupons(activity.owner, rule_id, 1, member.id)
						consume_coupon(activity.owner.id, rule_id, member.id)
					#积分
					elif activity.prize_type == 3:
						prize_detail = activity.prize_source
						#增加积分
						member.consume_integral(-int(prize_detail), u'参加活动，获得积分')
			except:
				ActivityItemValue.objects.filter(owner_id = request.webapp_owner_id, activity=activity, webapp_user_id=weapp_user.id).delete()
				ActivityUserCode.objects.filter(
					owner_id = request.webapp_owner_id,
					activity = activity,
					webapp_user_id = weapp_user.id,
				).delete()
				raise IOError
		except:
			notify_msg = u"活动报名失败, cause:\n{}".format(unicode_full_stack())
			watchdog_fatal(notify_msg)
			response = create_response(500)
			response.errMsg = u'提交错误'
			response.innerErrMsg = full_stack()
			return response.get_response()
	else:
		response = create_response(500)
		response.errMsg = u'is not POST method'

	return response.get_response()


########################################################################
# _create_activity_sign_code: 随机生成一个签到码
########################################################################
def _create_activity_sign_code(owner_id, activity_id):
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	code = '%03d%04d%s' % (owner_id, activity_id, ''.join(random.sample(random_args_value, 6)))
	return code

########################################################################
# join_activity_ph:
########################################################################
def join_activity_ph(request):
	print '1111111111111111111111111===========post'
	weapp_user = request.webapp_user
	activity_id = request.POST['activity_id']
	try:
		activity = Activity.objects.get(id=activity_id)
	except:
		response = create_response(500)
		response.errMsg = u'该活动不存在'
		return response.get_response()
	items = ActivityItem.objects.filter(activity=activity)
	ids = ''
	for item in items:
		input_name = '{}-{}'.format(item.id, item.type)
		if item.type == ACTIVITYITEM_TYPE_IMAGE:
			file = request.POST[input_name]
			if file:
				value = save_base64_img_file_local_for_webapp(request, file)
			else:
				value = ''
		else:
			value = request.POST.get(input_name, '')

		valueobj = ActivityItemValue.objects.create(
			owner_id = request.webapp_owner_id,
			webapp_user_id= weapp_user.id,
			item = item,
			activity = activity,
			value = value
		)
		ids = ids+','+str(valueobj.id)
	response = create_response(200)
	response.data.member_id = weapp_user.id
	response.data.ids = ids
	return response.get_response()

