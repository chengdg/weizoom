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
# 调研：Research
#########################################################################
class Research(models.Model):
	owner = models.ForeignKey(User, related_name='market_tool_research_user')
	name = models.CharField(max_length=256) #调研名称
	detail = models.TextField() #活动内容
	prize_type = models.IntegerField(verbose_name='奖品类别', default=-1) #0实物，1优惠券，2兑换码，3积分，-1无奖励
	prize_source = models.CharField(max_length=100, default='', verbose_name='奖品来源')
	is_deleted = models.BooleanField(default=False) #是否删除
	is_non_member = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_research'
		verbose_name = '调研'
		verbose_name_plural = '调研'
		ordering = ['-id']

	def get_researches_by_member(self, member):
		research_ids = ItmesValue.objects.filter(member=member).values("research_id").distinct()
		researches = Research.objects.filter(id__in=research_ids)
		return researches

	@property
	def joined_users(self):
		webapp_user_ids = [value.webapp_user_id for value in ResearchItemValue.objects.filter(research=self)]
		return list(WebAppUser.objects.filter(id__in=webapp_user_ids))

	@property
	def joined_user_count(self):
		return ResearchItemValue.objects.filter(research=self).values("webapp_user_id").distinct().count()			


RESEARCHITEM_TYPE_TEXT = 0
RESEARCHITEM_TYPE_SELECT = 1
RESEARCHITEM_TYPE_IMAGE = 2
RESEARCHITEM_TYPE_CHECKBOX = 3
ITEMTYPE2TEXT = {
	RESEARCHITEM_TYPE_TEXT: u'文本输入框',
	RESEARCHITEM_TYPE_SELECT: u'选项框',
	RESEARCHITEM_TYPE_IMAGE: u'图片上传控件',
	RESEARCHITEM_TYPE_CHECKBOX: u'复选框'
}
#########################################################################
# ResearchItem: 调研用户输入项
#########################################################################
class ResearchItem(models.Model):
	RESEARCHITEM_TYPES = (
		(RESEARCHITEM_TYPE_TEXT, u"文本"),
		(RESEARCHITEM_TYPE_SELECT, u"选项"),
		(RESEARCHITEM_TYPE_IMAGE, u"图片"),
		(RESEARCHITEM_TYPE_CHECKBOX, u"复选框"),
	)
	owner = models.ForeignKey(User)
	research = models.ForeignKey(Research)
	title = models.CharField(max_length=50) #输入项的title
	type = models.IntegerField(max_length=1, choices=RESEARCHITEM_TYPES, default=RESEARCHITEM_TYPE_TEXT)  #item类型
	initial_data = models.CharField(max_length=800, null=True, default='') #  选项: ‘｜’区分
	is_mandatory = models.BooleanField(default=False) #是否必填
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_research_item'
		verbose_name = '调研Item'
		verbose_name_plural = '调研Item'


#########################################################################
# ResearchItemValue：调研Item中填写的数据
#########################################################################
class ResearchItemValue(models.Model):           
	owner = models.ForeignKey(User)
	research = models.ForeignKey(Research)
	item = models.ForeignKey(ResearchItem)
	webapp_user = models.ForeignKey(WebAppUser)
	value = models.CharField(max_length=256, null=True) #内容
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_research_item_value'
		verbose_name = '调研Item对应数据'
		verbose_name_plural = '调研Item对应数据'
