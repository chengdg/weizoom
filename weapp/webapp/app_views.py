# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy
from bs4 import BeautifulSoup as bs

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.template.loader import get_template

from models import *
from core.jsonresponse import create_response, JsonResponse
from termite import pagestore as pagestore_manager
from termite.core import stripper
from termite.workbench import viper_api_views

from apps import models as app_model
from apps import views as app_util
from apps import api_views as app_api_util


def __get_left_navs(project, pages):
	left_nav = {
		'section': project.name.encode('utf-8'),
		'navs': []
	}
	app_name = project.inner_name
	for page in pages:
		page_id = page['page_id']
		page_model = page['component']['model']
		page_title = page_model['title']
		page_module = page_model['module']
		if page_model['type'] == 'top_level_page':
			url = '/apps/{}/?module={}&resource={}&action=get'.format(app_name, page_module, page_title)
			left_nav['navs'].append({
				'name': page_module.encode('utf-8'),
				'url': url.encode('utf-8'),
				'title': '%s' % page_model['navName'].encode('utf-8')
			})

	left_nav['navs'].append({
		'name': 'apps',
		'url': '/apps/',
		'title': u'<i class="icon icon-arrow-left"></i>返回百宝箱'.encode('utf-8')
	})
	return left_nav


def __create_settings_file(app_dir, project, pages):
	path = os.path.join(app_dir, 'settings.py')
	f = open(path, 'rb')
	content = f.read()
	f.close()

	#获取modules
	modules = []
	recorded_module_set = set()
	store_engine_set = set()
	for page in pages:
		page_id = page['page_id']
		page_model = page['component']['model']
		if page_model['type'] != 'top_level_page':
			store_engine_set.add(page_model['storeEngine'])
		module_name = page_model['module']
		if module_name in recorded_module_set:
			continue

		modules.append(module_name)
		recorded_module_set.add(module_name)

	if len(store_engine_set) > 1:
		raise RuntimeError(u'所有的编辑页面都应该使用相同的Store Engine')

	store_engine = str(list(store_engine_set)[0])
	#获取views
	views = []
	for module in modules:
		views.append('{}.views'.format(module))
		views.append('{}.api_views'.format(module))
		views.append('{}.mobile_views'.format(module))
		views.append('{}.mobile_api_views'.format(module))

	#获取navs
	navs = [__get_left_navs(project, pages)]

	modules = json.dumps(modules, indent=4).replace('    ', '\t')
	views = json.dumps(views, indent=4).replace('    ', '\t')
	navs = json.dumps(navs, ensure_ascii=False, indent=4).replace('    ', '\t')

	#写入settings内容
	f = open(path, 'wb')
	print >> f, content % {"modules":modules, "views":views, "navs":navs, "store_engine": store_engine}
	f.close()


def __create_export_file(app_dir, project, pages):
	path = os.path.join(app_dir, 'export.py')
	f = open(path, 'rb')
	content = f.read()
	f.close()

	app_name = project.inner_name
	file_name = 'export.py'

	views_py_template_path = os.path.join(app_name, file_name)
	template = get_template(views_py_template_path)
	context = Context({
		"app_name": app_name,
		"pages": pages
	})
	content = stripper.strip_lines(template.render(context))

	views_py_path = os.path.join(app_dir, file_name)
	f = open(views_py_path, 'wb')
	print >> f, content.encode('utf-8')
	f.close()


def __create_page(request, app_dir, project, page, id2page):
	page_model = page['component']['model']

	#获取html页面	
	request.page = page
	request.id2page = id2page
	request.in_generate_mode = True
	html = viper_api_views.create_page(request, return_html_snippet=True)

	#渲染最终页面
	c = RequestContext(request, {
		'project_id': project.id,
		'page_html_content': html
	})
	response = render_to_response('workbench/viper_app_record_page.html', c)
	content = response.content
	content = content.replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}').replace('<!-- begin verbatim -->', r'{% verbatim %}').replace('<!-- end verbatim -->', r'{% endverbatim %}')
	return content


