# -*- coding: utf-8 -*-

from django.conf.urls import *

import views as watchdog_view

urlpatterns = patterns('',
	(r'^$', watchdog_view.list),
	(r'^create/$', watchdog_view.create_watchdog),
#    (r'^list/(\d+)/$', watchdog_view.list),
#    (r'^delete/(\d+)/$', watchdog_view.delete),
#    (r'^delete_all/(\d+)/$', watchdog_view.delete_all),
#    (r'^newest_error/$', watchdog_view.get_newest_error),
#    (r'^newest_fatal/$', watchdog_view.get_newest_fatal),
#    (r'^operations/$', watchdog_view.get_operation_infos),
#    (r'^write_api_infos/$', watchdog_view.write_api_infos),
)