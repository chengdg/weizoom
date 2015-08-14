# -*- coding: utf-8 -*-

__author__ = 'robert'

import subprocess
import sys
import os
import logging
logger = logging.getLogger('prunt-uglify')

from prunt.decorator import register_task

@register_task('prunt-uglify')
def uglify(prunt):
	u"""
	对js文件进行去除空白、混淆压缩
	"""
	prunt.config.require('files')

	files = prunt.config['files']
	paths = files['src'] if type(files['src']) == list else [files['src']]

	for path in paths:
		pos = path.rfind('.')
		prefix = path[:pos]
		suffix = path[pos+1:]
		dst_path = '%s.min.%s' % (prefix, suffix)
		cmd = 'java -Xss20m -jar disttool/yuicompressor-2.4.6.jar %s -o %s' % (path, dst_path)
		logger.info('uglify js file [%s] to [%s], use command: "%s"' % (path, dst_path, cmd))
		subprocess.call(cmd.split(' '))