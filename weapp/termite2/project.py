# -*- coding: utf-8 -*-

import json
import os
import sys
import zipfile
import shutil
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models
from termite import pagestore as pagestore_manager
from utils import cache_util

EMPTY_PROJECT_ID = -1


class Project(resource.Resource):
	app = 'termite2'
	resource = 'project'

	@staticmethod
	def delete_webapp_page_cache(webapp_owner_id, project_id):
		key = 'termite_webapp_page_%s_%s' % (webapp_owner_id, project_id)
		cache_util.delete_cache(key)


	@staticmethod
	def create_empty_page(project):
		"""
		从硬盘导入空page的json数据到mongodb
		"""
		pagestore = pagestore_manager.get_pagestore_by_type('mongo')
		custom_template_source_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules/viper_workspace_home_page/project_wepage_template_base/')
		pages_data_file_path = os.path.join(custom_template_source_dir, 'pages.json')
		pages_data_file = open(pages_data_file_path, 'rb')
		content = pages_data_file.read()
		pages_data_file.close()
		page = json.loads(content)[0]
		page_id = page['page_id']
		page_component = page['component']
		page_component['is_new_created'] = True
		pagestore.save_page(str(project.id), page_id, page_component)

		return True

	@staticmethod
	def create_empty_app_page(request):
		"""
		创建新的
		"""
		_, app_name, _ = request.GET['project_id'].split(':')
		page_component = json.loads(request.POST['page_json'])
		page_component['is_new_created'] = True
		page_id = 1
		project_id = 'app:%s:%s:%s' % (app_name, request.manager.id, time.time())
		pagestore = pagestore_manager.get_pagestore_by_type('mongo')
		pagestore.save_page(project_id, page_id, page_component)

		page = pagestore.get_page(project_id, page_id)
		new_project_id = str(page['_id'])
		pagestore.update_page_project_id(project_id, page_id, new_project_id)
		return new_project_id

	@staticmethod
	def copy_page(project, source_template_id):
		"""
		从mongodb中拷贝现存project的page数据
		"""
		pagestore = pagestore_manager.get_pagestore_by_type('mongo')
		page_id = 1
		page = pagestore.get_page(source_template_id, page_id)
		page_component = page['component']
		page_component['is_new_created'] = True

		pagestore.save_page(str(project.id), page_id, page_component)
		return True

	@login_required
	def api_put(request):
		"""
		创建模板项目
		"""
		#创建数据库中的数据
		workspace = webapp_models.Workspace.objects.get(owner=request.manager, inner_name='home_page')
		count = webapp_models.Project.objects.filter(owner=request.manager, inner_name__startswith='wepage').count()
		project = webapp_models.Project.objects.create(
			owner = request.manager, 
			inner_name = 'wepage',
			workspace_id = workspace.id,
			name = u'定制模板{}'.format(count+1),
			type = 'wepage'
		)

		if request.user.is_manager:
			inner_name = 'wepage_basic_template'
		else:
			inner_name = 'wepage_%d' % project.id
		webapp_models.Project.objects.filter(id=project.id).update(inner_name=inner_name)

		source_template_id = int(request.POST.get('source_template_id', -1))		
		if source_template_id == EMPTY_PROJECT_ID:
			Project.create_empty_page(project)
		else:
			Project.copy_page(project, source_template_id)

		response = create_response(200)
		response.data = {
			'project_id': project.id
			#'page_id': page_id
		}
		return response.get_response()

	@staticmethod
	def import_from_zip_file(request):
		"""
		从zip file中抽取page信息，导入mongodb中
		"""
		pagestore = pagestore_manager.get_pagestore('mongo')
		project_id = request.POST['id']

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

				Project.update_project_site_title(project_id, page_component)

		return True

	@staticmethod
	def update_page_content(request):
		"""
		更新page内容
		"""
		pagestore = pagestore_manager.get_pagestore('mongo')
		project_id = request.POST['id']
		page_id = request.POST['page_id']
		page = json.loads(request.POST['page_json'])
		pagestore.save_page(project_id, page_id, page)

		Project.update_project_site_title(project_id, page)

	@staticmethod
	def update_app_page_content(request):
		"""
		更新app page内容
		"""
		_, app_name, project_id = request.GET['project_id'].split(':')
		pagestore = pagestore_manager.get_pagestore('mongo')
		page_id = 1
		page = json.loads(request.POST['page_json'])
		pagestore.save_page(project_id, page_id, page)

	@staticmethod
	def update_project_site_title(project_id, page):
		site_title = page['model']['site_title']
		webapp_models.Project.objects.filter(id=project_id).update(site_title=site_title)

	@login_required
	def api_post(request):
		"""
		保存(更新)模板项目
		"""
		project_id = request.POST['id']
		field = request.POST['field']
		if field == 'page_content_from_zip':
			if not Project.import_from_zip_file(request):
				response = create_response(501)
				response.errMsg = u'导入page失败'
				return response.get_response()				
		elif field == 'page_content':
			project_id = request.GET.get('project_id', '')
			if project_id.startswith('fake:'):
				_, project_type, webapp_owner_id, page_id, mongodb_id = project_id.split(':')
				pagestore = pagestore_manager.get_pagestore_by_type('mongo')
				page_component = json.loads(request.POST['page_json'])
				if mongodb_id == 'new':
					page_component['is_new_created'] = True		
				real_project_id = 'fake:%s:%s:%s' % (project_type, webapp_owner_id, page_id)			
				pagestore.save_page(real_project_id, page_id, page_component)

				if mongodb_id == 'new':
					page = pagestore.get_page(real_project_id, page_id)
					result_project_id = 'fake:%s:%s:%s:%s' % (project_type, webapp_owner_id, page_id, str(page['_id']))
				else:
					result_project_id = project_id
				response = create_response(200)
				response.data = result_project_id
				return response.get_response()
			if project_id.startswith('new_app:'):
				if project_id.endswith(':0'):
					project_id = Project.create_empty_app_page(request)
					response = create_response(200)
					response.data = {
						'project_id': project_id
					}
					return response.get_response()
				else:
					Project.update_app_page_content(request)
			else:
				Project.update_page_content(request)
				#清除webapp page cache
				Project.delete_webapp_page_cache(request.manager.id, project_id)
		elif field == 'is_enable':
			webapp_models.Project.objects.filter(id=project_id).update(is_enable=True)
		else:
			if field[0] == '[':
				fields = json.loads(field)
				values = json.loads(request.POST['value'])
				options = dict(zip(fields, values))
			else:
				value = request.POST['value']
				options = {field:value}
			webapp_models.Project.objects.filter(id=project_id).update(**options)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		#删除mongo中project所有的page
		project_id = request.POST['id']
		pagestore = pagestore_manager.get_pagestore_by_type('mongo')
		pagestore.remove_project_pages(str(project_id))

		#删除project本身
		webapp_models.Project.objects.filter(owner=request.manager, id=project_id).delete()

		#清除webapp page cache
		Project.delete_webapp_page_cache(request.manager.id, project_id)
		
		response = create_response(200)
		return response.get_response()










