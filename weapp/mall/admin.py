# -*- coding: utf-8 -*-
from django.contrib import admin

from .notices_models import Notice


class NoticeAdmin(admin.ModelAdmin):
    fields = ['title', 'content']


admin.site.register(Notice, NoticeAdmin)
