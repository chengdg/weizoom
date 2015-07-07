# -*- coding: utf-8 -*-

import logging
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
import zipfile

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from termite.core.jsonresponse import create_response, JsonResponse
import pagerender
from termite import pagestore as pagestore_manager


#===============================================================================
# show_workspaces : 显示workspace列表
#===============================================================================
@login_required
def show_workspaces(request):
	workspaces = Workspace.objects.filter(owner=request.user)
	c = RequestContext(request, {
		'workspaces': workspaces,
	})
	return render_to_response('workbench/workspaces.html', c)


#===============================================================================
# create_workspace : 创建workspace
#===============================================================================
@login_required
def create_workspace(request):
	Workspace.objects.create(
		owner=request.user, 
		name=request.POST['name'],
	)
	return HttpResponseRedirect('/')


#===============================================================================
# delete_workspace : 删除workspace
#===============================================================================
@login_required
def delete_workspace(request, workspace_id):
	#TODO: 删除workspace的project的所有page
	Workspace.objects.filter(id=workspace_id).delete()
	return HttpResponseRedirect('/');


#===============================================================================
# show_projects : 显示项目列表
#===============================================================================
@login_required
def show_projects(request):
	workspace_id = request.GET['workspace_id']
	projects = Project.objects.filter(owner=request.user, workspace_id=workspace_id)
	c = RequestContext(request, {
		'workspace_id': workspace_id,
		'projects': projects,
	})
	return render_to_response('workbench/projects.html', c)


#===============================================================================
# __create_project_css : 创建project的css文件
#===============================================================================
def __create_project_css(project):
	css_dir = os.path.join(settings.TERMITE_HOME, '..', 'static', 'project_css')
	if not os.path.exists(css_dir):
		os.makedirs(css_dir)

	project_id = project.id
	css_file = os.path.join(css_dir, 'project_%s.css' % project_id)
	if not os.path.exists(css_file):
		f = open(css_file, 'wb')
		print >> f, '/* css conentet for project %s */' % project_id
		f.close()


#===============================================================================
# __create_project_apis_file : 创建project的apis.py文件
#===============================================================================
def __create_project_apis_file(project):
	apis_dir = os.path.join(settings.TERMITE_HOME, '..', 'webapp')

	project_id = project.id
	src_file = os.path.join(apis_dir, 'apis_template.py')
	dst_file = os.path.join(apis_dir, 'apis_%s.py' % project_id)
	shutil.copyfile(src_file, dst_file)


#===============================================================================
# create_project : 创建项目
#===============================================================================
@login_required
def create_project(request):
	project = Project.objects.create(
		owner=request.user, 
		workspace_id=request.POST['workspaceId'],
		name=request.POST['projectName'],
		type=request.POST['projectType']
	)
	#__create_project_css(project)
	#__create_project_apis_file(project)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# copy_project : 复制项目
#===============================================================================
@login_required
def copy_project(request, project_id):
	source_project = Project.objects.get(id=project_id)

	#copy project
	project = Project.objects.create(
		owner=request.user, 
		name=source_project.name + ' COPY',
		type=source_project.type,
		workspace_id=source_project.workspace_id,
		datasource_project_id=source_project.datasource_project_id
	)
	__create_project_css(project)

	#copy pages
	source_pages = Page.objects.filter(project=source_project)
	for source_page in source_pages:
		page = Page.objects.create(
			owner = request.user,
			project = project,
			display_index = source_page.display_index,
			page_id = source_page.page_id,
			json_content = source_page.json_content
		)

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# delete_project : 删除项目
#===============================================================================
@login_required
def delete_project(request, project_id):
	Project.objects.filter(id=project_id).update(type='webapp_bak')
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


#===============================================================================
# export_project : 导出项目的page、css和apis
#===============================================================================
@login_required
def export_project(request):
	pagestore = pagestore_manager.get_pagestore(request)
	project_id = request.GET['project_id']

	#清空下载目录
	download_dir = os.path.join(settings.DOWNLOAD_HOME, 'download', project_id)
	if os.path.exists(download_dir):
		shutil.rmtree(download_dir)
	os.makedirs(download_dir)

	#export page
	for page in pagestore.get_pages(project_id):
		del page['_id']
		f = open(os.path.join(download_dir, 'page_%s.json' % page['page_id']), 'wb')
		print >> f, json.dumps(page, indent=4)
		f.close()

	#export apis.py
	# apis_dir = os.path.join(settings.TERMITE_HOME, '../../webapp')
	# src_file = os.path.join(apis_dir, 'apis_%s.py' % project_id)
	# dst_file = os.path.join(download_dir, 'apis_%s.py' % project_id)
	# shutil.copyfile(src_file, dst_file)

	#export project.css
	# css_dir = os.path.join(settings.TERMITE_HOME, '../../static/project_css')
	# src_file = os.path.join(css_dir, 'project_%s.css' % project_id)
	# dst_file = os.path.join(download_dir, 'project_%s.css' % project_id)
	# shutil.copyfile(src_file, dst_file)	

	#打包
	files = os.listdir(download_dir)
	zip_path = os.path.join(download_dir, 'project_%s.zip' % project_id)
	zip = zipfile.ZipFile(zip_path, 'w')
	for file in files:
		zip.write(os.path.join(download_dir, file), file)
	zip.close()

	path = '/termite_static/%s' % zip_path.replace('\\', '/').split('/static/')[-1]
	return HttpResponseRedirect(path)


