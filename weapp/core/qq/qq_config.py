# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from account.social_account.models import UserSocialLoginConfig
from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack
from core.weibo.weibo_config import WeiboConfig

class QQConfig(object):
	"""
	QQ配置信息
	"""

	def __init__(self):
		raise NotImplementedError

	def __init__(self, user_profile):
		try:
			configs = UserSocialLoginConfig.objects.filter(owner=user_profile.user)
			if configs.count():
				config = configs[0]
				self.app_id = config.qq_app_id
				self.app_key = config.qq_app_key
		except:
			error_message = u'qq QQConfig init error，原因:{}'.format(unicode_full_stack())
			watchdog_error(error_message)

	#app_id
	app_id = "100589053"

	# app_key
	app_key = "c9c2d8e75d7e2ecfea3977b3c560c3db"

	# 字符编码格式 目前支持  utf-8
	input_charset = "utf-8"

	# 签名方式，选择项：0001(RSA)、MD5
	sign_type = "MD5"

	login_callback_redirect_uri = "http://{}/social_account/qq/login_callback/"

	code = "get_user_info,list_album,upload_pic,do_like"

	def get_state(self, request):
		weibo_config = WeiboConfig(request.user_profile)
		return  weibo_config.get_state(request)


	def get_login_callback_redirect_uri(self, request):
		domain = "www.babydami.com"
		try:
			domain = request.user_profile.pc_mall_domain
		except:
			pass
		return self.login_callback_redirect_uri.format(domain)