def __create_module(request, app_dir, project, pages):
	app_name = project.inner_name

	#搜集每个module中的page
	module2pages = {}
	id2page = dict([(page['page_id'], page) for page in pages])
	for page in pages:
		page_model = page['component']['model']
		module_name = page_model['module']
		module2pages.setdefault(module_name, []).append(page)

	for module in module2pages:
		src = os.path.join(app_dir, 'module_template')
		dst = os.path.join(app_dir, module)
		shutil.copytree(src, dst)

	for module, pages in module2pages.items():
		#设置top_level_page
		top_level_pages = filter(lambda page: page['component']['model']['type'] == 'top_level_page', pages)
		if not top_level_pages:
			raise RuntimeError(u'应用的module(%s)中没有top_level_page，请检查并创建之' % module)
		top_level_page = top_level_pages[0]
		for page in pages:
			page['top_level_page'] = top_level_page

		#生成views.py, api_views.py
		for file_name in ['views.py', 'api_views.py', 'mobile_views.py', 'mobile_api_views.py']:
			views_py_template_path = os.path.join(app_name, 'module_template', file_name)
			template = get_template(views_py_template_path)
			context = Context({
				"app_name": app_name,
				"pages": pages
			})
			content = stripper.strip_lines(template.render(context))

			views_py_path = os.path.join(app_dir, module, file_name)
			f = open(views_py_path, 'wb')
			print >> f, content.encode('utf-8')
			f.close()

		#生成editor html文件
		for page in pages:
			page_model = page['component']['model']
			if page_model['type'] == 'dialog_page':
				#不处理dialog page
				continue
			page_title = page_model['title']
			
			content = __create_page(request, app_dir, project, page, id2page)
			template_file_path = os.path.join(app_dir, 'templates/editor', '%s.html' % page_title)
			f = open(template_file_path, 'wb')
			print >> f, content
			f.close()

		#生成webapp html文件
		for page in pages:
			page_model = page['component']['model']
			if page_model['type'] != 'edit_page':
				continue

			page_title = page_model['title']

			src_path = os.path.join(app_name, 'templates/webapp/record_template.html')
			template = get_template(src_path)
			context = Context({
				"app_name": app_name,
				"page": page
			})
			content = stripper.strip_lines(template.render(context)).replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}')

			dst_path = os.path.join(app_dir, 'templates/webapp/{}.html'.format(page_title))
			f = open(dst_path, 'wb')
			print >> f, content.encode('utf-8')
			f.close()


def __create_dialogs(request, app_dir, project, pages):
	#获取所有dialog pages
	dialog_paes = filter(lambda page: page['component']['model']['type'] == 'dialog_page', pages)
	for dialog_page in dialog_paes:
		page_model = dialog_page['component']['model']
		dialog_name = page_model['title']
		dialog_js_name = page_model['name']
		dialog_dir = '%s_dialog' % page_model['title']
		
		src = os.path.join(app_dir, 'js/dialog/dialog_template')
		dst = os.path.join(app_dir, 'js/dialog', dialog_dir)
		shutil.copytree(src, dst)

		'''
		生成dialog.html
		'''
		#获取html内容
		request.page = dialog_page
		request.in_generate_mode = True
		raw_get = request.GET
		new_get = {}
		new_get.update(raw_get)
		new_get['project_id'] = project.id
		new_get['page_id'] = dialog_page['page_id']
		request.GET = new_get
		html = viper_api_views.create_page_by_id(request, return_html_snippet=True)
		request.GET = raw_get

		src_path = os.path.join(app_dir, 'js/dialog/dialog_template/dialog.html')
		template = get_template(src_path)
		context = Context({
			"dialog_name": dialog_name,
			"page_html_content": html
		})
		content = stripper.strip_lines(template.render(context)).replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}')

		dst_path = os.path.join(app_dir, 'js/dialog/%s/dialog.html' % dialog_dir)
		f = open(dst_path, 'wb')
		print >> f, content.encode('utf-8')
		f.close()

		'''
		生成dialog.js
		'''
		src_path = os.path.join(app_dir, 'js/dialog/dialog_template/dialog.js')
		template = get_template(src_path)
		context = Context({
			"dialog_name": dialog_name,
			"dialog_js_name": dialog_js_name
		})
		content = stripper.strip_lines(template.render(context)).replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}')

		dst_path = os.path.join(app_dir, 'js/dialog/%s/dialog.js' % dialog_dir)
		f = open(dst_path, 'wb')
		print >> f, content.encode('utf-8')
		f.close()

	'''
	删除dialog_template
	'''
	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	print 'remove tree : ', os.path.join(app_dir, 'js/dialog/dialog_template')
	shutil.rmtree(os.path.join(app_dir, 'js/dialog/dialog_template'))


