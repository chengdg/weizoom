# -*- coding: utf-8 -*

__author__ = 'chuter'

from django.contrib import admin

from models import *

class UserAlipayOrderConfigAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'partner', 'key', 'private_key', 'ali_public_key', \
			'input_charset', 'sign_type', 'seller_email')
	list_display_links = ('owner',)
	list_filter = ('owner',)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'webapp_id', 'is_mp_registered', 'system_name', 'system_version')
	list_display_links = ('id',)
	list_filter = ('webapp_id',)
	
admin.site.register(UserAlipayOrderConfig, UserAlipayOrderConfigAdmin)
admin.site.register(UserProfile, UserProfileAdmin)