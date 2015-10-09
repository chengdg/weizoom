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

class SignParticipance(resource.Resource):
	app = 'apps/sign'
	resource = 'sign_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			sign_participance = app_models.SignParticipance.objects.get(id=request.GET['id'])
			data = sign_participance.to_json()
		else:
			data = {}
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		member_id = request.member.id
		activity_id = request.POST['id']
		response = create_response(500)
		if member_id:
			signer = app_models.SignParticipance.objects(belong_to=activity_id, member_id=member_id)
			sign = app_models.Sign.objects.get(id=activity_id)
			if signer.count() > 0:
				signer = signer.first()
			else:
				signer = app_models.SignParticipance(
					belong_to = activity_id,
					member_id = member_id,
					prize = {
						'integral': 0,
						'coupon': ''
					},
					created_at= datetime.today()
				)
				signer.save()
			return_data = signer.do_signment(sign)
			if return_data['status_code'] == app_models.RETURN_STATUS_CODE['SUCCESS']:
				response = create_response(200)
				response.data = {
					'serial_count': return_data['serial_count'],
					'daily_prize': {
						'integral': return_data['daily_integral'],
						'coupon': {
							'id': return_data['daily_coupon_id'],
							'name': return_data['daily_coupon_name']
						}
					},
				}
				if return_data['next_serial_count'] != 0:
					response.data['next_serial_prize'] = {
						'count': return_data['next_serial_count'],
						'prize': {
							'integral': return_data['next_serial_integral'],
							'coupon': {
								'id': return_data['next_serial_coupon_id'],
								'name': return_data['next_serial_coupon_name']
							}
						}
					}
			else:
				response.errMsg = return_data['errMsg']
		return response.get_response()

