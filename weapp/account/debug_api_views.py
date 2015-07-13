# -*- coding: utf-8 -*-

__author__ = 'chuter'

#import urllib2
#import os
from datetime import timedelta, datetime

#from django.contrib.auth.decorators import login_required
from django.conf import settings
#from django.shortcuts import render_to_response
#from django.contrib import auth

from models import *
from core.jsonresponse import create_response, decode_json_str
#from core.exceptionutil import unicode_full_stack
#from account.models import UserProfile
#from account.social_account.models import SocialAccount
#from core.wxapi import get_weixin_api

from watchdog.utils import watchdog_error, watchdog_alert

def log_api_error(request):
	api = request.POST.get('api', '')
	error = request.POST.get('error', '')

	if settings.DUMP_DEBUG_MSG:
		print 'api: ', api
		print 'error: ', error

	try:
		user_id = request.user.id
	except:
		user_id = 0

	if len(error.strip()) > 0:
		#TODO: 加入watchdog操作
		watchdog_error(u'api:{},\nerror:\n{}'.format(api, error), 'API', str(user_id))

	return create_response(200).get_response()


def log_js_error(request):
	content = request.POST.get('content', '')
	message = request.POST.get('message', '')
	user_agent = request.META['HTTP_USER_AGENT']
	try:
		user_id = request.user.id
	except:
		user_id = 0

	try:
		member_info = u'\nrequest.member.id = {}\n\n'.format(request.member.id)
	except:
		member_info = u''

	watchdog_alert(u"***** Client Javascript Exception (%s) *****\n%s[UserAgent]: %s\n%s" % (message, member_info, user_agent, content),
		'JS', str(user_id))

	return create_response(200).get_response()