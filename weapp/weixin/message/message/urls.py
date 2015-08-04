# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	#实时消息
	(r'^$', views.list_timelines),

	(r'^session_history/show/$', views.show_history),
	(r'^collect_message/list/$', views.list_collect_message),

	(r'^api/collect/message/$', api_views.collect_message),
	(r'^api/custome_message/create/$', api_views.send_custome_message),
	(r'^api/sessions/get/$', api_views.get_sessions),
	(r'^api/session/reply/write_back/$', api_views.reply_session_write_back),
	(r'^api/session/delete/$', api_views.delete_session),
	(r'^api/session/enable/$', api_views.enable_session),
	(r'^api/session_history/get/$', api_views.get_session_histories),

	(r'^api/realtime_unread_count/get/$', api_views.get_realtime_unread_count),
	(r'^api/realtime_unread_count/reset/$', api_views.reset_realtime_unread_count),
	
	(r'^api/messages/get/$', api_views.get_messages),

)