def __create_mysql_models(request, app_dir, project, pages):
	app_name = project.inner_name

	#获取所有dialog pages
	pages = [page for page in pages if page['component']['model']['type'] != 'top_level_page']
	model_template = get_template(os.path.join(app_dir, 'mysql_model_template.py'))
	models_template = get_template(os.path.join(app_dir, 'mysql_models.py'))
	model_classes = []
	for page in pages:
		page_model = page['component']['model']
		django_class_name = page_model['className']
		fields = []
		for component in page['component']['components']:
			fields.append(component['model']['name'])

		context = Context({
			"app_name": app_name,
			"class_name": django_class_name,
			"fields": fields,
			"resource": page_model['title']
		})
		content = model_template.render(context)
		model_classes.append(content)

	context = Context({
		"model_classes": model_classes
	})
	content = stripper.strip_lines(models_template.render(context)).replace('<%', '{%').replace('%>', '%}').replace('<<', '{{').replace('>>', '}}')

	'''
	写入mysql_models.py
	'''
	dst_path = os.path.join(os.path.join(app_dir, 'mysql_models.py'))
	f = open(dst_path, 'wb')
	print >> f, content.encode('utf-8')
	f.close()

	'''
	删除mysql_model_template.py
	'''
	os.remove(os.path.join(app_dir, 'mysql_model_template.py'))
			

def __copy_app_template_to(app_dir):
	app_template_dir = os.path.join(settings.PROJECT_HOME, '../apps/app_template')
	if os.path.exists(app_dir):
		shutil.rmtree(app_dir)
	shutil.copytree(app_template_dir, app_dir)


def __create_app_files(request, project_id):
	settings.IS_UNDER_CODE_GENERATION = True
	project = Project.objects.get(id=project_id)
	pagestore = pagestore_manager.get_pagestore('mongo')

	#获取page对象
	pages = pagestore.get_pages(project_id)

	app_dir = os.path.join(settings.PROJECT_HOME, '../apps/customerized_apps', project.inner_name)
	__copy_app_template_to(app_dir)
	__create_settings_file(app_dir, project, pages)
	__create_export_file(app_dir, project, pages)
	__create_module(request, app_dir, project, pages)
	__create_dialogs(request, app_dir, project, pages)
	__create_mysql_models(request, app_dir, project, pages)
	shutil.rmtree(os.path.join(app_dir, 'module_template'))
	
	settings.IS_UNDER_CODE_GENERATION = False

	return project.inner_name, project.name


#===============================================================================
# create_customized_app : 创建App
#===============================================================================
def create_customized_app(request):
	#创建app目录
	project_id = request.GET['project_id']
	try:
		app_name, app_display_name = __create_app_files(request, project_id)
	except RuntimeError as e:
		response = create_response(500)
		response.errMsg = e.message
		return response.get_response()
	
	#return create_response(200).get_response()
	if app_model.CustomizedApp.objects.filter(name=app_name).count() > 0:
		app_model.CustomizedApp.objects.filter(name=app_name).delete()
		os._exit(3)

	admin = User.objects.get(username='admin')
	for user in [admin]:
		post = {
			"app_name": app_name,
			"app_display_name": app_display_name,
			"user_id": user.id,
			"remark_name": 'termite',
			"principal": 'termite generated'
		}
		request.POST = post
		app_util.add_app(request)

		app = app_model.CustomizedApp.objects.get(name=app_name)
		request.POST = {
			"id": app.id
		}
		response = app_api_util.create_installed_app(request)
		response_data = json.loads(response.content)
		if response_data['code'] != 200:
			return create_response(500).get_response()		
	
	return create_response(200).get_response()
