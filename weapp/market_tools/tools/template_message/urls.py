# -*- coding: utf-8 -*-

__author__ = "bert"


from django.conf.urls import *

import views
import api_views


urlpatterns = patterns('',
   (r'^$', views.list_template_message),
   (r'^api/', api_views.call_api),
   
   (r'^edit_detail/$', views.edit_template_message_detail),
)
