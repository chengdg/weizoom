# -*- coding: utf-8 -*-

import logging
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
from termite.core import stripper

from models import *
from account.models import UserProfile
from termite.core.jsonresponse import create_response
import pagerender
import pagestore as pagestore_manager


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
	pagestore = pagestore_manager.get_pagestore(request)
	project_id = request.POST['project_id']
	image = request.POST['image']
	page_id = request.POST['page_id']
	page = json.loads(request.POST['page_json'])
	pagestore.save_page(project_id, page_id, page)

	if image:
		__save_template_picture(request.user.id, project_id, image)
	response = create_response(200)
	return response.get_response()


#######################################################################
# delete_page: 删除一个page
#######################################################################
@login_required
def delete_page(request):
	project_id = request.POST['project_id']
	page_id = request.POST['page_id']

	pagestore = pagestore_manager.get_pagestore(request)
	pagestore.remove_page(project_id, page_id)

	response = create_response(200)
	return response.get_response()


#######################################################################
# update_page_display_index: 调整page的显示顺序
#######################################################################
@login_required
def update_page_display_index(request):
	pagestore = pagestore_manager.get_pagestore(request)
	project_id = request.POST['project_id']
	ordered_pages = request.POST['ordered_pages']

	index = 1
	for page_id in ordered_pages.split(','):
		#Page.objects.filter(project_id=project_id, page_id=page_id).update(display_index=index)
		pagestore.update_page_display_index(project_id, page_id, index)
		index += 1

	response = create_response(200)
	return response.get_response()


#######################################################################
# get_pages_json: 获得page的json内容
#######################################################################
def get_pages_json(request):
	pagestore = pagestore_manager.get_pagestore(request)

	project_id = request.GET['project_id']
	pages = pagestore.get_page_components(project_id)

	response = create_response(200)
	response.data = json.dumps(pages)
	return response.get_response()


#######################################################################
# read_css_content_for: 读取project对应的css文件
#######################################################################
def read_css_content_for(project_id):
	css_dir = os.path.join(settings.TERMITE_HOME, 'project_css')
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
	css_dir = os.path.join(settings.TERMITE_HOME, 'project_css')
	css_file = os.path.join(css_dir, 'project_%s.css' % project_id)
	
	f = open(css_file, 'wb')
	print >> f, content.encode('utf-8')
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
# read_apis_content_for: 读取project对应的apis文件
#######################################################################
def read_apis_content_for(project_id):
	apis_dir = os.path.join(settings.PROJECT_HOME, '../webapp')
	apis_file = os.path.join(apis_dir, 'apis_%s.py' % project_id)

	f = open(apis_file, 'rb')
	content = f.read()
	f.close()

	return content


#######################################################################
# get_apis_content: 获得project的apis内容
#######################################################################
def get_apis_content(request):
	project_id = request.GET['project_id']

	apis_content = read_apis_content_for(project_id)

	response = create_response(200)
	response.data = apis_content
	return response.get_response()


#######################################################################
# write_apis_content_for: 写project对应的apis文件
#######################################################################
def write_apis_content_for(project_id, content):
	apis_dir = os.path.join(settings.PROJECT_HOME, '../webapp')
	apis_file = os.path.join(apis_dir, 'apis_%s.py' % project_id)
	
	f = open(apis_file, 'wb')
	content = content.replace('    ', '\t') #归一化python代码的缩进格式
	print >> f, content.encode('utf-8')
	f.close()

	return True


