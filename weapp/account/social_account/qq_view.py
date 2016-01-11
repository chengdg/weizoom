# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
try:
    import Image
except:
    from PIL import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from core.jsonresponse import create_response, JsonResponse
from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal
from core.exceptionutil import full_stack
from core.exceptionutil import unicode_full_stack
from account.social_account.weibo_view import get_shop_name_and_last_url, save_social_account, save_session, set_user_profile


#===============================================================================
# login_redirect : 跳转到QQ登陆页面
#===============================================================================
from core.qq.qq_authorize import QQAuthorize
def login_redirect(request, webapp_id):
	authorize = QQAuthorize(request)
	url = authorize.get_Http_authorize_url()
	return HttpResponseRedirect(url)


#===============================================================================
# callback_handler : 回调函数
#===============================================================================
from core.qq.qq_access_token import QQAccessToken
from core.qq.qq_open_id import QQOpenID
def login_callback_handler(request):
	code = request.GET.get('code', None)
	state = request.GET.get('state', None)
	new_url = '/'
	response = HttpResponseRedirect(new_url)
	watchdog_info(u'从QQ登陆回调函数，code={}，state={}'.format(code, state))
	if code:
		try:
			# 获取webapp_id 和 登陆后跳转地址
			webapp_id, new_url = get_shop_name_and_last_url(state)
			request = set_user_profile(request, webapp_id)
			# 获取 access_token
			qq_get_token = QQAccessToken(request, code)
			data = qq_get_token.get_access_token_data()
			token = data.get('access_token')

			# 获取 openId
			qq_get_open_id = QQOpenID(request, token)
			data = qq_get_open_id.get_open_id_data()
			openid = data.get('openid')

			# 创建 social_account
			social_account = save_social_account(openid, token, SOCIAL_PLATFORM_QQ, webapp_id)
			response = HttpResponseRedirect(new_url)
			save_session(response, social_account)
		except:
			watchdog_error(u'从QQ登陆回调函数错误，error={}'.format(unicode_full_stack()))
	else:
		response = HttpResponseRedirect(new_url)
		notify_message = u'从QQ登陆回调函数错误，没有code{}'.format(request)
		watchdog_fatal(notify_message)

	return response

