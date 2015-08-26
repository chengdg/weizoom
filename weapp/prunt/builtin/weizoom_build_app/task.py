# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import logging
logger = logging.getLogger('weizoom-build-app')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt


@register_task('weizoom-build-app')
def buildApp(prunt):
	u"""
	构建app中的各种文件(workbench.html)
	"""
	apps_dir = './apps/customerized_apps'
	for dir in os.listdir(apps_dir):
		app_dir = os.path.join(apps_dir, dir)
		if not os.path.isdir(app_dir):
			continue
		init_file = os.path.join(app_dir, '__init__.py')
		if not os.path.exists(init_file):
			continue

		is_restful_app = False
		with open(init_file, 'rb') as src_file:
			for line in src_file:
				line = line.strip()
				if 'is_restful_app' in line and 'True' in line:
					if not line[0] == '#':
						is_restful_app = True
						break

		if not is_restful_app:
			logger.warn('%s is not a RESTFUL app', app_dir)
			continue

		logger.info('build app %s', app_dir)

		app_templates_dir = os.path.join(app_dir, 'templates')
		for root, dirs, files in os.walk(app_templates_dir):
			for file in files:
				if not file.endswith('.html'):
					continue

				app_template_file_path = os.path.join(root, file)
				with open(app_template_file_path, 'rb') as app_template_file:
					content = app_template_file.read()

				if not ('<!-- *start_prunt_task* -->' in content and '<!-- *end_prunt_task* -->' in content):
					continue

				prunt.run_task('weizoom-build', {
					"files": {
						"src": app_template_file_path
					}
				})
