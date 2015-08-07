# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class TemplateCustomModule(models.Model):
	'''
	自定义模块
	'''
	owner = models.ForeignKey(User, related_name='owned_template_custom_modules')
	name = models.CharField(max_length=120, verbose_name="名称")
	reserve = models.IntegerField(default=0, verbose_name="预留字段")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
	updated_at = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")
	is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

	class Meta(object):
		db_table = 'template_custom_module'
		verbose_name = '自定义模块'
		verbose_name_plural = '自定义模块'


class Image(models.Model):
	"""
	图片
	"""
	owner = models.ForeignKey(User, related_name="owned_termite_images")
	url = models.CharField(max_length=256, default='')  # 图片url
	width = models.IntegerField()  # width
	height = models.IntegerField()  # height
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'webapp_image'
		verbose_name = '图片'
		verbose_name_plural = '图片'



class TemplateGlobalNavbar(models.Model):
	'''
	全局导航
	'''
	owner = models.ForeignKey(User, related_name='owned_template_global_navbar')
	is_enable = models.BooleanField(default=False, verbose_name='是否启用')
	content = models.TextField(default='', verbose_name='navbar的json字符串')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="修改时间")

	class Meta(object):
		db_table = 'template_global_navbar'
		verbose_name = '全局导航'
		verbose_name_plural = '全局导航'


	def get_pages(self):
		if self._pages:
			return self._pages

		pages = PageHasGlobalNavbar.objects.filter(owner=self.owner, global_navbar=self, is_enable=True)
		if pages.count() > 0:
			self._pages = {}
			for p in pages:
				self._pages[p.page_type] = True
			return self._pages
		else:
			return {}

	@staticmethod
	def get_object(user):
		global_navbar, _ = TemplateGlobalNavbar.objects.get_or_create(
			owner=user
		)
		return global_navbar



TEMPLATE_GLOBAL_NAVBAR_WEPAGE = 'wepage'
TEMPLATE_GLOBAL_NAVBAR_HOME_page = 'home_page'

class PageHasGlobalNavbar(models.Model):
	'''
	页面对应的全局导航
	'''
	owner = models.ForeignKey(User, related_name='owned_page_has_global_navbar')
	global_navbar = models.ForeignKey(TemplateGlobalNavbar)
	page_type = models.CharField(max_length=50, default='', verbose_name='空间类型')
	is_enable = models.BooleanField(default=False, verbose_name='是否启用')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

	class Meta(object):
		db_table = 'page_has_global_navbar'
		verbose_name = '页面对应的全局导航'
		verbose_name_plural = '页面对应的全局导航'

	@staticmethod
	def get_object(user, page_type, global_navbar):
		page_global_navbar, _ = PageHasGlobalNavbar.objects.get_or_create(
			owner = user,
			global_navbar = global_navbar,
			page_type = page_type
		)
		return page_global_navbar


	@staticmethod
	def get_global_navbar(user, page_type):
		try:			
			page_global_navbar = PageHasGlobalNavbar.objects.get(
				owner = user,
				page_type = page_type,
				is_enable = True
			)
			return page_global_navbar.global_navbar
		except:
			return None

