# -*- coding: utf-8 -*-

import time
from datetime import datetime
import urllib, urllib2
import json
import math

from django.conf import settings

from core.jsonresponse import create_response
from watchdog.utils import *
from core.exceptionutil import full_stack, unicode_full_stack
from modules.member.models import *
from modules.member.util import *
from weixin.user.models import WeixinUser, get_token_for
from util import send_phone_msg

def send_captcha(request):
	response = create_response(200)
	data = dict()
	phone_number = request.POST.get('phone_number', '').strip()
	sessionid = request.COOKIES.get('sessionid', 'unknow')
	if hasattr(request, 'member') and request.member:
		member_id = request.member.id
	else:
		member_id = -1
	"""
		如果独立wap站，注册是没有会员信息，则需要做修改
	"""
	member_info = MemberInfo.get_member_info(member_id=member_id)

	if member_info.is_binded is False:
		if MemberInfo.is_can_binding(phone_number, member_id, request.user_profile.webapp_id):
			if request.webapp_owner_info.mpuser_preview_info and request.webapp_owner_info.mpuser_preview_info.name:
				result,captcha = send_phone_msg(phone_number, request.webapp_owner_info.mpuser_preview_info.name)
			else:
				result,captcha = send_phone_msg(phone_number)
				
			if result and captcha:
				#if member_id > 0:
					member_info.session_id = sessionid
					member_info.captcha = captcha
					member_info.phone_number = phone_number
					member_info.save()
				# else:
				# 	openid = "%s_%s" % phone_number,webapp_id
				# 	token = get_token_for(webapp_id, openid)
				# 	social_account = member_util.create_social_account(webapp_id, openid, token, 3)
				# 	member = member_util.create_member_by_social_account(user_profile, social_account)
				# 	MemberInfo.objects.create(
				# 		member = member,
				# 		name = '',
				# 		session_id = sessionid,
				# 		captcha = captcha,
				# 		phone_number = phone_number
				# 	)
			else:
				response = create_response(501)
				data['msg'] = u'验证码获取失败，请重试'
				response.data = data
		else:
			response = create_response(502)
			data['msg'] = u'该手机已经绑定'
			response.data = data
	else:
		response = create_response(504)
		data['msg'] = u'会员已经绑定过手机'
		response.data = data
		return response.get_response()
	
	return response.get_response()

def binding_phone(request):
	response = create_response(200)
	data = dict()
	phone_number = request.POST.get('phone_number', '').strip()
	code = request.POST.get('code', '').strip()
	sessionid = request.COOKIES.get('sessionid', 'unknow')
	if hasattr(request, 'member') and request.member:
		member_id = request.member.id
	else:
		member_id = -1
	"""
		如果独立wap站，注册是没有会员信息，则需要做修改
	"""
	member_info = MemberInfo.get_member_info(member_id=member_id)
	if member_info.is_binded is False:
		if MemberInfo.is_can_binding(phone_number, member_id, request.user_profile.webapp_id):
			if MemberInfo.objects.filter(member_id=member_id, session_id=sessionid, phone_number=phone_number, captcha=code, is_binded=False).count() > 0:
				 MemberInfo.objects.filter(member_id=member_id, session_id=sessionid, phone_number=phone_number, captcha=code).update(is_binded=True, binding_time=datetime.now())
			else:
				response = create_response(501)
				data['msg'] = u'手机验证码错误，请重新输入'
				response.data = data
		else:
			response = create_response(502)
			data['msg'] = u'该手机已经注册过'
			response.data = data
	else:
		response = create_response(503)
		data['msg'] = u'会员已经绑定过手机'
		response.data = data
		return response.get_response()
	
	return response.get_response()

import hashlib
from utils.url_helper import remove_querystr_filed_from_request_url
def record_shared_url(request):
	member = request.member

	if member:
		title = request.POST.get('title', '')
		shared_url =  request.POST.get('link','')
		if shared_url.startswith('http'):
			shared_url = shared_url[shared_url.find(settings.DOMAIN+len(settings.DOMAIN):]

		if shared_url:
			shared_url = remove_querystr_filed_from_request_url(shared_url, 'from')
			shared_url = remove_querystr_filed_from_request_url(shared_url, 'isappinstalled')
			shared_url_digest = hashlib.md5(shared_url).hexdigest()

			print '=======================shareurl=', shared_url
			if MemberSharedUrlInfo.objects.filter(member=member, shared_url_digest=shared_url_digest).count() == 0:
				MemberSharedUrlInfo.objects.create(
					member = member,
					shared_url = shared_url,
					pv = 0,
					shared_url_digest = shared_url_digest,
					title=title
					)
	else:
		print 'no-------------------member'
	response = create_response(200)
	return response.get_response()