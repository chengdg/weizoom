# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import logging
logger = logging.getLogger('weizoom-load-termite-components')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt


@register_task('weizoom-load-termite-components')
def loadTermiteComponents(prunt):
	u"""
	加载termite component集合的内容，合并其js和html文件
	"""
	#解析components
	prunt.config.require('raw_lines')
	raw_lines = prunt.config['raw_lines']
	target_line = ''
	for line in raw_lines:
		if 'load_termite_components' in line:
			target_line = line.strip()
			break

	components_str = target_line[2:-2].strip().split('|')[0].strip()
	components = eval(components_str)

	#加载components的js和模板文件
	from weapp import settings
	from termite.workbench.templatetags import workbench_filter
	content = workbench_filter.load_termite_components(components, wrap_with_verbatim=True)
	prunt.set_last_result(content)
	
