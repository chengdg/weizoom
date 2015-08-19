# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging
logger = logging.getLogger('weizoom-merge')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt

@register_task('weizoom-merge')
def weizoomMerge(prunt):
	u"""
	将js, css文件进行concat和uglify操作
	"""
	prunt.config.require('files')
	files = prunt.config['files']
	paths = files['src'] if type(files['src']) == list else [files['src']]

	prunt.config.require('dest')
	dest = prunt.config['dest']

	path_map = prunt.config.get('path_map', None)

	logger.info('merge %s', paths)

	prunt.run_task('prunt-concat', {
		"files": {
			"src": paths,
			"dest": dest
		},
		"comment": "/* comment */",
		"path_map": path_map
	})

	src = dest
	prunt.run_task('prunt-md5', {
		"files": {
			"src": src
		}
	})

	src = prunt.get_last_result()
	prunt.run_task('prunt-uglify', {
		"files": {
			"src": src
		}
	})
