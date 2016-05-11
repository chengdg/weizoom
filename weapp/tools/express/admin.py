# -*- coding: utf-8 -*

__author__ = 'chuter'

from django.contrib import admin
from models import *
from django.contrib import messages

class ExpressServiceConfigAdmin(admin.ModelAdmin):
	fields = ('name',)
	list_display = ('name', 'value')
	actions = ['make_on',]

	def make_on(self ,request, queryset):
		if queryset.count() > 1:
			self.message_user(request,'只能选择1个快递服务商', messages.WARNING)
		else:
			ExpressServiceConfig.objects.all().update(value=0)
			queryset.update(value=1)
	make_on.short_description = "开启快递服务商"
admin.site.register(ExpressServiceConfig, ExpressServiceConfigAdmin)
