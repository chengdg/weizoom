# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

from termite2 import export
from webapp import models as webapp_models
import models as termite_models

FIRST_NAV = export.WEPAGE_FIRST_NAV
COUNT_PER_PAGE = 20

class Image(resource.Resource):
	app = 'termite2'
	resource = 'image'

	@login_required
	def api_put(request):
		"""
		图片
		"""
		image = termite_models.Image.objects.create(
			owner = request.user, 
			url = request.POST['url'],
			width = request.POST['width'],
			height = request.POST['height'],
		)

		response = create_response(200)
		return response.get_response()
