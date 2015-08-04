# -*- coding: utf-8 -*

from django.contrib import admin
from django.contrib.auth.models import User

from models import Notice

#向站内不是自己、amdin、manager所有用户发通知
def send_all_user(self, request, queryset):
	all_user = User.objects.all()
	for notice_content in queryset:
		for user in all_user:
			if 'admin' == user.username or 'manager' == user.username or user.id == notice_content.owner_id:
				continue
			else:
				Notice(owner_id=user.id,title=notice_content.title,content=notice_content.content,create_time=notice_content.create_time,has_read=False).save()
send_all_user.short_description = "向站内所有人通告"


class NoticeAdmin(admin.ModelAdmin):
	actions = [send_all_user,]
	search_fields = ('title', 'content')
	list_filter = ('has_read', 'owner_id',)
	list_display = ('show_username', 'title', 'content', 'create_time', 'has_read', 'create_time')
admin.site.register(Notice, NoticeAdmin)

