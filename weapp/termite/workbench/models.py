# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from termite.core import dateutil
from webapp import models as webapp_models


Workspace = webapp_models.Workspace
Project = webapp_models.Project


########################################################################
# PageTemplate: 页面的模板
########################################################################
class PageTemplate(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50) #模板名
	project_type = models.CharField(max_length=50) #项目类型
	display_index = models.IntegerField(default=1) #页面顺序, reserved
	page_json = models.TextField() #json内容
	image_data = models.TextField() #图片base64编码格式
	created_at = models.DateTimeField(auto_now=True) #添加时间

	class Meta(object):
		db_table = 'workbench_page_template'
		verbose_name = '页面模板'
		verbose_name_plural = '页面模板'
