# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from core import dateutil


#########################################################################
# Category：文章分类
#########################################################################
class Category(models.Model):
	owner = models.ForeignKey(User, related_name='owned_cms_categories')
	name = models.CharField(max_length=256) #分类名
	pic_url = models.CharField(max_length=1024, default='') #分类图片
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'cms_category'
		verbose_name = '文章分类'
		verbose_name_plural = '文章分类'


#########################################################################
# Article：文章
#########################################################################
class Article(models.Model):
	owner = models.ForeignKey(User, related_name='owned_cms_articles')
	title = models.CharField(max_length=256) #标题
	summary = models.CharField(max_length=256, default='') #摘要
	content = models.TextField(default='') #内容
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'cms_article'
		verbose_name = '文章'
		verbose_name_plural = '文章'


#########################################################################
# SpecialArticle：特殊文章
#########################################################################
class SpecialArticle(models.Model):
	owner = models.ForeignKey(User, related_name='owned_cms_special_articles')
	name = models.CharField(max_length=256) #内部名
	title = models.CharField(max_length=256) #标题
	content = models.TextField(default='') #内容
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'cms_special_article'
		verbose_name = '特殊文章'
		verbose_name_plural = '特殊文章'


#########################################################################
# CategoryHasArticle：<category, article>关系
#########################################################################
class CategoryHasArticle(models.Model):
	article = models.ForeignKey(Article)
	category = models.ForeignKey(Category)
	
	class Meta(object):
		db_table = 'cms_category_has_article'
