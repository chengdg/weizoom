# -*- coding: utf-8 -*-
"""@package utils.resource_util

"""

import os
from django.conf import settings
__author__ = 'robert'


def get_web_dialogs(version):
	"""
	获得web页面的dialog的资源
	"""

	#搜集所有的可能包含js/dialog的目录
	dirs = []
	if version == '1':
		WEAPP_WEB_DIALOG_DIRS = settings.WEAPP_WEB_DIALOG_DIRS
	elif version == '2':
		WEAPP_WEB_DIALOG_DIRS = settings.WEAPP_WEB_DIALOG_DIRS_V2
	else:
		WEAPP_WEB_DIALOG_DIRS = settings.WEAPP_WEB_DIALOG_DIRS_APPS

	for url_path, weapp_dialog_dir_path in WEAPP_WEB_DIALOG_DIRS:
		if weapp_dialog_dir_path.endswith('*'):
			weapp_dialog_dir_path = weapp_dialog_dir_path[:-2]
			for f in os.listdir(weapp_dialog_dir_path):
				if os.path.isdir(os.path.join(weapp_dialog_dir_path, f)):
					dirs.append({
						'module_parent': weapp_dialog_dir_path,
						'module': f,
						'url_path': url_path
					})
		else:
			dirs.append({
				'module_parent': weapp_dialog_dir_path,
				'module': '',
				'url_path': url_path
			})

	#获取包含js/dialog的目录
	dialogs = []
	for dir in dirs:
		dialogs_dir_path = os.path.join(dir['module_parent'], dir['module'], 'js/dialog')

		if not os.path.exists(dialogs_dir_path):
			continue

		for dialog_dir in os.listdir(dialogs_dir_path):
			if not os.path.isdir(os.path.join(dialogs_dir_path, dialog_dir)):
				continue

			if dialog_dir[0] == '.':
				#skip .svn directory
				continue
				
			#读取dialog.html的内容
			template_file_path = os.path.join(dialogs_dir_path, dialog_dir, 'dialog.html')
			if os.path.exists(template_file_path):
				src_file = open(template_file_path, 'rb')
				template_source = src_file.read()
				src_file.close()
			else:
				template_source = ''

			#获取js文件信息
			js_file_path = os.path.join(dialogs_dir_path, dialog_dir, 'dialog.js')
			if (dir['module']):
				js_url_path = '/%s/%s/js/dialog/%s/dialog.js' % (dir['url_path'], dir['module'], dialog_dir)
			else:
				js_url_path = '/%s/js/dialog/%s/dialog.js' % (dir['url_path'], dialog_dir)

			dialogs.append({
				'template_file_path': template_file_path,
				'template_source': template_source,
				'js_file_path': js_file_path,
				'js_url_path': js_url_path
			})
	return dialogs


def get_web_views(version):
	"""
	获得web页面的view的资源
	"""
	dirs = []
	if version == '1':
		WEAPP_WEB_VIEW_DIRS = settings.WEAPP_WEB_VIEW_DIRS
	elif version == '2':
		WEAPP_WEB_VIEW_DIRS = settings.WEAPP_WEB_VIEW_DIRS_V2
	else:
		WEAPP_WEB_VIEW_DIRS = settings.WEAPP_WEB_VIEW_DIRS_APPS
	for url_path, weapp_view_dir_path in WEAPP_WEB_VIEW_DIRS:
		if weapp_view_dir_path.endswith('*'):
			weapp_view_dir_path = weapp_view_dir_path[:-2]
			for f in os.listdir(weapp_view_dir_path):
				if os.path.isdir(os.path.join(weapp_view_dir_path, f)):
					dirs.append({
						'module_parent': weapp_view_dir_path,
						'module': f,
						'url_path': url_path
					})
		else:
			dirs.append({
				'module_parent': weapp_view_dir_path,
				'module': '',
				'url_path': url_path
			})

	#获取包含js/view的目录
	views = []
	for dir in dirs:
		views_dir_path = os.path.join(dir['module_parent'], dir['module'], 'js/view')
		#print("views_dir_path: {}".format(views_dir_path))

		if not os.path.exists(views_dir_path):
			continue

		#获得views集合信息
		view_info_file_path = os.path.join(views_dir_path, 'views.info')
		if not os.path.exists(view_info_file_path):
			raise RuntimeError('There is NO "views.info" file in directory "%s"' % views_dir_path)

		view_infos = []
		src_file = open(view_info_file_path, 'rb')
		for line in src_file:
			view_name = line.strip()
			view_dir = os.path.join(views_dir_path, view_name)
			if os.path.isdir(view_dir):
				view_infos.append({
					'dir': view_dir,
					'name': view_name
				})
		src_file.close()		

		#获得view的template和js
		for view_info in view_infos:			
			view_dir = view_info['dir']
			view_name = view_info['name']

			#获取template文件信息
			template_file_path = os.path.join(view_dir, 'template.html')
			template_source = ''
			if os.path.isfile(template_file_path):
				src_file = open(template_file_path, 'rb')
				template_source = src_file.read()
				src_file.close()

			#获取js文件信息
			js_file_path = os.path.join(views_dir_path, view_dir, 'view.js')
			if (dir['module']):
				js_url_path = '/%s/%s/js/view/%s/view.js' % (dir['url_path'], dir['module'], view_name)
			else:
				js_url_path = '/%s/js/view/%s/view.js' % (dir['url_path'], view_name)

			#print('js_file_path:{}'.format(js_file_path))
			views.append({
				'template_file_path': template_file_path,
				'template_source': template_source,
				'js_file_path': js_file_path,
				'js_url_path': js_url_path
			})
	return views


def get_web_models(version):
	"""
	获得web页面的model的资源
	"""
	dirs = []
	if version == '1':
		WEAPP_WEB_MODEL_DIRS = settings.WEAPP_WEB_MODEL_DIRS
	elif version == '2':
		WEAPP_WEB_MODEL_DIRS = settings.WEAPP_WEB_MODEL_DIRS_V2
	else:
		WEAPP_WEB_MODEL_DIRS = settings.WEAPP_WEB_MODEL_DIRS_APPS
	for url_path, weapp_view_dir_path in WEAPP_WEB_MODEL_DIRS:
		if weapp_view_dir_path.endswith('*'):
			weapp_view_dir_path = weapp_view_dir_path[:-2]
			for f in os.listdir(weapp_view_dir_path):
				if os.path.isdir(os.path.join(weapp_view_dir_path, f)):
					dirs.append({
						'module_parent': weapp_view_dir_path,
						'module': f,
						'url_path': url_path
					})
		else:
			dirs.append({
				'module_parent': weapp_view_dir_path,
				'module': '',
				'url_path': url_path
			})

	#获取包含js/view的目录
	models = []
	for dir in dirs:
		models_dir_path = os.path.join(dir['module_parent'], dir['module'], 'js/model')
		print("models_dir_path: {}".format(models_dir_path))

		if not os.path.exists(models_dir_path):
			continue

		for module_name in os.listdir(models_dir_path):
			module_dir = os.path.join(models_dir_path, module_name)
			if not os.path.isdir(module_dir):
				continue

			for f in os.listdir(module_dir):
				if f.endswith('.js'):
					if (dir['module']):
						js_url_path = '/%s/%s/js/model/%s/%s' % (dir['url_path'], dir['module'], module_name, f)
					else:
						js_url_path = '/%s/js/model/%s/%s' % (dir['url_path'], module_name, f)
					models.append({
						'js_file_path': os.path.join(module_dir, f),
						'js_url_path': js_url_path
					})
				
	return models