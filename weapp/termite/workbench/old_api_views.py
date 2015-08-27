# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import base64
import random

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth
from core import stripper

from models import *
from account.models import UserProfile
from core.jsonresponse import create_response
import pagerender

def __get_plural_name(name):
	if name[-1] == 's':
		return '%ses' % name
	elif name[-1] == 'y':
		return '%sies' % name[:-1]
	else:
		return '%ss' % name


#===============================================================================
# __create_file_from_template : 从模板创建文件
#===============================================================================
def __create_file_from_template(template_path, target_dir, target_file_name, context, should_process_django_template_tags=False):
	template = get_template(template_path)
	content = stripper.strip_lines(template.render(context))
	if should_process_django_template_tags:
		content = content.replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}')
	target_file = open(os.path.join(target_dir, target_file_name), 'wb')
	print >> target_file, content.encode('utf-8')
	target_file.close()


#===============================================================================
# create_pages : 创建页面文件
#===============================================================================
def create_pages(request):
	#
	#创建app目录
	#
	app_name = request.POST['app']
	app_dir = os.path.join('.', app_name)
	if os.path.isdir(app_dir):
		print 'remove old app: ', app_dir
		shutil.rmtree(app_dir)
	editor_template_dir = os.path.join(app_dir, 'templates', app_name, 'editor')
	mobile_template_dir = os.path.join(app_dir, 'templates', app_name)
	os.makedirs(editor_template_dir)

	#
	#创建app目录中的文件
	#
	#创建__init__.py
	init_file = open(os.path.join(app_dir, '__init__.py'), 'wb')
	init_file.close()

	#创建其他文件
	navs = json.loads(request.POST['navs'])
	name2nav = {}
	for nav in navs:
		name2nav[nav['value']] = nav

	data_json_str = request.POST['data_json_str']
	pages = json.loads(data_json_str)
	for page in pages:
		components = page
		components.sort(lambda x,y: cmp(x['index'], y['index']))

		print components

		context_data = components[0]
		context_data['listinfo'] = components[1]
		context_data['app'] = app_name
		context_data['properties'] = components[2:]
		context_data['className'] = context_data['className'].lower().capitalize()
		context_data['previewClassName'] = 'Preview%s' % context_data['className'].capitalize()
		context_data['instanceName'] = context_data['className'].lower()
		context_data['pluralInstanceName'] = __get_plural_name(context_data['instanceName'])
		#判断是否需要预览
		for component in context_data['properties']:
			if component['type'] == 'weixin_simulator':
				context_data['isEnablePreview'] = component['isEnablePreview']
				context_data['properties'].remove(component)
			if component['type'] == 'swipe_images_input':
				context_data['hasSwipeImages'] = "yes"
			if component['type'] == 'select_input':
				options_str = component['options']
				component['options_str'] = options_str
				component['options'] = []
				items = options_str.split(',')
				for item in items:
					if not item:
						continue
					display_name, value = item.split('=')
					component['options'].append({'displayName':display_name.strip(), 'value':value.strip()})

		#
		#处理list info
		#
		#获取<name, property>映射
		name2property = {}
		for property in context_data['properties']:
			name2property[property['name']] = property
		#获取每一column的信息
		list_component = components[1]
		if list_component['isEnableListPage'] == u'yes':
			columns = []
			for name, info in list_component['columns'].items():
				if not info['select']:
					continue
				
				columns.append({
					'name': name, 
					'label': name2property[name]['label'],
					'type': name2property[name]['type'],
					'index': info['index']
				})
			columns.sort(lambda x,y: cmp(x['index'], y['index']))
			context_data['list_columns'] = columns

		context = Context(context_data)

		# 生成app python文件
		__create_file_from_template('code/models_tmpl.py', app_dir, 'models.py', context)
		__create_file_from_template('code/urls_tmpl.py', app_dir, 'urls.py', context)
		__create_file_from_template('code/views_tmpl.py', app_dir, 'views.py', context)
		__create_file_from_template('code/api_views_tmpl.py', app_dir, 'api_views.py', context)

		nav_name = context_data['navItem']
		name2nav[nav_name]['target'] = '/%s/editor/%s/' % (app_name, context_data['pluralInstanceName'])
		context['navs'] = navs
		__create_file_from_template('code/webapp_template_info_tmpl.py', app_dir, 'webapp_template_info.py', context)

		#生成editor html模板文件
		__create_file_from_template('code/edit_entity_tmpl.html', editor_template_dir, 'edit_%s.html' % context_data['instanceName'], context, True)
		__create_file_from_template('code/list_entity_tmpl.html', editor_template_dir, '%s.html' % context_data['pluralInstanceName'], context, True)

		#生成mobile相关文件
		__create_file_from_template('code/mobile_urls_tmpl.py', app_dir, 'mobile_urls.py', context)
		__create_file_from_template('code/mobile_views_tmpl.py', app_dir, 'mobile_views.py', context)
		__create_file_from_template('code/mobile_index_tmpl.html', mobile_template_dir, 'index.html', context, True)
		__create_file_from_template('code/mobile_entity_list_tmpl.html', mobile_template_dir, '%s.html' % context_data['pluralInstanceName'], context, True)
		__create_file_from_template('code/mobile_entity_detail_tmpl.html', mobile_template_dir, '%s_detail.html' % context_data['instanceName'], context, True)

		print context

	#
	#更新user_settings.py
	#
	user_settings_file = open('workbench/templates/code/user_settings_tmpl.py', 'rb')
	content = user_settings_file.read()
	user_settings_file.close()
	prefix_end = content.find('# BEGIN OF DYNAMIC APP')
	suffix_beg = content.find('# END OF DYNAMIC APP')
	items = [content[:prefix_end].strip(), '# BEGIN OF DYNAMIC APP', "\t'%s'," % app_name, content[suffix_beg:].strip()]
	print items
	user_settings_file = open('user_settings.py', 'wb')
	print >> user_settings_file, '\n'.join(items)
	user_settings_file.close()

	#
	# 更新user_urls.py
	#
	user_urls_file = open('workbench/templates/code/user_urls_tmpl.py', 'rb')
	content = user_urls_file.read()
	user_urls_file.close()
	prefix_end = content.find('# BEGIN OF DYNAMIC URLS')
	suffix_beg = content.find('# END OF DYNAMIC URLS')
	items = [
		content[:prefix_end].strip(), 
		'# BEGIN OF DYNAMIC URLS', 
		"\turl(r'^m/%s/', include('%s.mobile_urls'))," % (app_name, app_name),
		"\turl(r'^%s/', include('%s.urls'))," % (app_name, app_name), 
		content[suffix_beg:].strip()
	]
	print items
	user_urls_file = open('user_urls.py', 'wb')
	print >> user_urls_file, '\n'.join(items)
	user_urls_file.close()

	#更新settings.py的时间，激发server重新加载
	os.utime('./termite/settings.py', None)

	response = create_response(200)
	return response.get_response()