#######################################################################
# update_apis_content: 更新project的apis内容
#######################################################################
def update_apis_content(request):
	project_id = request.POST['project_id']
	content = request.POST['content']

	write_apis_content_for(project_id, content)

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
# get_project_images: 获得项目图片
#######################################################################
@login_required
def get_project_images(request):
	project_id = request.GET['project_id']

	response = create_response(200)
	response.data = []

	project = Project.objects.get(id=project_id)
	manager = User.objects.get(username='manager')
	if project.owner_id == manager.id:
		dir_path = os.path.join(settings.PROJECT_HOME, '../static/test_resource_img/%s' % project.inner_name)
		if os.path.exists(dir_path):
			for file_name in os.listdir(dir_path):
				response.data.append('/standard_static/test_resource_img/%s/%s' % (project.inner_name, file_name))

	dir_path_suffix = '%d_%s' % (request.user.id, project_id)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	print 'dir_path: ', dir_path

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	for file_name in os.listdir(dir_path):
		response.data.append('/static/upload/%s/%s' % (dir_path_suffix, file_name))
	
	return response.get_response()


#######################################################################
# delete_project_image: 删除项目图片
#######################################################################
@login_required
def delete_project_image(request):
	project_id = request.POST['project_id']
	filename = request.POST.get('filename', None)
	#added by chuter
	if filename is None:
		response = create_response(400)
		response.errMsg = u'非法操作，请稍后重试!'
	else:
		filename = filename.split('/')[-1]

		dir_path_suffix = '%d_%s' % (request.user.id, project_id)
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
		
		file_path = os.path.join(dir_path, filename)
		if os.path.exists(file_path):
			os.remove(file_path)

		response = create_response(200)

	return response.get_response()


#######################################################################
# get_project_nav_icons: 获得导航图标
#######################################################################
@login_required
def get_project_nav_icons(request):
	response = create_response(200)
	data = {}
	icon_names = {
		'icon_White': u'白色系',
	    'icon_Black': u'黑色系',
	    'icon_my': u'我上传的'
	}
	nav_icons_dir = os.path.join(settings.TERMITE_HOME, 'termite_img/nav_icons')
	for dir_name in os.listdir(nav_icons_dir):
		if 'icon_' in  dir_name:
			icon_dir_path = os.path.join(settings.TERMITE_HOME, 'termite_img/nav_icons/%s' % dir_name)
			if os.path.isdir(icon_dir_path):
				dir_name_key = icon_names[dir_name]
				data[dir_name_key] = []
				for file_name in os.listdir(icon_dir_path):
					icon_file_path = os.path.join(settings.TERMITE_HOME, 'termite_img/nav_icons/%s/%s' % (dir_name, file_name))
					if os.path.isfile(icon_file_path) and '.png' in file_name:
						data[dir_name_key].append('/static/termite_img/nav_icons/%s/%s' % (dir_name, file_name))

	user_icon_dir = os.path.join(settings.UPLOAD_DIR, 'user_icon', str(request.user.id))
	data[u'我上传的'] = []
	if os.path.exists(user_icon_dir):
		for file in os.listdir(user_icon_dir):
			data[u'我上传的'].append('/standard_static/upload/user_icon/%d/%s' % (request.user.id, file))

	response.data = data
	return response.get_response()


#######################################################################
# create_page_template: 创建Page模板
#######################################################################
def __save_template_picture(user_id, project_id, image_data):
	data = base64.b64decode(image_data)
	file_name = '%d_%s.png' % (user_id, project_id)
	dir_path = settings.PAGE_TEMPLATE_IMAGE_DIR
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(data)
	dst_file.close()


@login_required
def create_page_template(request):
	project_id = request.POST['project_id']
	page = request.POST['page']
	image = request.POST['image']
	name = request.POST['name']

	__save_template_picture(request.user.id, project_id, image)
	Project.objects.filter(id=project_id).update(name=name)
	return create_response(200).get_response()


#######################################################################
# get_page_templates: 获取pate template集合
#######################################################################
@login_required
def get_page_templates(request):
	project_type = request.GET['project_type']

	system_manager = User.objects.get(username='manager')

	items = [{
		'page_json': "{}",
		'id': 0,
		'url': '',
		'name': u'空白页'
	}]
	for page_template in PageTemplate.objects.filter(owner=system_manager, project_type=project_type):
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