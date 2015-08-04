# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import sys

from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Template
from termite.core import stripper
from webapp import views as webapp_views 
from models import *
from mall.models import ProductCategory


type2template = {}


#################################################################################
# __extract_component_type: 从f中抽取component type
#################################################################################
def __extract_component_type(file_path):
	#print 'extract component type from ', file_path
	component_type = None
	src_file = open(file_path, 'rb')
	should_capture_type = False
	for line in src_file:
		line = line.strip()
		if 'W.component.Component.extend' in line:
			should_capture_type = True
		if should_capture_type and line.startswith('type:'):
			beg = line.find("'")
			if beg != -1:
				end = line.find("'", beg+1)
			else:
				beg = line.find('"')
				if beg == -1:
					print '[ERROR]: no W.component.register in ', file_path
				else:
					end = line.find('"', beg+1)

			component_type = line[beg+1:end]
			#only process first type line
			break
	src_file.close()

	return component_type


#################################################################################
# __load_template: 加载component dir下的template
#################################################################################
def __load_template(component_dir, component_category):
	component_name = os.path.basename(component_dir)
	template_path = os.path.join(component_dir, '%s.html' % component_name)
	if os.path.isfile(template_path):
		template_path = template_path.split('/app/')[-1]
		if settings.DEBUG:
			#print 'load... ', template_path
			pass
		template = get_template(template_path)
	else:
		print '[WARN]: no template file - ', os.path.join(component_dir, '%s.html' % component_name)
		template = None

	for file_name in os.listdir(component_dir):
		if file_name.endswith('.js'):
			file_path = os.path.join(component_dir, file_name)
			component_type = __extract_component_type(file_path)
			if component_type:
				type = '%s.%s' % (component_category, component_type)
				type2template[type] = template
	


#################################################################################
# __load_templates: 加载components的template
#################################################################################
def __load_templates():
	type2template.clear()
	components_home_dir = settings.COMPONENTS_DIR
	print 'components_home_dir: ', components_home_dir
	for components_dir in os.listdir(components_home_dir):
		component_category = components_dir
		components_dir = os.path.join(components_home_dir, components_dir)
		if not os.path.isdir(components_dir):
			continue
		for file_name in os.listdir(components_dir):
			component_dir = os.path.join(components_dir, file_name)
			if not os.path.isdir(component_dir):
				continue
		
			__load_template(component_dir, component_category)

	type2template['unknown'] = get_template('component/common/common.html')


#################################################################################
# __get_template: 获得component对应的template
#################################################################################
def __get_template(component_category, component):
	component_type = '%s.%s' % (component_category, component['type'])
	template = type2template.get(component_type, None)
	if not template:
		template = type2template['unknown']

	#if 'common.html' in template.name:
	#	print 'use template(%s) for component(%s) [!]' % (template.name, component_type)
	#else:
	#	print 'use template(%s) for component(%s)' % (template.name, component_type)
	return template


#===============================================================================
# __get_datas_from_datasource : 在product mode下，从page._data中获得component需要的数据
#===============================================================================
def __get_datas_from_datasource(request, page, component, project):
	page_data = page.get('_data', None)
	if page_data:
		component_name = component['model'].get('name', None)
		if component_name:
			return page_data.get(component_name, None)
		else:
			return {}

	return {}


#===============================================================================
# __get_page_data_from_datasource : 在product mode下，调用webapp的api，获得page对应的数据
#===============================================================================
def __get_page_data_from_datasource(request, page, component):
	if component['type'].endswith('.page') and (not hasattr(page, '_data')):
		datasource = component['model']['datasource']
		if not datasource:
			return {}

		api_name = datasource['api_name']
		if api_name:
			request.t__api_name = api_name
			request.t__return_json = True
			page['_data'] = webapp_views.call_api(request)