#===============================================================================
# preview_viper_result : 预览viper结果
#===============================================================================
@login_required
def preview_viper_result(request):
	app = request.GET['app']
	
	#确定url中的entity名, models.py文件中的第一个model的名字转换而成
	models_file = open('./%s/models.py' % app, 'rb')
	plural_instance_name = ''
	for line in models_file:
		if '(models.Model):' in line:
			beg = line.find("(")
			class_name = line[:beg].split(' ')[1]
			plural_instance_name = __get_plural_name(class_name.lower())
			break
	models_file.close()

	response = create_response(200)
	response.data = {'url': '/%s/editor/%s/' % (app, plural_instance_name)}
	return response.get_response()







# #===============================================================================
# # create_mobile_page : 创建移动页面
# #===============================================================================
# def __render_component(request, component, project_id):
# 	template = get_template('workbench/one_page.html')
# 	sub_components = component.get('components', [])
# 	sub_components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))
# 	for sub_component in sub_components:
# 		sub_component['parent_component'] = component
# 		sub_component['html'] = __render_component(request, sub_component, project_id)

# 	context = RequestContext(request, {
# 		'component': component,
# 		'project_id': project_id
# 	})
# 	content = stripper.strip_lines(template.render(context))
# 	'''
# 	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
# 	print component
# 	print content
# 	print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
# 	'''
# 	return content


