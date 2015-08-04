# -*- coding: utf-8 -*-

from django.conf.urls import *
import qq_view
import weibo_view

urlpatterns = patterns('',
	(r'(\d+)/qq/login/$', qq_view.login_redirect),

	(r'qq/login_callback/$', qq_view.login_callback_handler),


	(r'(\d+)/weibo/login/$', weibo_view.login_redirect),

	(r'weibo/login_callback/$', weibo_view.login_callback_handler),

)