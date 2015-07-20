# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf import settings

from models import *
from weixin.user.models import WeixinUser, DEFAULT_ICON

from core.qq.qq_user_info import QQUserInfo
from core.weibo.weibo_user_info import WeiboUserInfo
from core.exceptionutil import unicode_full_stack
from modules.member.models import SEX_TYPE_UNKOWN
from watchdog.utils import watchdog_fatal, watchdog_error

from utils.string_util import byte_to_hex, hex_to_byte

class SocialAccountInfo(object):
	def __init__(self, nickname, head_img, sex=SEX_TYPE_UNKOWN, subscribe=False, country='', province='', city=''):
		self.nickname = nickname
		self.head_img = head_img
		self.sex = sex
		self.country = country
		self.province = province
		self.city = city
		self.is_subscribed = subscribe

def _get_local_qq_account_info(social_account):
	return QQAccountInfo.objects.get(openid=social_account.openid)

def _save_local_qq_account_info(social_account, social_account_info):
	return QQAccountInfo.objects.create(nickname=social_account_info.nickname,
		head_img=social_account_info.head_img, openid=social_account.openid)

def _update_local_qq_account_info(social_account, social_account_info):
	QQAccountInfo.objects.filter(openid=social_account.openid).update(
		nickname = social_account_info.nickname,
		head_img = social_account_info.head_img
	)

def _get_qq_account_info_via_api(user_profile, social_account):
	try:
		#通过api去实时获取
		qq_user_info = QQUserInfo(user_profile, social_account)
		nickname, head_img = qq_user_info.get_qq_account_info()
		return SocialAccountInfo(nickname, head_img)
	except:
		return None

def get_qq_account_info(user_profile, social_account, can_use_local=True):
	qq_account_info = None

	if can_use_local:
		try:
			qq_account_info = _get_local_qq_account_info(social_account)
		except:
			notify_message = u"从本地获取QQ账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_error(notify_message)

	if qq_account_info and qq_account_info.head_img and qq_account_info.nickname:
		return qq_account_info

	#需要进行方式微博api进行实时获取
	qq_account_info_via_api = _get_qq_account_info_via_api(user_profile, social_account)
	if qq_account_info and qq_account_info_via_api:
		try:
			_update_local_qq_account_info(social_account, qq_account_info_via_api)
		except:
			notify_message = u"更新本地QQ账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_fatal(notify_message)

	elif qq_account_info_via_api:
		try:
			_save_local_qq_account_info(social_account, qq_account_info_via_api)
		except:
			notify_message = u"添加本地QQ账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_fatal(notify_message)

	return qq_account_info_via_api


def _get_local_sina_weibo_account_info(social_account):
	return SinaWeiboAccountInfo.objects.get(openid=social_account.openid)

def _save_local_sina_weibo_account_info(social_account, social_account_info):
	return SinaWeiboAccountInfo.objects.create(nickname=social_account_info.nickname,
		head_img=social_account_info.head_img, openid=social_account.openid)

def _update_local_sina_weibo_account_info(social_account, social_account_info):
	SinaWeiboAccountInfo.objects.filter(openid=social_account.openid).update(
		nickname = social_account_info.nickname,
		head_img = social_account_info.head_img
	)

def _get_sina_weibo_account_info_via_api(user_profile, social_account):
	try:
		#通过api去实时获取
		weibo_user_info = WeiboUserInfo(user_profile, social_account)
		nickname, head_img = weibo_user_info.get_weibo_account_info()
		return SocialAccountInfo(nickname, head_img)
	except:
		return None

def get_sina_weibo_account_info(user_profile, social_account, can_use_local=True):
	weibo_account_info = None

	if can_use_local:
		try:
			weibo_account_info = _get_local_sina_weibo_account_info(social_account)
		except:
			notify_message = u"从本地获取微博账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_error(notify_message)

	if weibo_account_info and weibo_account_info.nickname and weibo_account_info.head_img:
		return weibo_account_info

	#需要进行方式微博api进行实时获取
	weibo_account_info_via_api = _get_sina_weibo_account_info_via_api(user_profile, social_account)
	if weibo_account_info and weibo_account_info_via_api:
		try:
			_update_local_sina_weibo_account_info(social_account,
				weibo_account_info_via_api)
		except:
			notify_message = u"更新本地微博账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_fatal(notify_message)
	elif weibo_account_info_via_api:
		try:
			_save_local_sina_weibo_account_info(social_account,
				weibo_account_info_via_api)
		except:
			notify_message = u"添加本地微博账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_fatal(notify_message)

	return weibo_account_info_via_api


