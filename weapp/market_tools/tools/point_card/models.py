# -*- coding: utf-8 -*-
import random
from datetime import timedelta, datetime, date
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from core import dateutil


#########################################################################
# PointCardRule ：充值卡规则
#########################################################################
class PointCardRule(models.Model):
	owner = models.ForeignKey(User, related_name='owned_point_card_rules')
	name = models.CharField(max_length=20, db_index=True) #名称
	prefix = models.CharField(max_length=20, db_index=True) #卡号前辍
	point = models.IntegerField(default=0) #包含积分
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	@staticmethod
	def get_all_point_card_rules_list(user):
		if user is None:
			return []

		return list(PointCardRule.objects.filter(owner=user))

	class Meta(object):
		db_table = 'market_tool_point_card_rule'
		verbose_name = '充值卡规则'
		verbose_name_plural = '充值卡规则'
		ordering = ['-id']


#########################################################################
# PointCard ：充值卡
#########################################################################
#充值卡状态
POINT_CARD_STATUS_UNUSED = 0 #未使用
POINT_CARD_STATUS_USED = 1 #已被使用
COUPON_STATUS_EXPIRED = 2 #已过期

POINT_CARD_STATUS2POINT_CARD_STATUS_STR = {
		0: u'未使用',
		1: u'已使用',
		2: u'已过期',
}

class PointCard(models.Model):
	owner = models.ForeignKey(User)
	point_card_rule = models.ForeignKey(PointCardRule) 
	member_id = models.IntegerField(default=0) #充值卡分配的member的id
	status = models.IntegerField(default=POINT_CARD_STATUS_UNUSED) #充值卡状态
	point_card_id = models.CharField(max_length=50) #充值卡号
	password = models.CharField(max_length=50) #充值卡密码
	provided_time = models.DateTimeField(auto_now_add=True) #发放时间
	point = models.IntegerField(default=0) #积分
	is_manual_generated = models.BooleanField(default=False) #是否手工生成
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_point_card'
		verbose_name = '充值卡'
		verbose_name_plural = '充值卡'
		ordering = ['-id']
		unique_together = ('point_card_id',)
		
	@staticmethod
	def get_all_point_cards(user):
		if user is None:
			return []

		return list(PointCard.objects.filter(owner=user))

