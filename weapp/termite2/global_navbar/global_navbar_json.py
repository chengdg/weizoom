# -*- coding: utf-8 -*-

import json
import qrcode, os

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import termite2.models as termite_models
from django.conf import settings
from termite2 import export
import termite.pagestore as pagestore_manager


FIRST_NAV = export.WEPAGE_FIRST_NAV
class GlobalNavbarJson(resource.Resource):
	"""
	导航
	"""
	app = 'termite2'
	resource = 'global_navbar_json'

	@login_required
	def api_get(request):
		"""
		导航 获取数据
		"""
		pagestore = pagestore_manager.get_pagestore('mongo')

		project_id = request.GET['project_id']
		_, project_type, webapp_owner_id, page_id, mongodb_id = project_id.split(':')
		if mongodb_id == 'new':
			settings_module_path = 'termite2.global_navbar.settings'
			settings_module = __import__(settings_module_path, {}, {}, ['*',])
			pages = [json.loads(settings_module.NEW_PAGE_JSON)['component']]
		else:
			project_id = 'fake:%s:%s:%s' % (project_type, webapp_owner_id, page_id)
			pages = pagestore.get_page_components(project_id)
				
		response = create_response(200)
		response.data = pages
		return response.get_response()