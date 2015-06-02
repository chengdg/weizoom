# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#########################################################################
# Document：帮助文章
#########################################################################
class Document(models.Model):
	page_id = models.CharField(max_length=125, unique=True) #page的id
	title = models.CharField(max_length=125)
	content = models.TextField(default='')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'help_document'
		verbose_name = '帮助文档'
		verbose_name_plural = '帮助文档'