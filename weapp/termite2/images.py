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

class Images(resource.Resource):
	app = 'termite2'
	resource = 'images'

	@login_required
	def api_get(request):
		"""
		图片集合
		"""
		images = []
		for image in termite_models.Image.objects.filter(owner=request.user):
			images.append({
				"id": image.id,
				"url": image.url,
				"width": image.width,
				"height": image.height
			})

		response = create_response(200)
		response.data = images
		return response.get_response()
