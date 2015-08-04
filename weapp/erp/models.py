# -*- coding: utf-8 -*-

from django.db import models


#########################################################################
# ERPAuthUser
#########################################################################
class ERPAuthUser(models.Model):
	username = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'erp_authenticate'
		verbose_name = 'erp授权用户'
		verbose_name_plural = 'erp授权用户'

#########################################################################
# ERPApiRequestRecord
#########################################################################
class ERPRequestRecord(models.Model):
	username = models.CharField(max_length=100)
	ip = models.CharField(max_length=100)
	request_url = models.TextField(default='')

	class Meta(object):
		db_table = 'erp_api_request_record'
		verbose_name = 'api请求记录'
		verbose_name_plural = 'api请求记录'