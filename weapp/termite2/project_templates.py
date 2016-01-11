# -*- coding: utf-8 -*-

import json
import os
import sys
import zipfile
import shutil

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
from webapp import models as webapp_models
from termite import pagestore as pagestore_manager

COUNT_PER_PAGE = 10
class EmptyProject(object):
	def __init__(self, id, cover_name):
		self.id = id
		self.cover_name = cover_name


class ProjectTemplates(resource.Resource):
	"""
	项目模板集合
	"""
	app = 'termite2'
	resource = 'project_templates'

	def api_get(request):
		"""
		获取模板集合
		"""
		type = request.GET.get('type', 'all')

		manager = User.objects.get(username="manager")
		db_projects = webapp_models.Project.objects.filter(owner=manager, is_enable=True)
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))

		filter_projects = []
		if type == 'all' or type == 'basic_template':
			# 加入 空白模板
			filter_projects.append(EmptyProject(id=-1, cover_name=''))

		for project in db_projects:
			if type != 'all':
				if not type in project.inner_name:
					continue
			if project.inner_name == 'wepage_empty':
				continue
			filter_projects.append(project)

		pageinfo, db_projects = paginator.paginate(filter_projects, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		projects = []
		for project in db_projects:
			data = {
				'id': project.id,
				'cover_url': '/static_v2/img/termite2/cover/%s' % project.cover_name
			}
			projects.append(data)

		data = {
			"items": projects,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}

		response = create_response(200)
		response.data = data
		return response.get_response()
