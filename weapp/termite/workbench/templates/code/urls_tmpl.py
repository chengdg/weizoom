# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views

urlpatterns = patterns('',
	# Termite GENERATED START: url
	# MODULE START: {{instanceName}}
	(r'^editor/{{pluralInstanceName}}/$', views.list_{{pluralInstanceName}}),
	(r'^editor/{{instanceName}}/create/$', views.add_{{instanceName}}),
	(r'^editor/{{instanceName}}/update/(\d+)/$', views.update_{{instanceName}}),
	(r'^editor/{{instanceName}}/delete/(\d+)/$', views.delete_{{instanceName}}),

	{% ifequal listinfo.isEnableSort "yes" %}
	(r'^api/{{instanceName}}/display_index/update/$', api_views.update_{{instanceName}}_display_index),
	{% endifequal %}
	{% ifequal isEnablePreview "yes" %}
	(r'^api/preview_{{instanceName}}/create/$', api_views.craete_preview_{{instanceName}}),
	{% endifequal %}
	# MODULE END: {{instanceName}}
	# Termite GENERATED END: url
)