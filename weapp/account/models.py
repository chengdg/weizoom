# -*- coding: utf-8 -*-

import os
import json
from hashlib import md5
from core.dateutil import get_current_time_in_millis

from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from core import dateutil

from webapp.models import WebApp, GlobalNavbar
from webapp.modules.cms.models import SpecialArticle

from weixin.user.models import get_system_user_binded_mpuser
from watchdog.utils import watchdog_fatal, watchdog_error
from core.exceptionutil import unicode_full_stack
from market_tools.module_api import enable_market_tool_authority_for, disable_market_tool_authority_for



SYSTEM_VERSION_TYPE_BASE= 'base'
SYSTEM_VERSION_TYPE_PREMIUM = 'premium'
SYSTEM_VERSION_TYPES = (
	(SYSTEM_VERSION_TYPE_BASE, '初级版'),
	(SYSTEM_VERSION_TYPE_PREMIUM, '高级版'),
	)

#===============================================================================
# UserProfile ： 用户信息
#===============================================================================
USER_STATUS_NORMAL = 0
USER_STATUS_BUSY = 1
USER_STATUS_DISABLED = 2
USER_STATUSES = (
	(USER_STATUS_NORMAL, '正常'),
	(USER_STATUS_BUSY, '忙碌'),
	(USER_STATUS_DISABLED, '停用')
)
SELF_OPERATION = 0
THIRD_OPERATION = 1
OTHER_OPERATION = 2

OPERATION_TYPE = {
	SELF_OPERATION: u'自运营',
	THIRD_OPERATION: u'代运营',
	OTHER_OPERATION: u'其它'
}

WEBAPP_TYPE_MALL = 0 #普通商城
WEBAPP_TYPE_WEIZOOM_MALL = 1 #微众商城

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	manager_id = models.IntegerField(default=0) #创建该用户的系统用户的id
	webapp_id = models.CharField(max_length=16, db_index=True, verbose_name='用户所创建的app id')
	webapp_type = models.IntegerField(default=0) #商城类型
	app_display_name = models.CharField(max_length=50, verbose_name='用于显示app名称')
	is_active = models.BooleanField(default=True, verbose_name='用户是否有效')
	note = models.CharField(max_length=1024, default='')
	status = models.IntegerField(default=USER_STATUS_NORMAL, choices=USER_STATUSES)
	is_mp_registered = models.BooleanField(default=False, verbose_name='是否已经接入了公众账号') 
	mp_token = models.CharField(max_length=50, verbose_name='绑定公众号使用的token')
	mp_url = models.CharField(max_length=256, verbose_name='公众号绑定的url')
	new_message_count = models.IntegerField(default=0) #新消息数
	webapp_template = models.CharField(max_length=50, default='shop') #webapp的模板
	is_customed = models.IntegerField(default=0) #是否客户自定义CSS样式：1：是；0：否
	is_under_previewed = models.IntegerField(default=0) #是否是预览模式：1：是；0：否
	expire_date_day = models.DateField(auto_now_add=True)
	force_logout_date = models.BigIntegerField(null=True, blank=True, default=0)

	host_name = models.CharField(max_length=1024, default="")
	logout_redirect_to = models.CharField(max_length=1024, default="")
	system_name = models.CharField(max_length=64, default=u'微信营销管理系统', verbose_name='系统名称')
	system_version = models.CharField(max_length=16, choices=SYSTEM_VERSION_TYPES, default=SYSTEM_VERSION_TYPE_BASE, verbose_name='系统版本')
	
	homepage_template_name = models.CharField(max_length=250) #首页模板名
	backend_template_name = models.CharField(max_length=250) #后端页面模板名
	homepage_workspace_id = models.IntegerField(default=0) #homepage workspace的id
	#add by bert 
	account_type = models.IntegerField(default=SELF_OPERATION)#帐号类型
	is_oauth = models.BooleanField(default=False) #是否授权
	#v2
	sub_account_count = models.IntegerField(default=50) #可创建的子账号的个数
	#wepage
	is_use_wepage = models.BooleanField(default=False) #是否启用wepage
	class Meta(object):
		db_table = 'account_user_profile'
		verbose_name = '用户配置'
		verbose_name_plural = '用户配置'

	@property
	def host(self):
		if hasattr(self, '_host'):
			return self._host

		if self.host_name and len(self.host_name.strip()) > 0:
			self._host = self.host_name
		else:
			self._host = settings.DOMAIN

		return self._host


	def force_logout(self):
		self.force_logout_date = get_current_time_in_millis()
		self.save()

	@property
	def is_manager(self):
		return (self.user_id == self.manager_id) or (self.manager_id == 2) #2 is manager's id


