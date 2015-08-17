# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import logging
logger = logging.getLogger('weizoom-merge-views-dialogs')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt

from utils import resource_util

def merge_weapp_views_and_dialogs(target_js_path, target_template_path):
	version = '2'

	src_js_paths = []
	template_sources = []

	for model in resource_util.get_web_models(version):
		src_js_paths.append(model['js_file_path'])

	for view in resource_util.get_web_views(version):
		src_js_paths.append(view['js_file_path'])
		template_sources.append('\n<!--')
		template_sources.append('content from %s' % view['template_file_path'])
		template_sources.append('-->')
		template_sources.append(view['template_source'])

	for dialog in resource_util.get_web_dialogs(version):
		src_js_paths.append(dialog['js_file_path'])
		template_sources.append('\n<!--')
		template_sources.append('content from %s' % dialog['template_file_path'])
		template_sources.append('-->')
		template_sources.append(dialog['template_source'])

	#合并js内容
	dst_js = open(target_js_path, 'wb')
	for src_js_path in src_js_paths:
		lines = []
		lines.append("\n/****************************************************/")
		lines.append('/* js from %s' % src_js_path)
		lines.append("/****************************************************/")
		src_file = open(src_js_path, 'rb')
		lines.append(src_file.read())
		lines.append(';') #避免缺少分号导致的异常函数调用
		src_file.close()
		print >> dst_js, "\n".join(lines)
	dst_js.close()
	logger.info('write all view|dialog|model js files into %s', target_template_path)

	#合并template内容
	dst_template_file = open(target_template_path, 'wb')
	print >> dst_template_file, '\n'.join(template_sources)
	dst_template_file.close()
	logger.info('write all view|dialog template files into %s', target_template_path)


@register_task('weizoom-merge-views-dialogs')
def weizoomMergeViewsDialogs(prunt):
	u"""
	将weapp的views和dialogs的js和template文件归一
	"""
	prunt.config.require('dest')
	dest = prunt.config['dest']

	#合并weapp的views, dialogs相关文件
	target_weapp_views_dialogs_js_path = dest['js']
	target_weapp_views_dialogs_template_path = dest['template']
	merge_weapp_views_and_dialogs(target_weapp_views_dialogs_js_path, target_weapp_views_dialogs_template_path)

	src = target_weapp_views_dialogs_js_path
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

	prunt.set_last_result({
		"js": prunt.get_last_result(),
		"template": target_weapp_views_dialogs_template_path
	})
