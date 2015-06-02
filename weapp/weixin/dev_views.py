# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import os
import json
import hashlib
from core.jsonresponse import create_response

from BeautifulSoup import BeautifulSoup

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.test import Client

from weixin.user.models import WeixinUser

########################################################################
# create_signature: 接入公众平台
########################################################################
def create_signature(request):
	token = request.GET['token']
	timestamp = '1000'
	nonce = 'nonce'

	items = [token, timestamp, nonce]
	items.sort()
	real_signature = hashlib.sha1(''.join(items)).hexdigest()

	response = create_response(200)
	response.data = {
		'timestamp': timestamp,
		'nonce': nonce,
		'signature': real_signature,
		'token': token
	}

	return response.get_response()

########################################################################
# register: 接入公众平台
########################################################################
def register(request):
	c = RequestContext(request, {})
	return render_to_response('mp_register_form.html', c)

def create_dummy_weixinuser(webapp_id, username):
	return WeixinUser.objects.create(
		username = username,
		webapp_id = webapp_id,
		weixin_user_nick_name = '',
		weixin_user_remark_name = '',
		weixin_user_icon = ''
		)

def create_message_to_mp(request):
	if hasattr(request, 'user_profile') and request.user_profile:
		webapp_id = request.user_profile.webapp_id
	else:
		webapp_id = request.GET['to_user_name']
	from_weixin_user_name = request.GET['from_user_name']

	try:
		from_weixin_user = WeixinUser.objects.get(username=from_weixin_user_name)
	except:
		from_weixin_user = create_dummy_weixinuser(webapp_id, from_weixin_user_name)

	response = create_response(200)
	response.data = {
		'fakeId': from_weixin_user.fake_id
	}

	return response.get_response()