# -*- coding: utf-8 -*
__author__ = 'liupeiyu'

from django.contrib import admin
from models import CloudUser

class CloudUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'phone_number', 'captcha', 'status')
	list_display_links = ('owner',)

	def save_model(self, request, obj, form, change):
		# obj.password = get_make_password(obj.password)
		obj.save()

admin.site.register(CloudUser, CloudUserAdmin)
