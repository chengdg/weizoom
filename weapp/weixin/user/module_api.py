# -*- coding: utf-8 -*-

__author__ = 'bert'

from account.social_account.models import SocialAccount
from core.exceptionutil import full_stack, unicode_full_stack
from watchdog.utils import watchdog_info, watchdog_error
from weixin.user.models import *

def get_mp_head_img(user_id):
	if ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id).count() > 0:
		authed_appid = ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id)[0]
		if authed_appid.head_img:
			return authed_appid.head_img
		else:
			return None
	else:
		return None

def get_mp_qrcode_img(user_id):
	if ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id).count() > 0:
		authed_appid = ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id)[0]
		if authed_appid.qrcode_url:
			return authed_appid.qrcode_url
		else:
			return None
	else:
		return None


def get_mp_nick_name(user_id):
	if ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id).count() > 0:
		authed_appid = ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id)[0]
		if authed_appid.nick_name:
			return authed_appid.nick_name
		else:
			return None
	else:
		return None

def get_mp_info(user_id):
	if ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id).count() > 0:
		return ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=user_id)[0]
	else:
		return None

def authed_appid(user_id):
	try:
		return ComponentAuthedAppid.objects.get(user_id=user_id)
	except :
		return None

def get_all_active_mp_user_ids():
	try:
		return [o.user_id for o in ComponentAuthedAppid.objects.filter(is_active=True)]
	except:
		return None
