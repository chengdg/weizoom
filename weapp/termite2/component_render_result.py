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


class ComponentRenderResult(resource.Resource):
	"""
	component的渲染结果
	"""
	app = 'termite2'
	resource = 'component_render_result'

	@login_required
	def api_put(request):
		response = pagecreater.create_component(request)

		return response
