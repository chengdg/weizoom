# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import mobile_views

urlpatterns = patterns('',
	(r'^(\d+)/$', mobile_views.show_index),

	# Termite GENERATED START: mobile_url
	# MODULE START: {{instanceName}}
	(r'^{{pluralInstanceName}}/(\d+)/$', mobile_views.list_{{pluralInstanceName}}),
	(r'^{{instanceName}}/(\d+)/(\d+)/$', mobile_views.show_{{instanceName}}),
	# MODULE END: {{instanceName}}
	# Termite GENERATED END: mobile_url
)