# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import logging
logger = logging.getLogger('weizoom-load-app-views-dialogs')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt


@register_task('weizoom-load-app-views-dialogs')
def loadAppViewsAndDialogs(prunt):
	u"""
	合并app的views, dialogs
	"""
	#解析app name
	prunt.config.require('raw_lines')
	raw_lines = prunt.config['raw_lines']
	target_line = ''
	for line in raw_lines:
		if 'load_app_views_and_dialogs' in line:
			target_line = line.strip()
			break

	app_name = target_line[2:-2].strip().split('|')[0].strip()
	app_name = eval(app_name)

	#加载components的js和模板文件
	from weapp import settings
	from apps.templatetags import apps_filter
	content = '{%% verbatim %%}%s{%% endverbatim %%}' % apps_filter.load_app_views_and_dialogs(app_name).decode('utf-8').encode('utf-8')
	print content
	prunt.set_last_result(content)
	
