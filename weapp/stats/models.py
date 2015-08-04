# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import json
import time


class BrandValueHistory(models.Model):
	"""
	记录品牌价值的历史
	"""
	#owner = models.ForeignKey(User, related_name='brand_values')
	webapp_id = models.CharField(max_length=16, verbose_name='对应的webapp id')
	value_date = models.DateField()
	value = models.FloatField(default=0.0)
	# 用户评价年度消费金额
	user_avg_consumption = models.FloatField(default=0.0)
	buyer_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'stats_brand_value_history'
		verbose_name = '微品牌价值'
		verbose_name_plural = '微品牌价值'
		unique_together = ('webapp_id', 'value_date')
