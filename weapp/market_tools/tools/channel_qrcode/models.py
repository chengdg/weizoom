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
# 渠道扫码：ChannelQrcodeSettings
#########################################################################
class ChannelQrcodeSettings(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=500, verbose_name=u'渠道名称')
	award_prize_info = models.TextField(default='{"id":-1,"name":"no-prize"}', verbose_name=u'奖品信息')
	reply_type = models.IntegerField(max_length=1, default=0)  #扫码后行为：0普通关注一致，1回复文字，2回复图文
	reply_detail = models.TextField(verbose_name=u'回复文字', default='') #reply_type为1时有效
	reply_material_id = models.IntegerField(default=0) #素材id，reply_type为2时有效
	remark = models.CharField(max_length=500, verbose_name=u'备注')
	ticket = models.TextField() #获取的ticket值
	grade_id = models.IntegerField(default=-1) #关注后等级id
	re_old_member = models.IntegerField(default=0) #是否关联已关注会员
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_channel_qrcode_setting'
		verbose_name = '渠道扫码配置'
		verbose_name_plural = '渠道扫码配置'
		ordering = ['-id']

class ChannelQrcodeHasMember(models.Model):
	channel_qrcode = models.ForeignKey(ChannelQrcodeSettings)
	member = models.ForeignKey(Member)
	is_new = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	
	class Meta(object):
		db_table = 'market_tool_channel_qrcode_has_member'
		verbose_name = '渠道扫码配置'
		verbose_name_plural = '渠道扫码配置'

