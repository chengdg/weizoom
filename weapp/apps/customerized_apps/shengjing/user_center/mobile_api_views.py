# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil

from watchdog.utils import watchdog_fatal, watchdog_error

from shengjing.models import *

import qrcode_util
import util

from apps.register import mobile_api

import apps.customerized_apps.shengjing.study_plan.shengjing_api_view as shengjing_api

########################################################################
#send_captcha: 发送验证码 old
########################################################################
# @mobile_api(resource='sent_captcha', action='create')
'''
def send_captcha(request):
	response = create_response(200)
	data = dict()
	phone_number = request.POST.get('number', None) 
	member_id = request.POST.get('member_id', None) 

	if member_id and Member.objects.filter(id=member_id).count() > 0:
		member = Member.objects.filter(id=member_id)[0]
	else:
		member = None
		
	if phone_number and member:
		if ShengjingBindingMember.is_can_binding(phone_number, member_id, member.webapp_id):
			result,captcha = util.send_phone_msg(phone_number)
			if result and captcha:
				if ShengjingBindingMember.has_record_with_phone_number(phone_number, member.webapp_id):
					ShengjingBindingMember.objects.filter(phone_number=phone_number, webapp_id=member.webapp_id).update(captcha=captcha)
				else:
					ShengjingBindingMember.objects.create(
						phone_number=phone_number,
						captcha=captcha, 
						webapp_id=member.webapp_id)
			else:
				response = create_response(501)
				data['msg'] = u'获取失败，请重试'
				response.data = data
		else:
			response = create_response(501)
			data['msg'] = u'该手机已经注册过'
			response.data = data
	elif member:
		response = create_response(501)
		data['msg'] = u'请输入正确手机号'
		response.data = data
	else:
		response = create_response(501)
		data['msg'] = u'认证失败，请从图文进入微站'
		response.data = data
		return response.get_response()
	
	return response.get_response()
'''

########################################################################
#send_captcha: 发送验证码
########################################################################
@mobile_api(resource='sent_captcha', action='create')
def send_captcha(request):
	response = create_response(200)
	data = dict()
	phone_number = request.POST.get('number', None) 
	member_id = request.POST.get('member_id', None) 

	if member_id and Member.objects.filter(id=member_id).count() > 0:
		member = Member.objects.filter(id=member_id)[0]
	else:
		member = None
		
	if phone_number and member:
		if ShengjingBindingMember.is_can_binding(phone_number, member_id, member.webapp_id):
			#  向盛景发送验证码接口
			items = shengjing_api.mobile_get_captcha(phone_number)
			if items:
				try:
					if int(items.get('Header').get('Code')) == 0:
						if ShengjingBindingMember.has_record_with_phone_number(phone_number, member.webapp_id):
							ShengjingBindingMember.objects.filter(phone_number=phone_number, webapp_id=member.webapp_id).update(captcha='captcha')
						else:
							ShengjingBindingMember.objects.create(
								phone_number=phone_number,
								captcha='captcha', 
								webapp_id=member.webapp_id)
					else:
						response = create_response(501)
						# data['msg'] = u'code:{}, info:{}'.format(items.get('Header').get('Code'), items.get('Header').get('Info'))
						data['msg'] = u'{}'.format(items.get('Header').get('Info'))
						response.data = data	
				except:
					response = create_response(501)
					data['msg'] = u'获取失败，请重试'
					response.data = data
			else:
				response = create_response(501)
				data['msg'] = u'获取失败，请重试'
				response.data = data
		else:
			response = create_response(501)
			data['msg'] = u'该手机已经注册过'
			response.data = data
	elif member:
		response = create_response(501)
		data['msg'] = u'请输入正确手机号'
		response.data = data
	else:
		response = create_response(501)
		data['msg'] = u'认证失败，请从图文进入微站'
		response.data = data
		return response.get_response()
	
	return response.get_response()


