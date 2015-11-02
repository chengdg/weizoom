# -*- coding: utf-8 -*

__author__ = 'chuter'

from django.contrib import admin

from models import *

class WeiZoomCardManagerAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'username', 'nickname')
	list_display_links = ('user',)
	list_filter = ('user',)


	
admin.site.register(WeiZoomCardManager, WeiZoomCardManagerAdmin)
