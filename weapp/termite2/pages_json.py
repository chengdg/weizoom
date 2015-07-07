# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models

import termite.pagestore as pagestore_manager


class PagesJson(resource.Resource):
	app = 'termite2'
	resource = 'pages_json'

	@login_required
	def api_get(request):
		"""
		页面的json数据
		"""
		pagestore = pagestore_manager.get_pagestore('mongo')

		project_id = request.GET['project_id']
		project = webapp_models.Project.objects.get(id=project_id)
		pages = pagestore.get_page_components(project_id)
		
		try:
			pages[0]['model']['site_title'] = project.site_title
		except:
			pass
		
		response = create_response(200)
		response.data = json.dumps(pages)
		return response.get_response()
