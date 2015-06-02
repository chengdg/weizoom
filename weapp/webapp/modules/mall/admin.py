# -*- coding: utf-8 -*-

__author__ = 'lizhengxue'

from django.contrib import admin

from webapp.modules.mall.models import WeizoomMall, WeizoomMallHasOtherMallProduct

class WeizoomMallAdmin(admin.ModelAdmin):
	list_display = (
		'webapp_id', 
		'is_active',
		)
	list_display_links = ('webapp_id',)
	list_filter = ('webapp_id',)


admin.site.register(WeizoomMall, WeizoomMallAdmin)
