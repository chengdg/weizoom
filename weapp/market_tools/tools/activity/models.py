# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F
from datetime import datetime, timedelta

from core import dateutil
from modules.member.models import *
from account.models import *


#########################################################################
# 活动：Activity
#########################################################################
ACTIVITY_STATUS_RUNING = 1
ACTIVITY_STATUS_STOP = 0
ACTIVITY_STATUS_TIMEOUT = 2
ACTIVITY_STATUS_NO_START = 3
STATUS2TEXT = {
	ACTIVITY_STATUS_RUNING: u'已启动',
	ACTIVITY_STATUS_STOP: u'已暂停',
	ACTIVITY_STATUS_NO_START: u'未启动',
	ACTIVITY_STATUS_TIMEOUT: u'已过期'
}
class Activity(models.Model):
	STATUS = (
		(ACTIVITY_STATUS_RUNING, u"已启动"),
		(ACTIVITY_STATUS_STOP, u"已暂停"),
		(ACTIVITY_STATUS_NO_START, u"未启动"),
		(ACTIVITY_STATUS_TIMEOUT, u"已过期"),
	)
	owner = models.ForeignKey(User, related_name='market_tool_activity_user')
	name = models.CharField(max_length=256) #活动名称
	start_date = models.CharField(max_length=256) #开始日期
	end_date = models.CharField(max_length=256) #结束日期
	prize_type = models.IntegerField(verbose_name='奖品类别', default=-1) #0实物，1优惠券，2兑换码，3积分，-1无奖励
	prize_source = models.CharField(max_length=100, default='', verbose_name='奖品来源')
	detail = models.TextField() #活动内容
	status = models.IntegerField(default=ACTIVITY_STATUS_NO_START, choices=STATUS)
	guide_url = models.CharField(max_length=256) #引导地址
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	is_enable_offline_sign = models.BooleanField(default=False) #是否启用线下签到
	is_non_member = models.BooleanField(default=False) #是否非会员可参与
	type = models.IntegerField(default=0) #是否是特殊活动
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_activity'
		verbose_name = '活动'
		verbose_name_plural = '活动'
		ordering = ['-id']

	def get_activities_by_member(self, member):
		activity_ids = ItmesValue.objects.filter(member_id=member.id).values("activity_id").distinct()
		activities = Activity.objects.filter(id__in=activity_ids)
		return activities

	def check_time(self):
		today = datetime.today()

		end_date = self.end_date + "-23-59-59"
		end_date = datetime.strptime(end_date,'%Y-%m-%d-%H-%M-%S')
		if today >= end_date:
			self.status = ACTIVITY_STATUS_TIMEOUT
			self.save()

		start_date = self.start_date + "-0-0-0"
		start_date = datetime.strptime(start_date,'%Y-%m-%d-%H-%M-%S')
		if self.status == ACTIVITY_STATUS_NO_START and today >= start_date:
			self.status = ACTIVITY_STATUS_RUNING
			self.save()

	@property
	def joined_weapp_users(self):
		member_ids = [value.webapp_user_id for value in ActivityItemValue.objects.filter(activity=self)]
		return list(WebAppUser.objects.filter(id__in=member_ids))

	@property
	def joined_weapp_users_count(self):
		return ActivityItemValue.objects.filter(activity=self).values("webapp_user_id").distinct().count()

	@staticmethod
	def get_activites(request):
		webapp_user = request.webapp_user
		activity_ids = ActivityItemValue.objects.values_list('activity_id', flat=True).filter(webapp_user_id=webapp_user.id)
		activities = list(Activity.objects.filter(id__in=activity_ids))
		activity_user_codes = ActivityUserCode.objects.filter(activity_id__in=activity_ids, webapp_user_id=webapp_user.id)
		activity_id2sign_code = dict([(activity_user_code.activity_id, activity_user_code.sign_code) for activity_user_code in activity_user_codes])
		for activitie in activities:
			try:
				activitie.sign_code = activity_id2sign_code[activity.id]
			except:
				 activitie.sign_code = ''
		workspace_template_info = 'workspace_id=market_tool:activity&webapp_owner_id=%d&project_id=0' % request.project.owner_id
		for activity in activities:
			activity.target_link = './?module=market_tool:activity&model=activity&action=get&activity_id=%d&%s' % (activity.id, workspace_template_info)
		return activities


ACTIVITYITEM_TYPE_TEXT = 0
ACTIVITYITEM_TYPE_SELECT = 1
ACTIVITYITEM_TYPE_IMAGE = 2
ACTIVITYITEM_TYPE_CHECKBOX = 3
ITEMTYPE2TEXT = {
	ACTIVITYITEM_TYPE_TEXT: u'文本输入框',
	ACTIVITYITEM_TYPE_SELECT: u'单选框',
	ACTIVITYITEM_TYPE_IMAGE: u'图片上传控件',
	ACTIVITYITEM_TYPE_CHECKBOX: u'复选框'
}
#########################################################################
# ActivityItem: 用户输入项
#########################################################################
class ActivityItem(models.Model):
	ACTIVITYITEM_TYPES = (
		(ACTIVITYITEM_TYPE_TEXT, u"文本"),
		(ACTIVITYITEM_TYPE_SELECT, u"单选框"),
		(ACTIVITYITEM_TYPE_IMAGE, u"图片"),
		(ACTIVITYITEM_TYPE_CHECKBOX, u"复选框"),
	)
	owner = models.ForeignKey(User)
	activity = models.ForeignKey(Activity)
	title = models.CharField(max_length=50) #输入项的title
	type = models.IntegerField(max_length=1, choices=ACTIVITYITEM_TYPES, default=ACTIVITYITEM_TYPE_TEXT)  #item类型
	initial_data = models.CharField(max_length=800, null=True, default='') #  选项: ‘｜’区分
	is_mandatory = models.BooleanField(default=False) #是否必填
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_activity_item'
		verbose_name = '活动报名Item'
		verbose_name_plural = '活动报名Item'


#########################################################################
# ActivityItemValue：活动报名Item中填写的数据
#########################################################################
class ActivityItemValue(models.Model):
	owner = models.ForeignKey(User)
	activity = models.ForeignKey(Activity)
	item = models.ForeignKey(ActivityItem)
	webapp_user_id = models.IntegerField(default=-1)
	value = models.CharField(max_length=256, null=True) #内容
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_activity_item_value'
		verbose_name = '活动报名Item对应数据'
		verbose_name_plural = '活动报名Item对应数据'

	def get_member(self):
		return self.member



#########################################################################
# ActivityUserCode：活动报名用户签到码
#########################################################################
class ActivityUserCode(models.Model):
	owner = models.ForeignKey(User)
	activity = models.ForeignKey(Activity)
	webapp_user_id = models.IntegerField(default=-1)
	sign_code = models.CharField(max_length=50) #签到码
	sign_status = models.IntegerField(default=0) #是否己签到 0:未签到时1：己签到
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_activity_user_code'
		verbose_name = '活动报名用户对应签到码'
		verbose_name_plural = '活动报名用户对应签到码'

