# -*- coding: utf-8 -*

__author__ = 'chuter'

from django.contrib import admin

from models import *

class MarketToolAuthorityAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'is_enable_market_tool')
	list_display_links = ('owner',)
	list_filter = ('owner',)
	
admin.site.register(MarketToolAuthority, MarketToolAuthorityAdmin)