# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class PowerMeParticipance(resource.Resource):
	app = 'apps/powerme'
	resource = 'powerme_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			powerme_participance = app_models.PowerMeParticipance.objects.get(id=request.GET['id'])
			data = powerme_participance.to_json()
		else:
			data = {}
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		powerme_participance = app_models.PowerMeParticipance(**data)
		powerme_participance.save()
		error_msg = None
		
		#调整参与数量
		app_models.PowerMe.objects(id=data['belong_to']).update(**{"inc__participant_count":1})
		

		data = json.loads(powerme_participance.to_json())
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg
		response = create_response(200)
		response.data = data
		return response.get_response()

