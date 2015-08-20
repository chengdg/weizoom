# -*- coding: utf-8 -*-

__author__ = 'robert'

import subprocess
import sys
import os
import glob
import logging
logger = logging.getLogger('prunt-cdn')

from prunt.decorator import register_task

@register_task('prunt-cdn')
def uploadToCDN(prunt):
	u"""
	将文件上传到CDN
	"""
	from core import upyun_util

	prunt.config.require('rules')
	rules = prunt.config['rules']
	for rule in rules:
		dest_dir = rule['dest']
		patterns = rule['pattern'] if type(rule['pattern']) == list else [rule['pattern']]

		for pattern in patterns:
			files = glob.glob(pattern)
			for src_path in files:
				cdn_path = '%s/%s' % (dest_dir, os.path.basename(src_path))
				logger.info('upload local file [%s] to cdn [%s]', src_path, cdn_path)
				upyun_util.upload_static_file(src_path, cdn_path, True)