########################################################################
#check_captcha: 检查验证码
########################################################################
# @mobile_api(resource='binded_phone', action='create')
'''
def record_binding_phone(request):
	response = create_response(200)
	data = dict()
	phone_number =  request.POST.get('number', None)
	captcha =  request.POST.get('captcha', None)
	member_id =  request.POST.get('member_id', -1)

	if member_id and Member.objects.filter(id=member_id).count() > 0:
		member = Member.objects.filter(id=member_id)[0]
	else:
		member = None

	if member is None:
		response = create_response(500)
		data = dict()
		data['msg'] = u'认证失败，请从图文进入微站'
		response.data = data
	elif phone_number and captcha:
		if ShengjingBindingMember.validated_phone_aptcha(phone_number, captcha, member.webapp_id):
			response = create_response(500)
			data['msg'] = u'验证码无效'
			response.data = data
		elif  ShengjingBindingMember.has_member_with_phone_number(phone_number, member.id, member.webapp_id) is False:
			member = Member.objects.get(id=member_id)
			ShengjingBindingMember.objects.filter(phone_number=phone_number, captcha='captcha', member_id=0, webapp_id = member.webapp_id).update(member_id=member_id)
		else:
			response = create_response(500)
			data['msg'] = u'该手机已经注册过'
			response.data = data
	else:
		response = create_response(500)
		data = dict()
		data['msg'] = u'验证码无效'
		response.data = data
	
	return response.get_response()
'''

########################################################################
#check_captcha: 检查验证码
########################################################################
@mobile_api(resource='binded_phone', action='create')
def record_binding_phone(request):
	response = create_response(200)
	data = dict()
	phone_number =  request.POST.get('number', None)
	captcha =  request.POST.get('captcha', None)
	member_id =  request.POST.get('member_id', -1)

	if member_id and Member.objects.filter(id=member_id).count() > 0:
		member = Member.objects.filter(id=member_id)[0]
	else:
		member = None

	if member is None:
		response = create_response(500)
		data = dict()
		data['msg'] = u'认证失败，请从图文进入微站'
		response.data = data
	elif phone_number and captcha:

		if not ShengjingBindingMember.is_can_binding(phone_number, member_id, member.webapp_id):
			response = create_response(500)
			data['msg'] = u'该手机已经注册过'
			response.data = data

		#  向盛景发送验证码接口
		items = shengjing_api.mobile_get_captcha_verify(phone_number, captcha)
		try:
			if int(items.get('Header').get('Code')) == 0:
				if  ShengjingBindingMember.has_member_with_phone_number(phone_number, member.id, member.webapp_id) is False:
					member = Member.objects.get(id=member_id)
					ShengjingBindingMember.objects.filter(phone_number=phone_number, captcha='captcha', member_id=0, webapp_id = member.webapp_id).update(member_id=member_id)
				else:
					response = create_response(500)
					data['msg'] = u'该手机已经注册过'
					response.data = data
			else:
				response = create_response(500)
				# data['msg'] = u'code:{}, info:{}'.format(items.get('Header').get('Code'), items.get('Header').get('Info'))
				data['msg'] = u'{}'.format(items.get('Header').get('Info'))
				response.data = data	
		except:
			response = create_response(500)
			data['msg'] = u'验证失败，请重试'
			response.data = data
	else:
		response = create_response(500)
		data = dict()
		data['msg'] = u'验证码无效'
		response.data = data
	
	return response.get_response()


########################################################################
# get_member_qrcode_ticket: 获取推广二维码 ticket
########################################################################
from modules.member.util import get_request_member
from modules.member.models import *
def get_member_qrcode_ticket(request):
	member = get_request_member(request)
	if member:
		try:
			ticket, expired_second = get_member_qrcode(request.user_profile.user_id, member.id)
		except:
			ticket, expired_second = None, None
			notify_msg = u"获取微信会员二维码api view失败 cause:\n{}".format(unicode_full_stack())
			watchdog_fatal(notify_msg)
		
		if ticket is None:
			response = create_response(200)
			response.data.qrcode_url = None
			response.data.expired_second = 30
		else:
			response = create_response(200)
			response.data.qrcode_url = get_qcrod_url(ticket)
			response.data.expired_second = expired_second
		return response.get_response()
	else:
		response = create_response(400)
		response.data.qrcode_url = None
		response.data.expired_second = None
		return response.get_response()

weixin_qcrod_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s'
def get_qcrod_url(ticket):
	return 	weixin_qcrod_url % ticket

#######################################################################
#remove_binding_member: 删除绑定会员信息
#######################################################################
@mobile_api(resource='binding_member', action='remove')
def remove_binding_member(request):
	response = create_response(200)
	try:
		if request.member:
			ShengjingBindingMember.objects.filter(member_id=request.member.id).delete()
	except:
		response = create_response(501)

	return response.get_response()

