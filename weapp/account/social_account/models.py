# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.db import models
from django.contrib.auth.models import Group, User

SOCIAL_PLATFORM_WEIXIN = 0
SOCIAL_PLATFORM_QQ = 1
SOCIAL_PLATFORM_SINAWEIBO = 2
SOCIAL_PLATFORM_PHONE = 3
SOCIAL_PLATFORMS = (
	(SOCIAL_PLATFORM_WEIXIN, '微信'),
	(SOCIAL_PLATFORM_QQ, 'QQ'),
	(SOCIAL_PLATFORM_SINAWEIBO, '新浪微博'),
	(SOCIAL_PLATFORM_PHONE, '手机注册'),
)

class QQAccountInfo(models.Model):
	nickname = models.CharField(max_length=32, db_index=True, verbose_name='昵称')
	head_img = models.CharField(max_length=256, verbose_name='头像地址')
	openid = models.CharField(max_length=64, db_index=True, verbose_name='openid')

	class Meta(object):
		db_table = 'qq_account_info'
		verbose_name = 'QQ账号信息'
		verbose_name_plural = 'QQ账号信息'

#TODO 是否需要增加粉丝数等信息?
class SinaWeiboAccountInfo(models.Model):
	nickname = models.CharField(max_length=32, db_index=True, verbose_name='昵称')
	head_img = models.CharField(max_length=256, verbose_name='头像地址')
	openid = models.CharField(max_length=64, db_index=True, verbose_name='openid')

	class Meta(object):
		db_table = 'sinaweibo_account_info'
		verbose_name = '新浪微博账号信息'
		verbose_name_plural = '新浪微博账号信息'

class SocialAccount(models.Model):
	platform = models.IntegerField(default=SOCIAL_PLATFORM_WEIXIN, 
		choices=SOCIAL_PLATFORMS, db_index=True, verbose_name='社会化平台')
	webapp_id = models.CharField(max_length=16, db_index=True)
	token = models.CharField(max_length=64, db_index=True, unique=True, verbose_name='token')
	access_token = models.CharField(max_length=64,  blank=True, default='', verbose_name='access_token')
	is_for_test = models.BooleanField(default=False)
	openid = models.CharField(max_length=64, db_index=True, verbose_name='openid')
	uuid = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='加入日期')

	def is_from_weixin(self):
		return SOCIAL_PLATFORM_WEIXIN == self.platform

	def is_from_qq(self):
		return SOCIAL_PLATFORM_QQ == self.platform

	def is_frm_sina_weibo(self):
		return SOCIAL_PLATFORM_SINAWEIBO == self.platform

	class Meta(object):
		db_table = 'binding_social_account'
		verbose_name = '绑定的社会化账号'
		verbose_name_plural = '绑定的社会化账号信息'


LOGIN_SIGN_TYPES = (
('MD5', 'MD5'),
('0001', '0001(RSA)')
)
#===============================================================================
# UserSocialLoginConfig: 社会化登陆配置信息
#===============================================================================
class UserSocialLoginConfig(models.Model):
	owner = models.ForeignKey(User, unique=True)
	weibo_app_key = models.CharField(max_length=10, default='',verbose_name='新浪App Key')
	weibo_app_secret = models.CharField(max_length=1024, default='', verbose_name='新浪App Secret')
	qq_app_id = models.CharField(max_length=10, default='', verbose_name='QQ合作身份者ID')
	qq_app_key = models.CharField(max_length=1024, default='', verbose_name='QQ合作身份者KEY')
	input_charset = models.CharField(max_length=8, default='utf-8', verbose_name='字符编码格式 目前支持utf-8')
	sign_type = models.CharField(max_length=8, default='MD5', choices=LOGIN_SIGN_TYPES, verbose_name='签名方式')

	class Meta(object):
		db_table = 'account_social_login_config'
		verbose_name = '社会化登陆配置信息'
		verbose_name_plural = '社会化登陆配置信息'


