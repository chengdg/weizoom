# -*- coding: utf-8 -*-

__author__ = "paco bert"

from django.conf.urls import *
import views
import api_views
import mobile_views

urlpatterns = patterns('',
	(r'^$', views.member_qrcode_settings),
	# (r'^add/$', views.add_vote),
	# (r'^update/(\d+)/$', views.update_vote),
	# (r'^delete/(\d+)/$', views.delete_vote),
	# (r'^vote_statistics/(\d+)/$', views.show_vote_statistics),
	
	(r'^api/member_qrcode/edit/$', api_views.edit_member_qrcode_settings),
	(r'^api/member_qrcode/get/$', api_views.get_member_qrcode_ticket),
	(r'^member_qrcode/get/$', mobile_views.get_settings),
	#(r'^api/', api_views.call_api),
)