class OperationSettings(models.Model):
	owner = models.ForeignKey(User, unique=True)
	non_member_followurl = models.CharField(max_length=1024, default='')
	weshop_followurl = models.CharField(max_length=1024, default='')

	class Meta(object):
		db_table = 'account_operation_settings'
		verbose_name = '运营配置'
		verbose_name_plural = '阴影配置'

	@staticmethod
	def get_settings_for_user(userid):
		if userid is None:
			return None

		settings_list = list(OperationSettings.objects.filter(owner_id=userid)) 
		if len(settings_list) == 0:
			return OperationSettings.objects.create(owner_id=userid)
		else:
			return settings_list[0]

#===============================================================================
# GlobalSetting : 系统的全局配置
#===============================================================================
class GlobalSetting(models.Model):
	super_password = models.CharField(max_length=50)

	class Meta(object):
		db_table = 'weapp_global_setting'
		verbose_name = '全局配置'
		verbose_name_plural = '全局配置'


ALIPAY_SIGN_TYPES = (
		('MD5', 'MD5'),
		('0001', '0001(RSA)')
	)

#===============================================================================
# UserAlipayOrderConfig : 支付宝支付配置信息
#===============================================================================
class UserAlipayOrderConfig(models.Model):
	owner = models.ForeignKey(User)
	partner = models.CharField(max_length=32, verbose_name='合作身份者ID，以2088开头由16位纯数字组成的字符串')
	key = models.CharField(max_length=32, verbose_name='交易安全检验码，由数字和字母组成的32位字符串')
	private_key = models.CharField(max_length=1024, blank=True, null=True, verbose_name='商户的私钥')
	ali_public_key = models.CharField(max_length=1024, blank=True, null=True, verbose_name='支付宝的公钥')
	input_charset = models.CharField(max_length=8, default='utf-8', verbose_name='字符编码格式 目前支持utf-8')
	sign_type = models.CharField(max_length=8, default='MD5', choices=ALIPAY_SIGN_TYPES, verbose_name='签名方式')
	seller_email = models.CharField(max_length=64, blank=True)

	class Meta(object):
		db_table = 'account_alipay_order_config'
		verbose_name = '支付宝支付配置信息'
		verbose_name_plural = '支付宝支付配置信息'

#===============================================================================
# UserTenpayOrderConfig : 财付通支付配置信息
#===============================================================================
class UserTenpayOrderConfig(models.Model):
	owner = models.ForeignKey(User)
	partner = models.CharField(max_length=32, verbose_name='合作商户号')
	key = models.CharField(max_length=32, verbose_name='交易密钥')	
	input_charset = models.CharField(max_length=8, default='utf-8', verbose_name='字符编码格式 目前支持utf-8')
	sign_type = models.CharField(max_length=8, default='MD5', choices=ALIPAY_SIGN_TYPES, verbose_name='签名方式')

	class Meta(object):
		db_table = 'account_tenpay_order_config'
		verbose_name = '财付通支付配置信息'
		verbose_name_plural = '财付通支付配置信息'


#===============================================================================
# UserWeixinPayOrderConfig : 微信支付配置信息
#===============================================================================
V2 = 0
V3 = 1
class UserWeixinPayOrderConfig(models.Model):
	owner = models.ForeignKey(User)
	app_id = models.CharField(max_length=32, verbose_name='微信公众号app_id')
	app_secret = models.CharField(max_length=64)
	partner_id = models.CharField(max_length=32, verbose_name='合作商户id')
	partner_key = models.CharField(max_length=32, verbose_name='合作商初始密钥')	
	paysign_key = models.CharField(max_length=128, verbose_name='支付专用签名串')	
	pay_version  = models.IntegerField(default=V2)

	class Meta(object):
		db_table = 'account_weixin_pay_order_config'
		verbose_name = '微信支付配置信息'
		verbose_name_plural = '微信支付配置信息'