#===============================================================================
# import_project : 导入项目的page、css和apis
#===============================================================================
@login_required
def import_project(request):
	'''
	uid = request.POST['uid'][3:]
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')
	'''
	pagestore = pagestore_manager.get_pagestore(request)
	project_id = request.POST['project_id']

	#清空下载目录
	download_dir = os.path.join(settings.DOWNLOAD_HOME, 'download', project_id)
	if os.path.exists(download_dir):
		shutil.rmtree(download_dir)
	os.makedirs(download_dir)

	#获取文件内容
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	#获取文件路径
	file_name = request.POST['Filename']
	file_path = os.path.join(download_dir, file_name)

	#写入文件
	dst_file = open(file_path, 'wb')
	dst_file.write(''.join(content))
	dst_file.flush()
	dst_file.close()

	#创建page, apis.py, project.css
	pagestore.remove_project_pages(project_id)
	zip = zipfile.ZipFile(file_path)
	zip.extractall(download_dir)
	for file in os.listdir(download_dir):
		if file.endswith('.zip'):
			continue

		if file.startswith('page_'):
			src_file = open(os.path.join(download_dir, file), 'rb')
			content = src_file.read()
			src_file.close()
			page_json = json.loads(content)
			page_component = page_json['component']
			page_component['is_new_created'] = True
			page_id = page_json['page_id']
			pagestore.save_page(project_id, page_id, page_component)

		if file.startswith('apis_'):
			#export apis.py
			apis_dir = os.path.join(settings.TERMITE_HOME, '../../webapp')
			src_file = os.path.join(download_dir, file)
			dst_file = os.path.join(apis_dir, 'apis_%s.py' % project_id)
			shutil.copyfile(src_file, dst_file)

		if file.endswith('.css'):
			#export project.css
			css_dir = os.path.join(settings.TERMITE_HOME, '../../static/project_css')
			src_file = os.path.join(download_dir, file)
			dst_file = os.path.join(css_dir, 'project_%s.css' % project_id)
			shutil.copyfile(src_file, dst_file)

	#raise Http404('invalid image')
	return HttpResponse('import success')
	

@login_required
def show_workbench(request, project_id):
	"""
	显示工作台

	URL举例: http://dev.weapp.com/termite/workbench/project/edit/8/
	"""
	project = Project.objects.get(id=project_id)

	pages = []
	'''
	for page in Page.objects.filter(project_id=project_id):
		pages.append(json.loads(page.json_content))

	print json.dumps(pages).replace(r'\\n', r'\\\\n')
	'''

	c = RequestContext(request, {
		'project': project,
		'pages_json': json.dumps(pages)
	})
	return render_to_response('workbench/workbench.html', c)


# #===============================================================================
# # show_mobile_page : 显示移动页面
# #===============================================================================
# def show_mobile_page(request, project_id):
# 	c = RequestContext(request, {
# 		'project_id': project_id
# 	})
# 	return render_to_response('workbench/mobile_page.html', c)


# #===============================================================================
# # show_preview_mobile_page : 显示预览的移动页面
# #===============================================================================
# def show_preview_mobile_page(request, project_id, page_id):
# 	if page_id:
# 		page = Page.objects.get(project_id=project_id, page_id=int(page_id))
# 	else:
# 		page = Page.objects.filter(project_id=project_id).order_by('display_index')[0]
# 	page.component = json.loads(page.json_content)

# 	project = Project.objects.get(id=project_id)
# 	content = pagerender.create_mobile_page_html_content(request, page, page.component, project)

# 	c = RequestContext(request, {
# 		'project_id': project_id,
# 		'content': content
# 	})
# 	return render_to_response('workbench/preview_mobile_page.html', c)


#===============================================================================
# preview_page : 显示预览页面
#===============================================================================
@login_required
def preview_page(request, project_id, page_id):
	project = Project.objects.get(id=project_id)
	host = request.META['HTTP_HOST'].split(':')[0]
	if project.type == 'viper':
		url = 'http://%s/workbench/viper/preview/?project_id=%s' % (host, project_id)
		if page_id:
			url += ('&page_id='+page_id)
	elif project.type == 'jqm':
		url = 'http://%s/workbench/jqm/preview/?project_id=%s' % (host, project_id)
		if page_id:
			url += ('&page_id='+page_id)

	return HttpResponseRedirect(url)


