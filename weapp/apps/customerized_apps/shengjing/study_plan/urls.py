# -*- coding: utf-8 -*-

__author__ = 'guoliyan'

from django.conf.urls import *

import mobile_views
import mobile_api_views

urlpatterns = patterns('',
    url(r'^$', mobile_views.get_study_plan),
    url(r'^course/list/$', mobile_views.list_course),
#    url(r'^api/course/apply/$', mobile_api_views.apply_course),
)