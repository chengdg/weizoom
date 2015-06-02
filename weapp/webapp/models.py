# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#########################################################################
# App：App信息
#########################################################################
class WebApp(models.Model):
	owner = models.ForeignKey(User)
	appid = models.CharField(max_length=16)
	name = models.CharField(max_length=100, default='')

	class Meta(object):
		db_table = 'webapp'

#########################################################################
# PageVisitLog：Page访问日志
#########################################################################
class PageVisitLog(models.Model):
	webapp_id = models.CharField(max_length=16)
	token = models.CharField(max_length=64, blank=True)
	url = models.CharField(max_length=1024)
	is_from_mobile_phone = models.BooleanField()
	create_date = models.DateField(auto_now_add=True, db_index=True) #访问日期
	created_at = models.DateTimeField(auto_now_add=True) #访问时间

	class Meta(object):
		db_table = 'webapp_page_visit_log'
		verbose_name = 'WebApp Page访问日志'
		verbose_name_plural = 'WebApp Page访问日志'


#########################################################################
# PageVisitDailyStatistics：Page访问统计结果
#########################################################################
URL_TYPE_ALL = 0
URL_TYPE_SPECIFIC = 1
USER_STATUSES = (
	(URL_TYPE_ALL, u'总计'),
	(URL_TYPE_SPECIFIC, u'独立')
)
class PageVisitDailyStatistics(models.Model):
	webapp_id = models.CharField(max_length=16)
	url_type = models.IntegerField(default=URL_TYPE_SPECIFIC, choices=USER_STATUSES)
	url = models.CharField(max_length=1024, default='')
	pv_count = models.IntegerField(default=0) #pv
	uv_count = models.IntegerField(default=0) #uv
	data_date = models.DateField() #统计日期

	class Meta(object):
		db_table = 'webapp_page_visit_daily_statistics'
		verbose_name = 'WebApp Page访问统计'
		verbose_name_plural = 'WebApp Page访问统计'



########################################################################
# Workspace: 一个工作空间，可包含多个Project
########################################################################
class Workspace(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50) #名字
	inner_name = models.CharField(max_length=50) #内部名字
	data_backend = models.CharField(max_length=50) #数据源
	source_workspace_id = models.IntegerField(default=0) #源workspace的id
	template_project_id = models.IntegerField(default=0) #模板project的id
	template_name = models.CharField(max_length=125, default='default') #首页模板名
	backend_template_name = models.CharField(max_length=125, default='default') #非首页模板名
	is_deleted = models.BooleanField(default=False) #是否已删除
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	display_index = models.IntegerField(default=1) #显示排序

	@staticmethod
	def get_market_tool_workspace(owner, market_tool_name):
		'''market_tool_name的格式为: market_tool:vote'''
		workspace = Workspace()
		workspace.owner = owner
		workspace.data_backend = market_tool_name
		return workspace

	@staticmethod
	def get_app_workspace(owner, app_name):
		'''app的格式为: app:app1'''
		workspace = Workspace()
		workspace.owner = owner
		workspace.data_backend = app_name
		return workspace
		
	class Meta(object):
		db_table = 'webapp_workspace'
		verbose_name = 'APP'
		verbose_name_plural = 'APP'


########################################################################
# Project: 一个项目，可包含多个Page
########################################################################
class Project(models.Model):
	owner = models.ForeignKey(User)
	workspace = models.ForeignKey(Workspace)
	name = models.CharField(max_length=50) #项目名
	inner_name = models.CharField(max_length=50) #内部名字
	type = models.CharField(max_length=50) #项目类型
	css = models.TextField() #css内容
	pagestore = models.CharField(max_length=50, default='mongo') #使用的pagestore类型
	source_project_id = models.IntegerField(default=0) #源project的id
	datasource_project_id = models.IntegerField(default=0) #提供数据源的project
	template_project_id = models.IntegerField(default=0) #模板project的id
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	@staticmethod
	def get_market_tool_project(owner, market_tool_name):
		'''market_tool_name的格式为: market_tool:vote'''
		project = Project()
		project.id = '%s:%d' % (market_tool_name, owner.id)
		project.owner = owner
		project.type = 'market_tool'
		return project

	@staticmethod
	def get_app_project(owner, app_name):
		'''app_name的格式为: apps:vote'''
		project = Project()
		project.id = '%s:%d' % (app_name, owner.id)
		project.owner = owner
		project.type = 'app'
		return project

	class Meta(object):
		db_table = 'webapp_project'
		verbose_name = '项目'
		verbose_name_plural = '项目'


########################################################################
# GlobalNavbar: webapp上的全局导航
########################################################################
class GlobalNavbar(models.Model):
	owner = models.ForeignKey(User)
	is_enable = models.BooleanField(default=False) #是否开启全局导航
	content = models.TextField() #navbar的json字符串
	created_at = models.DateTimeField(auto_now_add=True) #添加时间


	class Meta(object):
		db_table = 'webapp_global_navbar'
		verbose_name = '全局导航'
		verbose_name_plural = '全局导航'


#
# [hack] 修改Django User的行为，添加判斷是否可以使用weizoom card的操作
#
from django.contrib.auth.models import User
def __user_can_use_weizoom_card(self):
	from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
	return AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(self.id)
User.can_use_weizoom_card = __user_can_use_weizoom_card


#########################################################################
# WebappUserClickConcernShopLog：记录在微众商城中给商户带来的关注
#########################################################################
class WebappUserClickConcernShopLog(models.Model):
	webapp_user_id = models.IntegerField(default=0, verbose_name="手机端会员")
	from_webapp_id = models.CharField(max_length=16, default='', verbose_name="从该店铺进入")
	to_webapp_id = models.CharField(max_length=16, default='', verbose_name="到该店铺")
	redirect_url = models.CharField(max_length=1024, default='', verbose_name="跳转url")
	product_id = models.IntegerField(default=0, verbose_name="商品ID")
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'webapp_user_click_concern_shop_log'
		verbose_name = '记录在微众商城中给商户带来的关注'
		verbose_name_plural = '记录在微众商城中给商户带来的关注'

