# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import F

from core import dateutil

#########################################################################
# MessageDailyStatistics: 每日消息统计
#########################################################################
class MessageDailyStatistics(models.Model):
	owner = models.ForeignKey(User)
	count = models.IntegerField(default=0) #消息数
	data_date = models.DateField(auto_now_add=True) #统计日期

	class Meta(object):
		db_table = 'app_weixin_message_daily_statistics'
		verbose_name = 'app每日消息统计'
		verbose_name_plural = 'app每日消息统计'
		unique_together = ['data_date', 'owner']

#########################################################################
# WeixinUserDailyStatistics: 每日新增统计
#########################################################################
class WeixinUserDailyStatistics(models.Model):
	owner = models.ForeignKey(User)
	count = models.IntegerField(default=1) #新增微信用户数
	data_date = models.DateField(auto_now_add=True) #统计日期

	class Meta(object):
		db_table = 'app_weixin_user_daily_statistics'
		verbose_name = 'app每日新增微信用户统计'
		verbose_name_plural = 'app每日新增微信用户统计'
		unique_together = ['data_date', 'owner']

#===============================================================================
# increase_weixin_user_statistics : 增加weixin user统计计数
#===============================================================================
def increase_weixin_user_statistics(user):
	today = dateutil.get_today()
	count = WeixinUserDailyStatistics.objects.filter(data_date=today, owner=user).count()
	if count > 0:
		WeixinUserDailyStatistics.objects.filter(data_date=today, owner=user).update(count = F('count') + 1)
	else:
		WeixinUserDailyStatistics.objects.create(owner=user, count=1)

#===============================================================================
# decrease_weixin_user_statistics : 减少weixin user统计计数
#===============================================================================
def decrease_weixin_user_statistics(user):
	today = dateutil.get_today()
	count = WeixinUserDailyStatistics.objects.filter(data_date=today, owner=user).count()
	if count > 0:
		WeixinUserDailyStatistics.objects.filter(data_date=today, owner=user).update(count = F('count') - 1)
	else:
		WeixinUserDailyStatistics.objects.create(owner=user, count=-1)
