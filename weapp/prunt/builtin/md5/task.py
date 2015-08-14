# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import hashlib
import os
import shutil
import logging
logger = logging.getLogger('prunt-md5')

from prunt.decorator import register_task

@register_task('prunt-md5')
def md5(prunt):
	u"""
	将文件名替换为新的文件名（文件名_文件内容摘要），比如a.js替换为a_${md5}.js
	"""
	prunt.config.require('files')

	files = prunt.config['files']
	paths = files['src'] if type(files['src']) == list else [files['src']]

	for path in paths:
		src_file = open(path, 'rb')
		content = src_file.read()
		src_file.close()

		md5 = hashlib.md5(content)
		digest = md5.hexdigest()

		#生成md5摘要后的文件
		pos = path.rfind('.')
		prefix = path[:pos]
		suffix = path[pos+1:]
		new_path = '%s_%s.%s' % (prefix, digest, suffix)
		shutil.copyfile(path, new_path)
		logger.info('generate md5 file %s for %s', new_path, path)
	