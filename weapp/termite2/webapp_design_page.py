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

from termite2 import pagecreater


class WebappDesignPage(resource.Resource):
	"""
	设计页面
	"""
	app = 'termite2'
	resource = 'webapp_design_page'

	@login_required
	def get(request):
		project_id = request.GET['project_id']
		html = pagecreater.create_page(request, return_html_snippet=True)

		c = RequestContext(request, {
			'page_html_content': html,
			'project_id': project_id
		})
		
		return render_to_response('termite2/wepage_design_page.html', c)

	# @login_required
	# def api_post(request):
	# 	response = pagecreater.create_page(request)

	# 	return response