#===============================================================================
# create_mobile_page : 创建移动页面
#===============================================================================
def __render_component(request, page, component, project):
	if request.in_production_mode:
		#获得数据
		__get_page_data_from_datasource(request, page, component)
		component['datasources'] = __get_datas_from_datasource(request, page, component, project)
		print component['type']
		print page.get('_data')

	#获取所有sub component的html片段
	sub_components = component.get('components', [])
	component['sub_component_count'] = len(sub_components)
	sub_components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))
	for sub_component in sub_components:
		if sub_component['type'] == 'wepage.item_list':
			# 过滤 商品列表 更新分类信息
			sub_component = __update_category(sub_component)

		if sub_component:
			sub_component['parent_component'] = component
			sub_component['html'] = __render_component(request, page, sub_component, project)
			#将sub_component的信息放入component中
			sub_component_type = sub_component['type'].replace('.', '')
			if not sub_component_type in component:
				component[sub_component_type] = sub_component

	#处理javascript, javascript片段在model中，以event:onclick的形式存储
	for field, value in component['model'].items():
		if field.startswith('event:'):
			if '{{' in value:
				#渲染模板
				script_template = Template(value)
				context = RequestContext(request, {
				})
				value = script_template.render(context)
				page['scripts'].append(value)
			else:
				page['scripts'].append(value)

	#渲染component自身
	context = Context({
		'request': request,
		'page': page,
		'component': component,
		'project': project,
		'project_id': project.id,
		'in_design_mode': request.in_design_mode,
		'in_preview_mode': request.in_preview_mode,
		'in_production_mode': request.in_production_mode,
	})
	if hasattr(request, 'extra_page_context'):
		context.update(request.extra_page_context)
	component_category = project.type
	template = __get_template(component_category, component)
	content = stripper.strip_lines(template.render(context))
	'''
	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	print component
	print content
	print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
	'''
	return content


#######################################################################
# __update_category: 更新分组信息
#######################################################################
def __update_category(component):
	category = component["model"].get("category")
	if category:
		category = json.loads(category)
		if len(category) > 0:
			cateoryId = category[0]["id"]
			categories = ProductCategory.objects.filter(id=cateoryId)
			if categories.count() == 0:
				component = None
			else:
				category[0]["title"] = categories[0].name
				component["model"]["category"] = json.dumps(category)

	return component


#设置别名，方便别的文件调用
_render_component = __render_component


#===============================================================================
# __render_component_global_content : 渲染global content
#===============================================================================
def __render_component_global_content(request, page, components, project):
	project_id = project.id
	component_category = project.type
	components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))

	htmls = []
	for component in components:
		#正常渲染sub component
		sub_components = component.get('components', [])
		sub_components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))
		for sub_component in sub_components:
			sub_component['parent_component'] = component
			sub_component['html'] = __render_component(request, page, sub_component, project)

		template = __get_template(component_category, component)
		old_type = component['type']
		component['type'] = '%s:global_content' % old_type
		context = RequestContext(request, {
			'page': page,
			'component': component,
			'project_id': project_id
		})

		content = stripper.strip_lines(template.render(context))
		component['type'] = old_type

		htmls.append(content)
	#print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	#print component
	#print content
	#print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
	return '\n'.join(htmls)


def create_mobile_page_html_content(request, page, page_component, project=None):
	#if len(type2template) == 0:
	#	__load_templates()
	__load_templates()

	page['scripts'] = []
	htmls = []
	if hasattr(page_component, 'global_content_components'):
		htmls.append(__render_component_global_content(request, page, page_component['global_content_components'], project))
	htmls.append(__render_component(request, page, page_component, project))

	'''
	if len(page['scripts']) > 0:
		page['scripts'].reverse()
		htmls.append('<script type="text/javascript">');
		htmls.append('$(document).ready(function() {');
		for script in page['scripts']:
			htmls.append(script)
		htmls.append('});');
		htmls.append('</script>');
	'''

	if '_data' in page:
		htmls.append('<script type="text/javascript">W.pageData = $.parseJSON(\'%s\');</script>' % json.dumps(page['_data']).replace(r'\"', r'\\"'))

	return '\n'.join(htmls)