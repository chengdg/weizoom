# -*- coding: utf-8 -*
from django.contrib import admin

from order.account.models import FreightUser, get_make_password

class FreightUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'username', 'password', 'status')
	list_display_links = ('owner',)

	def save_model(self, request, obj, form, change):
		obj.password = get_make_password(obj.password)
		obj.save()

admin.site.register(FreightUser, FreightUserAdmin)
