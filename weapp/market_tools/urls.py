# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf.urls import *
from django.core.urlresolvers import (RegexURLPattern, RegexURLResolver)

import views
import api_views

urlpatterns = patterns('',
	(r'^$', views.show_dashboard),
	#(r'^api/', api_views.call_api),
)

from market_tools import ToolModule

for tool_module in ToolModule.all_tool_modules():
	if not hasattr(tool_module.urls, 'urlpatterns'):
		continue

	regex = r'^'+tool_module.module_name+r'/'
	urlpatterns.append(
        RegexURLResolver(regex, tool_module.urls.urlpatterns, None, None, None)
		)