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

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class exSignParticipance(resource.Resource):
	app = 'apps/exsign'
	resource = 'exsign_participance'

	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			exsign_participance = app_models.exSignParticipance.objects.get(id=request.GET['id'])
			data = exsign_participance.to_json()
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
			sign = app_models.exSign.objects.get(id=activity_id)
			if sign.status != 1:
				response.errMsg = u'签到活动未开始'
				return response.get_response()

			signer = app_models.exSignParticipance.objects(belong_to=activity_id, member_id=member_id)
			if signer.count() > 0:
				signer = signer.first()
			else:
				signer = app_models.exSignParticipance(
					belong_to = activity_id,
					member_id = member_id,
					prize = {
						'integral': 0,
						'coupon': ''
					},
					created_at= datetime.today()
				)
				signer.save()

			return_data = signer.do_signment(sign, request.member.grade_id)
			detail_dict = {
				'belong_to': activity_id,
				'member_id': member_id,
				'created_at': datetime.today(),
				'type': u'页面签到',
				'prize': {
					'integral': 0,
					'coupon': {
						'id': 0,
						'name': ''
					}
				}
			}
			if return_data['status_code'] == app_models.RETURN_STATUS_CODE['SUCCESS']:
				detail_dict['prize'] = {
					'integral': return_data['curr_prize_integral'],
					'coupon': []
				}
				if return_data['curr_prize_coupon']:
					print return_data['curr_prize_coupon'],"ppppppppppppp"
					for c in return_data['curr_prize_coupon']:
						coupon_flag = c['count'] > 0
						detail_dict['prize']['coupon'].append({
							'id':  c['id'],
							'name':  c['name'] if coupon_flag else u'优惠券已领完,请联系客服补发'
						})
				response = create_response(200)
				response.data = {
					'serial_count': return_data['serial_count'],
					'daily_prize': {
						'integral': return_data['daily_integral'],
						'coupon': return_data['daily_coupon']
					},
					'curr_prize':{
						'integral': return_data['curr_prize_integral'],
						'coupon': return_data['curr_prize_coupon']
					}
				}
				if return_data['next_serial_count'] != 0:
					response.data['next_serial_prize'] = {
						'count': return_data['next_serial_count'],
						'prize': {
							'integral': return_data['next_serial_integral'],
							'coupon': return_data['next_serial_coupon']
						}
					}
				#记录签到历史
				details = app_models.exSignDetails(**detail_dict)
				details.save()
			else:
				response.errMsg = return_data['errMsg']
		return response.get_response()