#===============================================================================
# Job : 后台任务
#===============================================================================
NOT_START = 0 #任务未启动
RUNNING = 1 #任务运行中
FINISH = 2 #任务正常结束
ABORT = 3 #任务异常终止
CLOSED = 4 #任务被客户端确认关闭
JOB_STATUS_CHOICES = (
	(0, '未启动'),
	(1, '运行中'),
	(2, '任务正常结束'),
	(3, '任务异常终止'),
)
class Job(models.Model):
	owner = models.ForeignKey(User, related_name='owned_jobs')
	name = models.CharField(max_length=500) #任务名
	service_name = models.CharField(max_length=100, default='unknown') #service名
	runner = models.CharField(max_length=100, default='unknown') #负责处理该job的service的标识符
	process = models.CharField(max_length=20, default='unknown') #处理该job的process id
	create_time = models.DateTimeField(auto_now_add=True) #任务创建时间
	scheduled_time = models.DateTimeField(auto_now_add=True) #任务预期启动时间
	start_time = models.DateTimeField(auto_now_add=True) #任务真实启动时间
	update_time = models.DateTimeField(auto_now=True) #service更新job信息时间
	finish_time = models.DateTimeField(auto_now=True) #任务结束时间
	total_load = models.IntegerField(default=-1) #总工作量
	current_load = models.IntegerField(default=0) #当前完成工作量
	status = models.IntegerField(default=NOT_START, choices=JOB_STATUS_CHOICES) #任务当前状态
	filter1 = models.CharField(max_length=100, blank=True, db_index=True) #service自定义字段
	result = models.CharField(max_length=1024, blank=True) #任务运行结果
	args = models.TextField(max_length=1024, blank=True) #任务参数
	log = models.TextField(blank=True) #任务运行日志
					
	def __unicode__(self):
		return self.name
	
	class Meta(object):
		db_table = 'tiger_job'
		ordering = ["-create_time"]
		verbose_name = '后台任务'
		verbose_name_plural = '后台任务'


#===============================================================================
# HobbitSetting : Hobbit框架的配置信息
#===============================================================================
class HobbitSetting(models.Model):
	is_save_log = models.BooleanField(default=False)
	enable_profiling = models.BooleanField(default=False)
	
	class Meta(object):
		db_table = 'tiger_hobbit_setting'
		verbose_name = 'Hobbit配置'
		verbose_name_plural = 'Hobbit配置'


#===============================================================================
# user_order_notify_setting : 发送订单邮件信息配置
#===============================================================================
PLACE_ORDER = 0	#下单
PAY_ORDER = 1	#付款
SHIP_ORDER = 2#发货
SUCCESSED_ORDER = 3#完成
CANCEL_ORDER = 4 #已取消
class UserOrderNotifySettings(models.Model):
	user = models.ForeignKey(User)
	emails = models.TextField(default='')# '|'分割
	black_member_ids= models.TextField(default='')#'|'分割，会员id
	status = models.IntegerField(default=0)
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'user_order_notify_setting'
		verbose_name = '发送订单邮件信息配置'
		verbose_name_plural = '发送订单邮件信息配置'


#===============================================================================
# increase_new_message_count : 增加new message count计数
#===============================================================================
def increase_new_message_count(user=None, webapp_id=None, count=1):
	if user:
		profile_query_set = UserProfile.objects.filter(user=user)
	else:
		profile_query_set = UserProfile.objects.filter(webapp_id=webapp_id)
	profile_query_set.update(new_message_count = F('new_message_count') + count)


#===============================================================================
# reset_new_message_count : 将news message count清零
#===============================================================================
def reset_new_message_count(user=None, webapp_id=None):
	if user is None and webapp_id is None:
		return

	if user:
		profile_query_set = UserProfile.objects.filter(user=user)
	else:
		profile_query_set = UserProfile.objects.filter(webapp_id=webapp_id)
	profile_query_set.update(new_message_count = 0)


def delete_system_user(user):
	if user is None:
		return False

	try:
		from modules.member.models import Member
		user_profile = UserProfile.objects.get(user_id=user.id)
		mpuser = get_system_user_binded_mpuser(user)
		if mpuser:
			mpuser.delete()

		#删除所有之前的会员
		Member.objects.filter(webapp_id=user_profile.webapp_id).delete()
		user_profile.delete()

		User.objects.filter(id=user.id).delete()

		return True
	except:
		watchdog_fatal(u"删除用户{}失败".format(user.id))
		return False

#===============================================================================
# create_profile : 自动创建user profile
#===============================================================================
def __create_special_article(owner, name, title):
	from webapp.modules.cms.models import SpecialArticle
	article = SpecialArticle.objects.create(
		owner = owner, 
		name = name, 
		title = title
	)

	article.display_index = article.id
	article.save()

