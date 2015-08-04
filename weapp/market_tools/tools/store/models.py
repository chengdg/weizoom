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
# Store ：门店信息
#########################################################################
class Store(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=256) #门店信息
	thumbnails_url = models.CharField(max_length=1024) #门店缩略图
	store_intro = models.CharField(max_length=256) #门店简介
	city = models.CharField(max_length=256) #所在地区
	address = models.CharField(max_length=256) #公司地址
	location = models.CharField(max_length=256) #公司坐标
	bus_line = models.TextField(max_length=1024) #乘车路线
	tel = models.CharField(max_length=20) #联系电话
	detail = models.TextField() #详情
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'market_tool_store'
		verbose_name = '门店信息'
		verbose_name_plural = '门店信息'

	@staticmethod
	def can_update_by(owner_id, store_id):
		#当前owner下不还有商品，微众商城表里包含商品 这样的商品不能修改
		if Store.objects.filter(owner_id=owner_id, id=store_id).count() > 0:
			return True
		else:
			return False


#########################################################################
# StoreSwipeImage ：门店轮播图
#########################################################################
class StoreSwipeImage(models.Model):
	store = models.ForeignKey(Store)
	url = models.CharField(max_length=256, default='')
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_store_swipe_image'
		verbose_name = '门店轮播图'
		verbose_name_plural = '门店轮播图'
		ordering = ['id',]


