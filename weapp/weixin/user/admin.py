# -*- coding: utf-8 -*

__author__ = 'bert'

from django.contrib import admin

from models import *

class WeixinMpUserAccessTokenAdmin(admin.ModelAdmin):
	list_display = ('id', 'mpuser', 'app_id', 'app_secret', 'access_token', 'update_time', 'expire_time')
	list_display_links = ('mpuser',)
	list_filter = ('mpuser',)

class WeixinMpUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'username', 'is_active')
	list_display_links = ('id',)
	list_filter = ('owner', 'username',)

class MpuserPreviewInfoAdmin(admin.ModelAdmin):
	list_display = ('mpuser', 'name', 'image_path')
	list_display_links = ('mpuser',)
	list_filter = ('mpuser', 'name',)	

class ComponentInfoAdmin(admin.ModelAdmin):
	list_display = ('app_id', 'app_secret', 'component_verify_ticket', 'token', 'ase_key', 'component_access_token', 'last_update_time')
	list_filter = ('app_id', 'app_secret',)	

admin.site.register(WeixinMpUserAccessToken, WeixinMpUserAccessTokenAdmin)
admin.site.register(WeixinMpUser, WeixinMpUserAdmin)
admin.site.register(MpuserPreviewInfo, MpuserPreviewInfoAdmin)
admin.site.register(ComponentInfo, ComponentInfoAdmin)