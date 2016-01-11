# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.contrib import admin

from models import IntegralStrategySttings, MemberIntegralLog, Member

class IntegralStrategySttingsAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'webapp_id', 
		'click_shared_url_increase_count_after_buy',
		'click_shared_url_increase_count_before_buy',
		'buy_award_count_for_buyer',
		'buy_via_shared_url_increase_count_for_author',
		'be_member_increase_count',
		'increase_integral_count_for_brring_customer_by_qrcode',
		'integral_each_yuan',
		)
	list_display_links = ('webapp_id',)
	list_filter = ('webapp_id',)

class MemberIntegralLogAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'event_type', 
		'integral_count',
		'created_at'
		)
	list_display_links = ('id',)
	list_filter = ('id',)

class MemberAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'token', 
		'webapp_id',
		'username_hexstr',
		'integral',
		'experience',
		'remarks_name',
		'grade',
		'is_for_test',
		'created_at'
		)
	list_display_links = ('id', 'username_hexstr')
	list_filter = ('id', 'username_hexstr')
	

admin.site.register(IntegralStrategySttings, IntegralStrategySttingsAdmin)
admin.site.register(MemberIntegralLog, MemberIntegralLogAdmin)
admin.site.register(Member, MemberAdmin)
