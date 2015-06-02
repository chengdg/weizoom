# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *

import api_views

urlpatterns = patterns('',
	(r'^(\d+)/api/presented_award/get/$', api_views.get_presented_award),
	(r'^api/member_remarks_name/update/$', api_views.update_member_remarks_name),
	(r'^api/browse_record/get/$', api_views.get_browse_record),
	(r'^api/member_share/get/$', api_views.get_member_share),
)