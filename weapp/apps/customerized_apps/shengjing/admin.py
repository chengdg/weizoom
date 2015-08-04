# -*- coding: utf-8 -*

__author__ = 'chuter'

from django.contrib import admin

from models import *

class ShengjingEmailSettingsAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'course_registration_email')
	list_display_links = ('owner',)
	list_filter = ('owner',)
	
admin.site.register(ShengjingEmailSettings, ShengjingEmailSettingsAdmin)