class FakeRequest(object):
	def __init__(self):
		pass

def create_profile(instance, created, **kwargs):
	if created:
		if instance.username == 'admin':
			return
		
		#add by bert 
		if instance.username.find('001@') > -1 or instance.username.find('002@') > -1 or instance.username.find('003@') > -1:
			return 

		from mall.models import PostageConfig, MallConfig
		from market_tools.models import MarketToolAuthority
		try:
			if PostageConfig.objects.filter(owner=instance).count() == 0:
				#创建默认的“免运费”配置
				PostageConfig.objects.create(
					owner = instance,
					name = u'免运费',
					added_weight = "0.0",
					is_enable_added_weight = False,
					is_enable_special_config = False,
					is_enable_free_config = False,
					is_used = True,
					is_system_level_config = True
				)
		except:
			notify_msg = u"创建user:{}运费配置时异常, cause:\n{}".format(instance.id, unicode_full_stack())
			watchdog_error(notify_msg)
		
		try:
			if MallConfig.objects.filter(owner=instance).count() == 0:
				MallConfig.objects.create(
					owner = instance
				)
		except:
			notify_msg = u"创建user:{} MallConfig时异常, cause:\n{}".format(instance.id, unicode_full_stack())
			watchdog_error(notify_msg)

		try:
			if MarketToolAuthority.objects.filter(owner=instance).count() == 0:
				MarketToolAuthority.objects.create(
					owner = instance,
					is_enable_market_tool = False
				)
		except:
			notify_msg = u"创建user:{} MarketToolAuthority时异常, cause:\n{}".format(instance.id, unicode_full_stack())
			watchdog_error(notify_msg)

		try:
			from webapp.modules.cms.models import SpecialArticle
			if SpecialArticle.objects.filter(owner=instance).count() == 0:
				__create_special_article(instance, 'not_from_weixin', u'非微信访问页面')
				__create_special_article(instance, 'integral_guide', u'积分指南')
		except:
			notify_msg = u"创建user:{} SpecialArticle时异常, cause:\n{}".format(instance.id, unicode_full_stack())
			watchdog_error(notify_msg)

		if UserProfile.objects.filter(user=instance).count() == 0:
			profile = UserProfile.objects.create(user = instance, backend_template_name = 'default_v3', manager_id = instance.id, expire_date_day = dateutil.yearsafter(1))
			webapp_id = settings.MIXUP_FACTOR + profile.id
			mp_url = 'http://%s/weixin/%d/' % (settings.DOMAIN, webapp_id)

			token_str = ('*)|%s12@' % mp_url).replace(settings.DOMAIN, 'balabalame')
			mp_token = md5(token_str).hexdigest()[1:-1]

			profile.webapp_id = '%d' % webapp_id
			profile.mp_url = mp_url
			profile.mp_token = mp_token
			
			profile.save()
			
			#创建WebApp
			WebApp.objects.create(
				appid = '%s'%webapp_id,
				owner = instance,
			)

			if IntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() == 0:
				IntegralStrategySttings.objects.create(webapp_id=webapp_id)



signals.post_save.connect(create_profile, sender=User, dispatch_uid = "account.create_profile")

def update_user_settings(instance, created, **kwargs):
	if created:
		return

	if SYSTEM_VERSION_TYPE_PREMIUM == instance.system_version:
		enable_market_tool_authority_for(instance.user)
	else:
		disable_market_tool_authority_for(instance.user)

	import cache_util
	cache_util.get_user_profile_by_owner_id(instance.user_id)


signals.post_save.connect(update_user_settings, sender=UserProfile, dispatch_uid = "account.update_profile")

#当用户登录后在session中添加最近登录时间
def update_session_last_login(sender, user, request, **kwargs):
	if request:
		request.session['LAST_LOGIN_DATE'] = get_current_time_in_millis()

user_logged_in.connect(update_session_last_login)


#===============================================================================
# UserHasSubUser: 员工帐号
#===============================================================================
class UserHasSubUser(models.Model):
	user = models.ForeignKey(User)
	sub_user = models.ForeignKey(User, related_name='sub_user') #子账号信息
	is_active = models.BooleanField(default=False)
	remark = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'account_user_has_sub_user'
		verbose_name = '员工帐号'
		verbose_name_plural = '员工帐号'



