# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import views
import dev_views
import js_views

urlpatterns = patterns('',

	(r'^js/config/$', js_views.config),
	(r'^js/renovate/$', js_views.renovate),
	
	(r'^register/$', dev_views.register),

	(r'^api/m/message_to_mp/create/$', dev_views.create_message_to_mp),
	(r'^api/signature/create/$', dev_views.create_signature),

	(r'^message/qa/', include('weixin.message.qa.urls')),
	(r'^message/material/', include('weixin.message.material.urls')),
	(r'^message/message/', include('weixin.message.message.urls')),

	(r'^manage/', include('weixin.manage.urls')),
	(r'^statistics/', include('weixin.statistics.urls')),

	(r'^(\d+)/$', views.handle),
	(r'^component/receiveauthcode/$', views.receiveauthcode),
	(r'^appid/(.*)/$', views.component_handle),
)