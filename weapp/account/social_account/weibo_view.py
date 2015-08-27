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
from watchdog.utils import watchdog_error, watchdog_info, watchdog_fatal
from core.exceptionutil import full_stack
from core.exceptionutil import unicode_full_stack
from modules.member.member_settings import SOCIAL_ACCOUNT_TOKEN_SESSION_KEY
import hashlib
from account.models import UserProfile


#===============================================================================
# login_redirect : 跳转到Weibo登陆页面
#===============================================================================
from core.weibo.weibo_authorize import WeiboAuthorize
def login_redirect(request, webapp_id):
	authorize = WeiboAuthorize(request)
	url = authorize.get_Http_authorize_url()
	return HttpResponseRedirect(url)


#===============================================================================
# callback_handler : 回调函数
#===============================================================================
from core.weibo.weibo_access_token import WeiboAccessToken
from core.weibo.weibo_token_info import WeiboTokenInfo
from core.weibo.weibo_user_info import WeiboUserInfo
def login_callback_handler(request):
	code = request.GET.get('code', None)
	state = request.GET.get('state', None)
	new_url = '/'
	if code:
		# 获取shop_name 和 登陆后跳转地址
		webapp_id, new_url = get_shop_name_and_last_url(state)
		request = set_user_profile(request, webapp_id)
		# 获取 access_token
		weibo_get_token = WeiboAccessToken(request, code)
		data = weibo_get_token.get_access_token_data()
		token = data.get('access_token')

		# 获取 openId
		weibo_get_open_id = WeiboTokenInfo(request, token)
		data = weibo_get_open_id.get_open_id_data()
		uid = data.get('uid')

		# 创建 social_account
		social_account = save_social_account(uid, token, SOCIAL_PLATFORM_SINAWEIBO, webapp_id)
		response = HttpResponseRedirect(new_url)
		save_session(response, social_account)
	else:
		response = HttpResponseRedirect(new_url)
		notify_message = u'从微博登陆回调函数错误，没有code{}'.format(request)
		watchdog_fatal(notify_message)

	return response


def save_social_account(openid, token, platform, shop_name):
	social_accounts = SocialAccount.objects.filter(openid=openid, shop_name=shop_name)
	if social_accounts.count() > 0:
		social_account = social_accounts[0]
		social_account.access_token = token
		social_account.save()
	else:
		social_account = SocialAccount.objects.create(
			openid = openid, 
			access_token = token, 
			token = _get_token_for_weibo_account(openid, shop_name),
			platform = platform, 
			shop_name = shop_name
			)

	watchdog_info(u"weibo login success save_social_account shop_name: %s, token: %s, "
	                          u"openid: %s, platform:%s, shop_name: %s" % (shop_name, token, openid, platform, shop_name))
	return social_account

def _get_token_for_weibo_account(openid, shop_name):
	return compile_md5("{}_{}".format(shop_name, openid))

def save_session(response, social_account):
	sign = '%s' % social_account.token
	response.set_cookie(get_session_name(), sign, max_age=3600*24)
	watchdog_info(u"weibo login success save_session sign: %s, name: %s" % (sign, get_session_name()))


def get_session_name():
	return SOCIAL_ACCOUNT_TOKEN_SESSION_KEY


def compile_md5(sign):
	return hashlib.md5(sign).hexdigest()


def parse_md5(sign):
	pass


def get_shop_name_and_last_url(state):
	shop_name="3180"
	url = '/'
	try:
		state = state.split('~')
		shop_name = state[0]
		url = state[1]
	except:
		watchdog_error(u'get_shop_name_and_last_url错误，state={}'.format(state))
	return shop_name, url


def set_user_profile(request, webapp_id):
	user_profiles = UserProfile.objects.filter(shop_name=webapp_id)
	if user_profiles.count() > 0:
		request.user_profile = user_profiles[0]
	return request


class Social():
	def __init__(self):
		pass
