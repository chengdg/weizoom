# -*- coding: utf-8 -*-

from django.db import models

class City(models.Model):
	name = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=50)
	province_id = models.IntegerField(db_index=True)

	class Meta(object):
		db_table = 'city'
		verbose_name = '城市列表'
		verbose_name_plural = '城市列表'

class Province(models.Model):
	name = models.CharField(max_length=50)

	class Meta(object):
		db_table = 'province'
		verbose_name = '省份列表'
		verbose_name_plural = '省份列表'


class District(models.Model):
	name = models.CharField(max_length=50)
	city_id = models.IntegerField(db_index=True)

	class Meta(object):
		db_table = 'district'
		verbose_name = '区县列表'
		verbose_name_plural = '区县列表'