# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.db import models
import mongoengine as mongo_models
from django.contrib.auth.models import User

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert, watchdog_fatal

#定制化app状态
class CustomizedappStatus(object):
	STOPEED = 0 #已停止或未启动
	STOPPING = 1 #正在停止
	STARTING = 2 #正在启动
	RUNNING = 3 #正在运行
	UPDATING = 4 #正在更新
	WITHERROR = 5 #正在运行，但是有故障
	UNINSTALLED = 6 #已经卸载
	INACTIVE = 7 #需要激活后才可以使用
	MARKETTOOL = 8 #该应用是markettool转化而来的app

#########################################################################
# CustomizedApp : 定制化App信息
#########################################################################
class CustomizedApp(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100, db_index=True, unique=True)
	display_name = models.CharField(max_length=100) #用于显示的名字
	status = models.IntegerField(default=CustomizedappStatus.STOPEED, verbose_name='状态')
	last_version = models.IntegerField(max_length=16, default=1, verbose_name='当前版本')
	updated_time = models.DateTimeField(verbose_name='最近更新时间')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

	class Meta(object):
		db_table = 'customized_apps'
		verbose_name = '用户定制APP'
		verbose_name_plural = '用户定制APP'

	@property
	def is_running(self):
		return CustomizedappStatus.RUNNING == self.status

	@property
	def is_stopped(self):
		return CustomizedappStatus.STOPEED == self.status		

	@property
	def is_uninstalled(self):
		return CustomizedappStatus.UNINSTALLED == self.status

	@property
	def is_inactive(self):
		return CustomizedappStatus.INACTIVE == self.status		

	def update_version(self, new_version):
		if new_version is None:
			return

		self.last_version = new_version
		try:
			CustomizedApp.objects.filter(id=self.id).update(
					last_version = new_version
				)
		except:
			notify_msg = u"更新app:{}版本号为{}失败，cause:\n{}".format(
					self.__unicode__(),
					new_version,					
					unicode_full_stack()
				)
			watchdog_fatal(notify_msg, self.owner.id)

	def update_status(self, new_status):
		if new_status is None:
			return

		self.status = new_status
		try:
			CustomizedApp.objects.filter(id=self.id).update(
					status = new_status
				)
		except:
			notify_msg = u"更新app:{}状态为{}失败，cause:\n{}".format(
					self.__unicode__(),
					unicode_full_stack()
				)
			watchdog_fatal(notify_msg, self.owner.id)

	@property
	def appinfo(self):
		try:		
			return CustomizedAppInfo.objects.get(customized_app_id=self.id)
		except:
			err_msg = u"获取appid为{}的应用信息失败，cause:\n{}".format(
					self.id,
					unicode_full_stack()
				)
			watchdog_alert(err_msg, self.owner.id)
			return None

	@staticmethod
	def all_valid_apps_list():
		try:
			return list(CustomizedApp.objects.exclude(status=CustomizedappStatus.INACTIVE))
		except:
			err_msg = u"获取有效的app列表失败，cause:\n{}".format(
					unicode_full_stack()
				)
			watchdog_alert(err_msg)
			return []

	@staticmethod
	def all_running_apps_list(user=None):
		try:
			if user is None:
				return list(CustomizedApp.objects.filter(status=CustomizedappStatus.RUNNING))
			else:
				return list(CustomizedApp.objects.filter(owner_id=user.id, status=CustomizedappStatus.RUNNING))
		except:
			err_msg = u"获取正在运行的app列表失败，cause:\n{}".format(
					unicode_full_stack()
				)
			watchdog_alert(err_msg)
			return []

	def __unicode__(self):
		return u"[user:{}, name:{}, version:{}]".format(
				self.owner.id,
				self.name,
				self.last_version
			)

	def __str__(self):
		return "[user:{}, name:{}, version:{}]".format(
				self.owner.id,
				self.name,
				self.last_version
			)


#########################################################################
# CustomizedAppModel : 定制化App的数据描述
# 实际数据的io操作改为基于MongoDB来实现
#########################################################################
class CustomizedAppModel(models.Model):
	class Meta(object):
		abstract = True


#########################################################################
# CustomizedAppInfo : 定制化App详细信息
#########################################################################
class CustomizedAppInfo(models.Model):
	owner = models.ForeignKey(User)
	customized_app = models.ForeignKey(CustomizedApp)
	app_name = models.CharField(max_length=100, default='', verbose_name='app名称')
	description = models.CharField(max_length=100, default='', verbose_name='app描述')
	app_logo = models.CharField(max_length=100, default='', verbose_name='app图标')
	remark_name = models.CharField(max_length=100, default='', verbose_name='备注名称')
	principal = models.CharField(max_length=100, default='', verbose_name='负责人')
	repository_path = models.TextField(verbose_name='产品库地址')
	repository_username = models.TextField(verbose_name='产品库用户名')
	repository_passwd = models.TextField(verbose_name='产品库用户密码')

	class Meta(object):
		db_table = 'customized_app_info'
		verbose_name = '用户定制APP详细信息'
		verbose_name_plural = '用户定制APP详细信息'

class AppOps(object):
	INSTALL = 'install'
	STOP = 'stop'
	UPDATE = 'update'
	REMOVE = 'remove'
	UNINSTALL = 'uninstall'

#########################################################################
# CustomizedAppOpLog : 记录对APP进行操作的log信息
#########################################################################
class CustomizedAppOpLog(models.Model):
	owner = models.ForeignKey(User)
	customized_app = models.ForeignKey(CustomizedApp)
	op = models.CharField(max_length=16)
	op_result_msg = models.TextField(default='', blank=True, null=True, verbose_name='操作结果')
	failed_cause_stack = models.TextField(default='', blank=True, null=True, verbose_name='更新失败的详细堆栈信息')
	update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

	class Meta(object):
		db_table = 'customized_app_op_log'
		verbose_name = '对用户定制APP进行的操作日志'
		verbose_name_plural = '对用户定制APP进行的操作日志'


class TemplateMessageDetails(mongo_models.Document):
	"""
	模板消息详情
	"""
	template_id = mongo_models.StringField(max_length=256, default='') #用于weixin api的模板id
	title = mongo_models.StringField(max_length=256) #模板标题
	primary_industry = mongo_models.StringField(max_length=64) #一级行业
	deputy_industry = mongo_models.StringField(max_length=64) #二级行业
	content = mongo_models.StringField(max_length=1024) #模板内容

	meta = {
		'collection': 'apps_template_message_details'
	}

class UserHasTemplateMessages(mongo_models.Document):
	"""
	商家在公众平台上配置的模板消息
	"""
	owner_id = mongo_models.LongField() #所属商家
	template_id = mongo_models.StringField(max_length=32) #模板详情记录的id

	meta = {
		'collection': 'apps_user_has_template'
	}

class UserappHasTemplateMessages(mongo_models.Document):
	"""
	各百宝箱活动所配置的模板消息
	"""
	owner_id = mongo_models.LongField() #所属商家
	apps_type = mongo_models.StringField(max_length=64) #活动类型
	data_control = mongo_models.DynamicField() #模板选择选择控制 e.g {"success": "template_id1", "fail": "template_id2"}

	meta = {
		'collection': 'apps_Userapp_has_template'
	}