from account.util import *
from core.wxapi import get_weixin_api
def check_openid_by_api(user_profile, openid):
	mp_user = get_binding_weixin_mpuser(user_profile.user_id)
	if mp_user is None:
		return None

	mpuser_access_token = get_mpuser_accesstoken(mp_user)
	if mpuser_access_token is None:
		return False

	if mp_user.is_certified and mpuser_access_token.is_active:
		weixin_api = get_weixin_api(mpuser_access_token)
		userinfo = weixin_api.get_user_info(openid)

		if hasattr(userinfo, 'errcode'):
			return False
		else:
			return True
	else:
		return False

def _get_weixin_account_info_via_api(user_profile, social_account):
	mp_user = get_binding_weixin_mpuser(user_profile.user_id)
	if mp_user is None:
		return None

	mpuser_access_token = get_mpuser_accesstoken(mp_user)
	if mpuser_access_token is None:
		return None

	if mp_user.is_certified and mpuser_access_token.is_active:
		weixin_api = get_weixin_api(mpuser_access_token)
		userinfo = weixin_api.get_user_info(social_account.openid)

		if userinfo is None:
			return None
		else:
			nickname = ''
			headimgurl=''
			sex = 0
			subscribe = False
			country = ''
			city = ''
			province = ''

			try:
				if hasattr(userinfo, 'nickname'):
					nickname = userinfo.nickname
			
				if hasattr(userinfo, 'headimgurl'):
					headimgurl = userinfo.headimgurl
		
				if hasattr(userinfo, 'sex'):
					sex = userinfo.sex
		
				if hasattr(userinfo, 'subscribe'):
					if str(userinfo.subscribe) == '1':
						subscribe = True

				if hasattr(userinfo, 'city'):
					city = userinfo.city
				
				if hasattr(userinfo, 'province'):
					province = userinfo.province
				
				if hasattr(userinfo, 'country'):
					country = userinfo.country
			except:
				pass
			
			return SocialAccountInfo(nickname, headimgurl, sex, subscribe, country, province, city)
	else:
		return None

def _get_local_weixin_account_info(social_account):
	try:
		weixin_user = WeixinUser.objects.get(username=social_account.openid)
	except:
		weixin_user = WeixinUser.objects.create(
						username = social_account.openid, 
						webapp_id = social_account.webapp_id, 
						nick_name = '', 
						weixin_user_icon = '',
						is_subscribed = False
						)
	
	return SocialAccountInfo(weixin_user.weixin_user_nick_name, weixin_user.weixin_user_icon)

def _update_local_weixin_account_info(social_account, social_account_info):
	WeixinUser.objects.filter(username=social_account.openid).update(
		nick_name = byte_to_hex(social_account_info.nickname),
		weixin_user_icon = social_account_info.head_img
		)

def get_weixin_account_info(user_profile, social_account, can_use_local=True):
	weixin_account_info = None
	# if can_use_local:
	# 	try:
	# 		weixin_account_info = _get_local_weixin_account_info(social_account)
	# 	except:
	# 		notify_message = u"从本地获取微信账号基本信息失败，openid:{}, cause:\n{}".format(
	# 			social_account.openid, unicode_full_stack())
	# 		watchdog_error(notify_message)

	if weixin_account_info and weixin_account_info.nickname and weixin_account_info.head_img:
		return weixin_account_info

	#需要进行方式微信api进行实时获取
	try:
		weixin_account_info = _get_weixin_account_info_via_api(user_profile, social_account)
	except:
		notify_message = u"访问微信api获取微信账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
		watchdog_fatal(notify_message)

	if weixin_account_info and weixin_account_info.nickname:
		try:
			_update_local_weixin_account_info(social_account, weixin_account_info)
		except:
			notify_message = u"更新本地微信账号基本信息失败，openid:{}, cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_fatal(notify_message)

	return weixin_account_info

#给定系统用户配置和社交账号获取社交账号的详细信息
def get_social_account_info(social_account, user_profile, can_use_local=True):
	if social_account is None or user_profile is None:
		return None
	if settings.MODE == 'develop' or social_account.is_for_test:
		return SocialAccountInfo(None, DEFAULT_ICON, subscribe=True)

	#判断社交账号所在平台，使用各个平台获取用户的响应
	#api去获取社交账号的详细信息
	social_account_info = None
	if social_account.is_from_weixin():
		#获取微信用户信息
		social_account_info = get_weixin_account_info(user_profile, social_account, can_use_local)
	elif social_account.is_from_qq():
		#获取qq用户信息
		social_account_info = get_qq_account_info(user_profile, social_account, can_use_local)
	elif social_account.is_frm_sina_weibo():
		#获取新浪微博用户信息
		social_account_info = get_sina_weibo_account_info(user_profile, social_account, can_use_local)
	else:
		raise ValueError(u"不支持社交平台:{}".format(social_account.social_platform))

	return social_account_info
