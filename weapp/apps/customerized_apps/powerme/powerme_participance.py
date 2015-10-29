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
		try:
			member_id = request.member.id
			power_id = request.POST['id']
			fid = request.POST['fid']
			#更新当前member的参与信息
			curr_member_power_info = app_models.PowerMeParticipance.objects(belong_to=power_id, member_id=member_id).first()
			updated_powered_member_ids = curr_member_power_info.powered_member_id.append(fid)
			curr_member_power_info.update(set__powered_member_id=updated_powered_member_ids)

			#更新被助力者信息
			powered_member_info = app_models.PowerMeParticipance.objects(belong_to=power_id, member_id=int(fid))
			powered_member_info.update(inc__power=1)

			response = create_response(200)
		except Exception,e:
			response = create_response(500)
			response.errMsg = e
		return response.get_response()

