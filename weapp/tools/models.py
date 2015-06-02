# -*- coding: utf-8 -*-
from django.db import models


#########################################################################
# Weather ：天气
#########################################################################
class Weather(models.Model):
	info = models.TextField(verbose_name="天气信息")
	update_span = models.IntegerField(default=60, verbose_name="间隔60分钟更新数据")
	update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")
	city_code =  models.CharField(max_length=30, verbose_name="城市代码")

	class Meta(object):
		db_table = 'tool_weather'
		verbose_name = '景点天气'
		verbose_name_plural = '景点天气'