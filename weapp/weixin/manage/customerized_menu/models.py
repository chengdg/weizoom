# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.db import models
from django.contrib.auth.models import User

from weixin.message.qa.models import TEXT_TYPE, NEWS_TYPE

#########################################################################
# CustomerMenuItem：自定义菜单项
#########################################################################
FATHER_ID_NO_FATHER = 0

MENU_ITEM_TYPE_KEYWORD = 1
MENU_ITEM_TYPE_LINK = 2
MENU_ITEM_TYPES = (
	(MENU_ITEM_TYPE_KEYWORD, '关键词'),
	(MENU_ITEM_TYPE_LINK, '链接')
	)
class CustomerMenuItem(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=256) #名称
	type = models.IntegerField(default=MENU_ITEM_TYPE_KEYWORD, choices=MENU_ITEM_TYPES) #类型
	url = models.CharField(max_length=256, default='') #连接地址
	rule_id = models.IntegerField(default=0) #关键词Rule的id
	is_active = models.BooleanField(default=True) #是否启用
	father_id = models.IntegerField(default=FATHER_ID_NO_FATHER) #父级id
	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'weixin_menu_item'
		verbose_name = '自定义菜单项'
		verbose_name_plural = '自定义菜单项'