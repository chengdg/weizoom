# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.db import models
from django.contrib.auth.models import User


####################################################
# MarketToolAuthority: 营销工具权限
####################################################
class MarketToolAuthority(models.Model):
	owner = models.ForeignKey(User)
	is_enable_market_tool = models.BooleanField(default=False, verbose_name=u'是否启用营销工具') #是否启用营销工具

	class Meta(object):
		db_table = 'market_tool_authority'
		verbose_name = '营销工具权限'
		verbose_name_plural = '营销工具权限'


########################################################################
# OperatePermission: 用于生成控制营销工具访问权限的content type
########################################################################
class OperatePermission(models.Model):
	class Meta(object):
		managed = False