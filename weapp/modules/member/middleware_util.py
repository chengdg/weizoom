# -*- coding: utf-8 -*-

__author__ = 'bert'

import time
import os
import qrcode

from django.conf import settings
from django.db.models import F

from core.exceptionutil import full_stack, unicode_full_stack
from core.wxapi import get_weixin_api

from utils.uuid import uniqueid
from utils.string_util import byte_to_hex
from account.social_account import account_info as social_account_info_util

from models import *
from weixin.user.models import WeixinUser
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN, SOCIAL_PLATFORM_QQ, SOCIAL_PLATFORM_SINAWEIBO
from account.social_account.account_info import get_social_account_info
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from webapp.modules.mall.models import Order

import member_settings

def replace_fmt_in_request_url(request, new_followed_member_token=None):
	orig_full_path = request.get_full_path()

	if new_followed_member_token is None:
		return orig_full_path

	query_parts = orig_full_path.split('&')
	for index, query_part in enumerate(query_parts):
		if query_part.find(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD) >= 0:
			key_and_value = query_part.split('=')
			new_query_part = "{}={}".format(key_and_value[0], new_followed_member_token)
			query_parts[index] = new_query_part
			break

	return '&'.join(query_parts)


import member_info_util
import member_identity_util
import member_relation_util

def get_request_member(request):
	#假设经过了MemberSessionMiddleware中间件的处理
	return member_info_util.get_request_member(request)

def get_request_social_account(request):
	#假设经过了RequestSocialAccountSessionMiddleware中间件的处理
	return member_info_util.get_request_social_account(request)

def get_fmt_from_url(request):
	return member_info_util.get_followed_member_token_from_url_querystr(request)