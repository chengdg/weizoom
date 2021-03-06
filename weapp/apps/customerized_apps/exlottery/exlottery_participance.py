# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from apps.request_util import get_consume_coupon
from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from mall import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class lotteryParticipance(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery_participance'

	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			lottery_participance = app_models.lotteryParticipance.objects.get(id=request.GET['id'])
			data = lottery_participance.to_json()
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
		lottery_participance = app_models.lotteryParticipance(**data)
		lottery_participance.save()
		error_msg = None

		#调整参与数量
		app_models.lottery.objects(id=data['belong_to']).update(**{"inc__participant_count":1})

		#活动奖励
		prize = data.get('prize', None)
		if prize:
			prize_type = prize['type']
			if prize_type == 'no_prize':
				pass #不进行奖励
			elif prize_type == 'integral':
				if not request.member:
					pass #非会员，不进行积分奖励
				else:
					value = int(prize['data'])
					integral_api.increase_member_integral(request.member, value, u'参与活动奖励积分')
			elif prize_type == 'coupon':
				if not request.member:
					pass #非会员，不进行优惠券发放
				else:
					coupon_rule_id = int(prize['data']['id'])
					# coupon, msg = mall_api.consume_coupon(request.webapp_owner_id, coupon_rule_id, request.member.id)
					coupon, msg, _ = get_consume_coupon(request.webapp_owner_id, 'lottery', data['belong_to'], coupon_rule_id, request.member.id)
					if not coupon:
						error_msg = msg

		data = json.loads(lottery_participance.to_json())
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg
		response = create_response(200)
		response.data = data
		return response.get_response()

