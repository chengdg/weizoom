# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth

from watchdog.utils import watchdog_fatal, watchdog_error

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from models import *
from util import *

########################################################################
# edit_member_qrcode_settings: 编辑/新建会员二维码
########################################################################
@login_required
def edit_member_qrcode_settings(request):
	id = int(request.POST.get('id', 0))
	reward = request.POST.get('reward', '')
	detail = request.POST.get('detail', '').strip()
	
	if reward == '':
		response = create_response(400)
		return response.get_response()

	if reward == '1':
		prize_source = request.POST.get('prize_source|0', '')
		prize_type = request.POST.get('prize_type|0', '')

		if prize_source == '' or prize_type == '':
			response = create_response(400)
			return response.get_response()

		if id:
			MemberQrcodeSettings.objects.filter(id=id).update(award_member_type=int(reward), detail=detail)
			MemberQrcodeAwardContent.objects.filter(member_qrcode_settings_id=id).delete()
			MemberQrcodeAwardContent.objects.create(member_qrcode_settings_id=id,
													award_type=prize_type, 
													award_content=prize_source)
		else:
			member_qrcode_settings = MemberQrcodeSettings.objects.create(owner=request.user, 
																		award_member_type=int(reward), 
																		detail=detail)
			
			MemberQrcodeAwardContent.objects.create(member_qrcode_settings=member_qrcode_settings, 
													award_type=prize_type, 
													award_content=prize_source)
	
	elif reward == '0':
		level2info = {}
	
		for key in request.POST:
			if not key.startswith('prize_'):
				continue

			key_name, level = key.split('|')
			value = request.POST[key]
			
			if level in level2info :
				level2info[level][key_name] = value
			else:
				level2info[level] = {key_name: value}
		
		if id:
			MemberQrcodeSettings.objects.filter(id=id).update(award_member_type=int(reward), detail=detail)
		else:
			id = MemberQrcodeSettings.objects.create(
				owner=request.user, 
				award_member_type=int(reward), 
				detail=detail).id
		
		MemberQrcodeAwardContent.objects.filter(member_qrcode_settings_id=id).delete()
		for level in level2info.keys():
			prize_info = level2info[level]
			MemberQrcodeAwardContent.objects.create(
				member_qrcode_settings_id=id,
				member_level=level,
				award_type=prize_info['prize_type'], 
				award_content=prize_info['prize_source'])

	response = create_response(200)
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
			ticket, expired_second = get_member_qrcode(request.project.owner_id, member.id)
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