# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import urllib
from account.social_account.models import UserSocialLoginConfig
from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal
from core.exceptionutil import unicode_full_stack

class WeiboConfig(object):
	"""
	Weibo配置信息
	"""

	def __init__(self):
		raise NotImplementedError

	def __init__(self, user_profile):
		try:
			configs = UserSocialLoginConfig.objects.filter(owner=user_profile.user)
			if configs.count():
				config = configs[0]
				self.app_id = config.weibo_app_key
				self.app_secret = config.weibo_app_secret
		except:
			error_message = u'weibo WeiboConfig init error，原因:{}'.format(unicode_full_stack())
			watchdog_error(error_message)


	# 合作身份者ID
	app_id = "3189676293"

	# app_secret
	app_secret = "91f69109d70d6770827e433a3299087d"

	# 字符编码格式 目前支持  utf-8
	input_charset = "utf-8"

	# 签名方式，选择项：0001(RSA)、MD5
	sign_type = "MD5"

	login_callback_redirect_uri = "http://{}/social_account/weibo/login_callback/"

	code = "get_user_info,list_album,upload_pic,do_like"


	def get_callback_redirect_uri(self):
		redirect_uri = urllib.quote(self.login_callback_redirect_uri, '')
		return redirect_uri

	def get_login_callback_redirect_uri(self, request):
		domain = "www.babydami.com"
		try:
			domain = request.user_profile.pc_mall_domain
		except:
			pass
		return self.login_callback_redirect_uri.format(domain)

	def get_state(self, request):
		webapp_id = '3181'
		try:
			last_page = request.META['HTTP_REFERER']
			webapp_id = request.user_profile.webapp_id
			notify_message = u'微博登陆获取webapp_id在weibo_config.py，webapp_id:{}'.format(webapp_id)
			watchdog_info(notify_message)
		except:
			notify_message = u'微博登陆获取webapp_id错误在weibo_config.py，原因:{}'.format(unicode_full_stack())
			watchdog_fatal(notify_message)
			last_page = '/'
		return '%s~%s' % (webapp_id, last_page)