# -*- coding: utf-8 -*-

__author__ = "guoliyan"


from django.conf.urls import *

import views
import api_views


urlpatterns = patterns('',

    (r'^permissions/edit/$', views.edit_weizoom_card_account_permission),


    (r'^api/', api_views.call_api),

    
)