# def _create_mobile_page_html_content(request, page, project_id=None):
# 	if not 'components' in page:
# 		page['components'] = []
# 	print json.dumps(page, indent=2)
# 	#识别header, content components, footer
# 	page['headers'] = []
# 	page['footers'] = []
# 	page['content'] = {'type': 'content', 'uid':'', 'components':[], 'model': {'index': 1}}
# 	for component in page['components']:
# 		if component['type'] == 'page_header':
# 			component['model']['index'] = 0
# 			page['headers'].append(component)
# 		elif component['type'] == 'page_footer':
# 			component['model']['index'] = 999999999
# 			page['footers'].append(component)
# 		else:
# 			page['content']['components'].append(component)

# 	page['original_components'] = page['components']
# 	page['components'] = []
# 	page['components'].extend(page['headers'])
# 	page['components'].append(page['content'])
# 	page['components'].extend(page['footers'])

# 	html = __render_component(request, page, project_id)
# 	return html


@login_required
def create_mobile_page(request):
	page = json.loads(request.POST['page'])
	#html = _create_mobile_page_html_content(request, page)
	html = pagerender.create_mobile_page_html_content(request, {}, page)

	response = create_response(200)
	response.data = html
	return response.get_response()


#######################################################################
# synchronize_page: 同步一个page的内容
#######################################################################
@login_required
def synchronize_page(request):
	project_id = request.POST['project_id']
	page_id = request.POST['page_id']
	page_json = request.POST['page_json']

	page = Page.objects.filter(project_id=project_id, page_id=page_id)
	if page.count() > 0:
		page.update(json_content = page_json)
	else:
		page = Page.objects.create(
			owner = request.user,
			project_id = project_id,
			page_id = page_id,
			display_index = page_id,
			json_content = page_json
		)

	response = create_response(200)
	return response.get_response()


#######################################################################
# delete_page: 删除一个page
#######################################################################
@login_required
def delete_page(request):
	project_id = request.POST['project_id']
	page_id = request.POST['page_id']

	Page.objects.filter(project_id=project_id, page_id=page_id).delete()

	response = create_response(200)
	return response.get_response()


#######################################################################
# update_page_display_index: 调整page的显示顺序
#######################################################################
@login_required
def update_page_display_index(request):
	project_id = request.POST['project_id']
	ordered_pages = request.POST['ordered_pages']

	index = 1
	for page_id in ordered_pages.split(','):
		Page.objects.filter(project_id=project_id, page_id=page_id).update(display_index=index)
		index += 1

	response = create_response(200)
	return response.get_response()


#######################################################################
# get_pages_json: 获得page的json内容
#######################################################################
def get_pages_json(request):
	project_id = request.GET['project_id']
	
	pages = []
	for page in Page.objects.filter(project_id=project_id).order_by('display_index'):
		pages.append(json.loads(page.json_content))

	response = create_response(200)
	response.data = json.dumps(pages)
	return response.get_response()


#######################################################################
# read_css_content_for: 读取project对应的css文件
#######################################################################
def read_css_content_for(project_id):
	css_dir = os.path.join(settings.PROJECT_HOME, '..', 'static', 'project_css')
	if not os.path.exists(css_dir):
		os.makedirs(css_dir)

	css_file = os.path.join(css_dir, 'project_%s.css' % project_id)
	if not os.path.exists(css_file):
		f = open(css_file, 'wb')
		print >> f, '/* css conentet for project %s */' % project_id
		f.close()

	f = open(css_file, 'rb')
	content = f.read()
	f.close()

	return content


#######################################################################
# get_css: 获得project的css内容
#######################################################################
def get_css(request):
	project_id = request.GET['project_id']

	css_content = read_css_content_for(project_id)

	response = create_response(200)
	response.data = css_content
	return response.get_response()


