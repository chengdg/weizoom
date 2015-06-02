# -*- coding: utf-8 -*-

__author__ = 'taol'

from django.conf.urls import *

import mobile_views
import mobile_api_views

urlpatterns = patterns('',
    url(r'^orders/get', mobile_views.get_orders),
)