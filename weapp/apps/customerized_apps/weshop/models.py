# -*- coding: utf-8 -*-
__author__ = 'jiangzhe'

from django.db import models
from django.contrib.auth.models import User

#===============================================================================
# ShengjingBindingMember: ShengjingBindingMember 手机号绑定的weapp会员
#===============================================================================
class WeshipMemberRelation(models.Model):
	weshop_openid = models.CharField(max_length=64, verbose_name='商城openid')
	tenant_openid = models.CharField(max_length=64, verbose_name='商户openid')
	tenant_user = models.ForeignKey(User, verbose_name='商户User')
	class Meta(object):
		db_table = 'weshop_member_relation'
		verbose_name = '微众商城会员-商户会员关系表'
		verbose_name_plural = '微众商城会员-商户会员关系表'