#######################################################################
# write_css_content_for: 写project对应的css文件
#######################################################################
def write_css_content_for(project_id, content):
	css_dir = os.path.join(settings.PROJECT_HOME, '..', 'static', 'project_css')
	css_file = os.path.join(css_dir, 'project_%s.css' % project_id)
	
	f = open(css_file, 'wb')
	print >> f, content
	f.close()

	return True


#######################################################################
# update_css: 更新project的css内容
#######################################################################
def update_css(request):
	project_id = request.POST['project_id']
	content = request.POST['content']

	write_css_content_for(project_id, content)

	response = create_response(200)
	return response.get_response()


#######################################################################
# update_workspace_name: 更新workspace名
#######################################################################
def update_workspace_name(request):
	workspace_id = request.POST['workspace_id']
	Workspace.objects.filter(id=workspace_id).update(name=request.POST['name'])

	response = create_response(200)
	return response.get_response()


#######################################################################
# update_project_name: 更新project名
#######################################################################
def update_project_name(request):
	project_id = request.POST['project_id']
	Project.objects.filter(id=project_id).update(name=request.POST['name'])

	response = create_response(200)
	return response.get_response()


#######################################################################
# get_datasource_project: 获得数据源
#######################################################################
@login_required
def get_datasource_project(request):
	project_id = request.GET['project_id']

	pages = []
	for page in Page.objects.filter(project_id=project_id):
		page_component = json.loads(page.json_content)
		page_model = page_component['model']
		one_page = {}
		one_page['name'] = page_model['title']
		one_page['id'] = page.page_id

		try:
			record = Record.objects.filter(page_id=page.page_id)[0]
			fields = []
			record_model = json.loads(record.json_content)
			for field in record_model:
				if field.startswith('__'):
					continue
				else:
					fields.append(field)
			one_page['fields'] = fields
		except:
			one_page['fields'] = []

		pages.append(one_page)

	response = create_response(200)
	response.data = pages
	return response.get_response()


#######################################################################
# get_project_images: 获得项目图片
#######################################################################
@login_required
def get_project_images(request):
	project_id = request.GET['project_id']
	dir_path_suffix = '%d_%s' % (request.user.id, project_id)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	response = create_response(200)
	response.data = []
	for file_name in os.listdir(dir_path):
		response.data.append('/static/upload/%s/%s' % (dir_path_suffix, file_name))
	
	return response.get_response()


#######################################################################
# delete_project_image: 删除项目图片
#######################################################################
@login_required
def delete_project_image(request):
	project_id = request.POST['project_id']
	filename = request.POST['filename'].split('/')[-1]
	dir_path_suffix = '%d_%s' % (request.user.id, project_id)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	
	file_path = os.path.join(dir_path, filename)
	if os.path.exists(file_path):
		os.remove(file_path)

	response = create_response(200)

	return response.get_response()


#######################################################################
# create_page_template: 创建Page模板
#######################################################################
def __save_template_picture(image_data):
	data = base64.b64decode(image_data)
	file_name = '%s_%d.png' % (str(time.time()).replace('.', '0'), random.randint(1, 1000))
	dir_path = settings.PAGE_TEMPLATE_IMAGE_DIR
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(data)
	dst_file.close()


	pos = file_path.find('/static')
	return file_path[pos:].replace('\\', '/')

@login_required
def create_page_template(request):
	project_id = request.POST['project_id']
	page = request.POST['page']
	image = request.POST['image']
	name = request.POST['name']

	project = Project.objects.get(id=project_id)
	PageTemplate.objects.create(
		owner = request.user, 
		project_type = project.type,
		page_json = page,
		name = name,
		image_data = __save_template_picture(image)
	)

	return create_response(200).get_response()


#######################################################################
# get_page_templates: 获取pate template集合
#######################################################################
@login_required
def get_page_templates(request):
	project_type = request.GET['project_type']

	items = [{
		'page_json': "{}",
		'id': 0,
		'url': '',
		'name': u'空白页'
	}]
	for page_template in PageTemplate.objects.filter(project_type=project_type):
		one_template = {
			'pageJson': page_template.page_json,
			'id': page_template.id,
			'url': page_template.image_data,
			'name': page_template.name
		}
		items.append(one_template)

	response = create_response(200)
	response.data = items
	return response.get_response()