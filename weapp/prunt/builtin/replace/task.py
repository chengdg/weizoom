# -*- coding: utf-8 -*-

__author__ = 'robert'

import subprocess
import sys
import os
import logging
logger = logging.getLogger('prunt-replace')

from prunt.decorator import register_task

@register_task('prunt-replace')
def replace(prunt):
	u"""
	对文本文件内容进行简单的文本替换（目前不支持正则表达式）
	"""
	prunt.config.require('rules')
	prunt.config.require('files')

	files = prunt.config['files']
	paths = files['src'] if type(files['src']) == list else [files['src']]

	rules = prunt.config['rules']

	for path in paths:
		src_file = open(path, 'rb')
		content = src_file.read()
		src_file.close()

		for rule in rules:
			content = content.replace(rule['pattern'], rule['replacement'])
			logger.info('replace file [%s], change "%s" to "%s"' % (path, rule['pattern'], rule['replacement']))

		dst_file = open(path, 'wb')
		print >> dst_file, content
		dst_file.close()