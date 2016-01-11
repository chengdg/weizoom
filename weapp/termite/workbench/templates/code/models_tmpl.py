# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from core import dateutil

# Termite GENERATED START: model
# MODULE START: {{instanceName}}
#########################################################################
# {{className|capfirst}}：{{entityName}}
#########################################################################
class {{className|capfirst}}(models.Model):
	owner = models.ForeignKey(User)
	{% for property in properties %}
	{% ifequal property.type 'text_input' %}
	{{property.name}} = models.CharField(max_length=256) #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'richtext_input' %}
	{{property.name}} = models.TextField() #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'textarea_input' %}
	{{property.name}} = models.TextField() #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'select_input' %}
	{{property.name}} = models.CharField(max_length=50) #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'image_selector' %}
	{{property.name}} = models.CharField(max_length=1024) #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'checkbox_input' %}
	{{property.name}} = models.BooleanField(default=True) #{{property.label}}
	{% endifequal %}
	{% endfor %}
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = '{{tableName}}'
		verbose_name = '{{entityName}}'
		verbose_name_plural = '{{entityName}}'


{% ifequal isEnablePreview "yes" %}
#########################################################################
# {{previewClassName}}：{{entityName}}预览
#########################################################################
class {{previewClassName}}(models.Model):
	owner = models.ForeignKey(User)
	{% for property in properties %}
	{% ifequal property.type 'text_input' %}
	{{property.name}} = models.CharField(max_length=256) #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'richtext_input' %}
	{{property.name}} = models.TextField() #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'textarea_input' %}
	{{property.name}} = models.TextField() #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'select_input' %}
	{{property.name}} = models.CharField(max_length=50) #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'image_selector' %}
	{{property.name}} = models.CharField(max_length=1024) #{{property.label}}
	{% endifequal %}
	{% ifequal property.type 'checkbox_input' %}
	{{property.name}} = models.BooleanField(default=True) #{{property.label}}
	{% endifequal %}
	{% endfor %}
	session = models.CharField(max_length=256) #session
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = '{{tableName}}_preview'
		verbose_name = '{{entityName}}预览'
		verbose_name_plural = '{{entityName}}预览'
{% endifequal %}

{% ifequal hasSwipeImages "yes" %}
#########################################################################
# {{className}}SwipeImage：{{entityName}}的轮播图
#########################################################################
class {{className}}SwipeImage(models.Model):
	owner = models.ForeignKey(User)
	{{instanceName}} = models.ForeignKey({{className}})
	pic_url = models.CharField(max_length=256) #轮播图片地址
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = '{{tableName}}_swipe_image'
		verbose_name = '{{entityName}}轮播图'
		verbose_name_plural = '{{entityName}}轮播图'


	{% ifequal isEnablePreview "yes" %}
#########################################################################
# {{previewClassName}}SwipeImage：{{entityName}}预览
#########################################################################
class {{previewClassName}}SwipeImage(models.Model):
	owner = models.ForeignKey(User)
	preview_{{instanceName}} = models.ForeignKey({{previewClassName}})
	pic_url = models.CharField(max_length=256) #轮播图片地址
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	session = models.CharField(max_length=256) #session
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = '{{tableName}}_preview_swipe_image'
		verbose_name = '{{entityName}}预览的轮播图'
		verbose_name_plural = '{{entityName}}预览的轮播图'
	{% endifequal %}
{% endifequal %}

# MODULE END: {{instanceName}}
# Termite GENERATED END: model