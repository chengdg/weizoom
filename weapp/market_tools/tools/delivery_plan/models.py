# -*- coding: utf-8 -*-
import random
from datetime import timedelta, datetime, date
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.db.models import F

from core import dateutil


#########################################################################
# DeliveryPlan ：套餐
#########################################################################
MONTHLY = 2
WEEKLY = 1
DAILY = 0
class DeliveryPlan(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=20, db_index=True) #名称
	product_id = models.IntegerField(default=0) #对应商品ID
	original_product_id = models.IntegerField(default=0) #生成套餐时选择的商品ID
	type = models.IntegerField(default=1) #类型 周、月、日
	frequency = models.IntegerField(default=0) #频率
	times = models.IntegerField(default=0)  #配送次数
	price = models.DecimalField(max_digits=65, decimal_places=2) #金额
	original_price = models.DecimalField(max_digits=65, decimal_places=2) #原价
	is_deleted = models.BooleanField(default=False) #是否删除
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_delivery_plan'
		verbose_name = '套餐'
		verbose_name_plural = '套餐'
		ordering = ['-created_at']
