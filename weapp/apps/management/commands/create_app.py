# -*- coding: utf-8 -*-

__author__ = 'robert'

import datetime
import array
import os
import json
import shutil
import copy
import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

from utils import stripper

FORCE_CREATE = False

class Command(BaseCommand):
	help = "create app from json file"
	args = ''

	def __get_plural_name(self, name):
		if name[-1] == 's':
			return '%ses' % name
		elif name[-1] == 'y':
			return '%sies' % name[:-1]
		else:
			return '%ss' % name

	def __render_template_file(self, template_file_path, context, dst_file_path, content_processors=None):
		print '[render] %s to %s' % (template_file_path, dst_file_path)
		template = get_template(template_file_path)
		content = stripper.strip_lines(template.render(context)).replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}')
		if content_processors:
			for content_processor in content_processors:
				content = content_processor(content)
		f = open(dst_file_path, 'wb')
		print >> f, content.encode('utf-8')
		f.close()

	def copy_app_template_to(self, app_dir, app_name):
		app_template_dir = os.path.join(settings.PROJECT_HOME, '../apps/app_template')
		if os.path.exists(app_dir) and not FORCE_CREATE:
			print u'[危险操作] 已经存在一个名为"%s"的app!!!!' % app_name
			print u'是否覆盖现存的"%s"，创建空的新app ? [y|n] : ' % app_name,
			value = raw_input().strip()
			if value == 'n' or value == 'N':
				sys.exit(1)
		
		if os.path.exists(app_dir):
			print 'remove old app: ', app_dir
			shutil.rmtree(app_dir)

		shutil.copytree(app_template_dir, app_dir)

	def generate_resource_files(self, app_dir, app):
		#收集resource
		resources = []
		for resource in app['resources']:
			resource['plural_name'] = self.__get_plural_name(resource['name']).lower()
			resource['actions'] = {"get":True, "api_put":True, "api_post":True,"api_delete":True}
			resource['is_item_resource'] = True
			resource['is_status_resource'] = False
			resource['is_collection_resource'] = False
			resource['is_need_model'] = True
			resource['is_mobile_resource'] = False
			resource['is_participance'] = False
			resource['file_name'] = resource['lower_name']
			resource['second_nav'] = resource['plural_name']
			resources.append(resource)

			if resource['need_user_participant']:
				participance_resource = copy.copy(resource)
				participance_resource['lower_name'] = '%s_participance' % participance_resource['lower_name']
				participance_resource['item_class_name'] = resource['class_name']
				participance_resource['class_name'] = '%sParticipance' % participance_resource['class_name']
				participance_resource['actions'] = {"api_get":True, "api_put":True}
				participance_resource['is_item_resource'] = True
				participance_resource['is_collection_resource'] = False
				participance_resource['is_need_model'] = False
				participance_resource['is_mobile_resource'] = False
				participance_resource['is_participance'] = True
				participance_resource['need_user_participant'] = False
				participance_resource['enable_termite'] = False
				participance_resource['file_name'] = participance_resource['lower_name']
				resources.append(participance_resource)

				participances_resource = copy.copy(resource)
				participances_resource['lower_name'] = '%s_participances' % resource['lower_name']
				participances_resource['item_class_name'] = participance_resource['class_name']
				participances_resource['class_name'] = '%sParticipances' % resource['class_name']
				participances_resource['actions'] = {"get":True, "api_get":True}
				participances_resource['is_item_resource'] = False
				participances_resource['is_collection_resource'] = True
				participances_resource['is_need_model'] = False
				participances_resource['is_mobile_resource'] = False
				participances_resource['is_participance'] = True
				participances_resource['need_user_participant'] = False
				participances_resource['file_name'] = participances_resource['lower_name']
				resources.append(participances_resource)

			mobile_resource = copy.copy(resource)
			mobile_resource['is_item_resource'] = False
			mobile_resource['is_collection_resource'] = False
			mobile_resource['is_mobile_resource'] = True
			mobile_resource['is_need_model'] = False
			mobile_resource['need_check_user_participant'] = True
			mobile_resource['need_user_participant'] = False
			mobile_resource['actions'] = {"get":True}
			mobile_resource['file_name'] = 'm_%s' % mobile_resource['lower_name']
			resources.append(mobile_resource)

			status_resource = copy.copy(resource)
			status_resource['lower_name'] = '%s_status' % resource['lower_name']
			status_resource['class_name'] = '%sStatus' % resource['class_name']
			status_resource['item_lower_name'] = resource['lower_name']
			status_resource['item_class_name'] = resource['class_name']
			status_resource['is_item_resource'] = False
			status_resource['is_status_resource'] = True
			status_resource['is_collection_resource'] = False
			status_resource['is_mobile_resource'] = False
			status_resource['is_need_model'] = False
			status_resource['need_user_participant'] = False
			status_resource['actions'] = {"api_post":True}
			status_resource['file_name'] = status_resource['lower_name']
			resources.append(status_resource)

			collection_resource = copy.copy(resource)
			collection_resource['name'] = self.__get_plural_name(collection_resource['name'])
			collection_resource['item_lower_name'] = collection_resource['lower_name']
			collection_resource['lower_name'] = self.__get_plural_name(collection_resource['lower_name'])
			collection_resource['item_class_name'] = collection_resource['class_name']
			collection_resource['file_name'] = collection_resource['lower_name']
			collection_resource['class_name'] = self.__get_plural_name(collection_resource['class_name'])
			collection_resource['actions'] = {"get":True, "api_get":True}
			collection_resource['is_item_resource'] = False
			collection_resource['is_collection_resource'] = True
			collection_resource['is_mobile_resource'] = False
			collection_resource['is_need_model'] = False
			collection_resource['need_user_participant'] = False
			collection_resource['need_export'] = True
			resources.append(collection_resource)

		#生成resource py文件
		for resource in resources:
			if resource['is_mobile_resource']:
				resource_template = 'item_mobile_resource_template.py'
			else:
				if resource['is_item_resource']:
					resource_template = 'item_resource_template.py'
				elif resource['is_status_resource']:
					resource_template = 'item_status_template.py'
				else:
					if resource['is_participance']:
						resource_template = 'collection_participance_template.py'
					else:
						resource_template = 'collection_resource_template.py'
			
			tmpl_file_path = os.path.join(app['name'], resource_template)
			dst_file_path = os.path.join(app_dir, '%s.py' % resource['file_name'])
			context = Context({
				'app_name': app['name'],
				'resource': resource
			})
			self.__render_template_file(tmpl_file_path, context, dst_file_path)

		#生成urls.py
		context = Context({
			'app_name': app['name'],
			'resources': resources
		})
		tmpl_file_path = os.path.join(app['name'], 'urls_template.py')
		dst_file_path = os.path.join(app_dir, 'urls.py')
		self.__render_template_file(tmpl_file_path, context, dst_file_path)

		#生成export.py
		tmpl_file_path = os.path.join(app['name'], 'export_template.py')
		dst_file_path = os.path.join(app_dir, 'export.py')
		self.__render_template_file(tmpl_file_path, context, dst_file_path)

		#生成models.py
		tmpl_file_path = os.path.join(app['name'], 'mongo_models_template.py')
		dst_file_path = os.path.join(app_dir, 'models.py')
		self.__render_template_file(tmpl_file_path, context, dst_file_path)

		#生成html文件
		def replace_target_with(target, replace_content):
			def inner(content):
				return content.replace(target, replace_content)
			return inner

		for resource in resources:
			context = Context({
				'app_name': app['name'],
				'resource': resource
			})
			if resource['is_mobile_resource']:
				tmpl_file_path = os.path.join(app['name'], 'templates/webapp/record_template.html')
				dst_file_path = os.path.join(app_dir, 'templates/webapp/m_%s.html' % resource['lower_name'])
				self.__render_template_file(tmpl_file_path, context, dst_file_path)
			elif resource['is_item_resource']:
				if resource['enable_termite']:
					tmpl_file_path = os.path.join(app['name'], 'templates/editor/workbench_template.html')
					dst_file_path = os.path.join(app_dir, 'templates/editor/workbench.html')
					self.__render_template_file(tmpl_file_path, context, dst_file_path)					
				else:
					resource['fields'] = [{
						"field": "name",
						"type": "string"
					}, {
						"field": "time",
						"type": "time"
					}]
					tmpl_file_path = os.path.join(app['name'], 'templates/editor/resource_form_template.html')
					dst_file_path = os.path.join(app_dir, 'templates/editor/%s.html' % resource['lower_name'])
					self.__render_template_file(tmpl_file_path, context, dst_file_path)
			elif resource['is_participance']:
				tmpl_file_path = os.path.join(app['name'], 'templates/editor/participance_list_template.html')
				dst_file_path = os.path.join(app_dir, 'templates/editor/%s.html' % resource['lower_name'])
				self.__render_template_file(tmpl_file_path, context, dst_file_path)
			else:
				tmpl_file_path = os.path.join(app['name'], 'templates/editor/resource_list_template.html')
				dst_file_path = os.path.join(app_dir, 'templates/editor/%s.html' % resource['lower_name'])
				func1 = replace_target_with('[[item_resource]]', resource['item_lower_name'])
				func2 = replace_target_with('[[app_name]]', app['name'])
				self.__render_template_file(tmpl_file_path, context, dst_file_path, [func1, func2])

		#生成dialog
		context = Context({
			'app_name': app['name'],
			'participance_resource_name': participance_resource['lower_name']
		})
		tmpl_file_path = os.path.join(app['name'], 'static/js/dialog/view_participance_data_dialog/dialog_template.js')
		dst_file_path = os.path.join(app_dir, 'static/js/dialog/view_participance_data_dialog/dialog.js')
		self.__render_template_file(tmpl_file_path, context, dst_file_path)
		tmpl_file_path = os.path.join(app['name'], 'static/js/dialog/view_participance_data_dialog/dialog_template.html')
		dst_file_path = os.path.join(app_dir, 'static/js/dialog/view_participance_data_dialog/dialog.html')
		self.__render_template_file(tmpl_file_path, context, dst_file_path)

	def remove_template_files(self, app_dir):
		for root, dirs, files in os.walk(app_dir):
			for file in files:
				if '_template.' in file:
					file_path = os.path.join(root, file)
					print '[remove template]: %s' % file_path
					os.remove(file_path)

	option_list = BaseCommand.option_list + (
		make_option('--force',
			action='store_true',
			dest='force',
			default=False,
			help='force create app'),
	)
	
	def handle(self, json_file_path, **options):
		if options['force']:
			global FORCE_CREATE
			FORCE_CREATE = True
		src_file = open(json_file_path, 'rb')
		content = src_file.read()
		src_file.close()

		app_data = json.loads(content)
		for resource in app_data['resources']:
			resource['lower_name'] = resource['name'].lower()
			resource['class_name'] = resource['name']

		#app_dir = os.path.join(settings.PROJECT_HOME, '../apps/new_apps', app_data['name'])
		app_dir = os.path.join(settings.PROJECT_HOME, '../apps/customerized_apps', app_data['name'])
		self.copy_app_template_to(app_dir, app_data['name'])

		self.generate_resource_files(app_dir, app_data)
		self.remove_template_files(app_dir)
		