# -*- coding: utf-8 -*-
from collections import OrderedDict

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
from modules.member import models as member_models
from mall.promotion import utils as mall_api

COUNT_PER_PAGE = 20

ITEM_FOR_DISPLAY = {
	'phone': u'手机',
	'name': u'姓名',
	'email': u'邮箱',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}

class voteParticipance(resource.Resource):
	app = 'apps/vote'
	resource = 'vote_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			vote_participance = app_models.voteParticipance.objects.get(id=request.GET['id'])
			webapp_user_name = member_models.WebAppUser.get_member_by_webapp_user_id(vote_participance.webapp_user_id).username_for_title
			if webapp_user_name == "":
				webapp_user_name = u'非会员'
			termite_data = vote_participance.termite_data
			item_data_list = []

			for k in sorted(termite_data.keys()):
				v = termite_data[k]
				pureName = k.split('_')[1]
				item_data = {}
				item_data['item_name'] = pureName
				if v['type'] == 'appkit.selection':
					value_list = []
					for inner_k, inner_v in v['value'].items():
						if inner_v['isSelect']:
							value_list.append(inner_k.split('_')[1])
					item_data['item_value'] = ','.join(value_list)
				else:
					if pureName in ITEM_FOR_DISPLAY:
						item_data['item_name'] = ITEM_FOR_DISPLAY[pureName]
					else:
						item_data['item_name'] = pureName
					item_data['item_value'] = v['value']
				item_data_list.append(item_data)
		else:
			webapp_user_name = ''
			item_data_list = {}
		response = create_response(200)
		response.data = {
			'webapp_user_name': webapp_user_name,
			'items': item_data_list
		}
		return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		vote_participance = app_models.voteParticipance(**data)
		vote_participance.save()
		
		#调整参与数量
		app_models.vote.objects(id=data['belong_to']).update(**{"inc__participant_count":1})
		
		#活动奖励
		prize = data.get('prize', None)
		error_msg = None
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
					coupon, msg = mall_api.consume_coupon(request.webapp_owner_id, coupon_rule_id, request.member.id)
					if not coupon:
						error_msg = msg
		
		data = json.loads(vote_participance.to_json())
		if 'actionButtons' in request.POST:
			data['actionButtons'] = json.loads(request.POST['actionButtons'])
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg
		response = create_response(200)
		response.data = data
		return response.get_response()

