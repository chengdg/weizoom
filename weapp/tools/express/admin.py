# -*- coding: utf-8 -*

__author__ = 'chuter'

from django.contrib import admin

from models import *

class ExpressServiceConfigAdmin(admin.ModelAdmin):
	list_display = ('name', 'value')


admin.site.register(ExpressServiceConfig, ExpressServiceConfigAdmin)