from django.db.models import signals
from weapp.hack_django import post_update_signal
from weapp.hack_django import post_delete_signal
from mall import models as mall_models
import cache
from webapp import models as webapp_models

def delete_webapp_page_cache(**kwargs):
	if hasattr(cache, 'request') and cache.request.user_profile:
		webapp_owner_id = cache.request.user_profile.user_id
		for project in webapp_models.Project.objects.filter(owner_id=webapp_owner_id, type='wepage'):
			key = 'termite_webapp_page_%s_%s' % (webapp_owner_id, project.id)
			cache_util.delete_cache(key)

post_update_signal.connect(delete_webapp_page_cache, sender=mall_models.Product, dispatch_uid = "termite_product.update")
signals.post_save.connect(delete_webapp_page_cache, sender=mall_models.Product, dispatch_uid = "termite_product.save")
signals.post_save.connect(delete_webapp_page_cache, sender=mall_models.ProductCategory, dispatch_uid = "termite_product_category.save")
post_delete_signal.connect(delete_webapp_page_cache, sender=mall_models.ProductCategory, dispatch_uid = "termite_product_category.delete")
signals.post_save.connect(delete_webapp_page_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "termite_category_has_product.save")
post_delete_signal.connect(delete_webapp_page_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "termite_category_has_product.delete")

