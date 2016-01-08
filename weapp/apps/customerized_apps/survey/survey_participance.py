# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from apps.customerized_apps.survey.m_survey import Msurvey
from core import resource
from core.jsonresponse import create_response
import models as app_models
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

TEXT_NAME={
	'phone': U'手机',
	'email': U'邮箱',
	'name': u'姓名',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}

class surveyParticipance(resource.Resource):
	app = 'apps/survey'
	resource = 'survey_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		items = []
		if 'id' in request.GET:
			item_data_list = Msurvey.get_surveyparticipance_datas(request)
			if item_data_list:
				items = item_data_list[0]
		response = create_response(200)
		response.data = items
		return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		member_id = request.member.id
		eventParticipance = app_models.surveyParticipance.objects.filter(belong_to=request.POST['belong_to'],member_id=member_id)
		if eventParticipance.count() >0:
			response = create_response(500)
			response.data = u"您已参加过该活动！"
			return response.get_response()
		else:
			data = request_util.get_fields_to_be_save(request)
			survey_participance = app_models.surveyParticipance(**data)
			survey_participance.save()

			#调整参与数量
			app_models.survey.objects(id=data['belong_to']).update(**{"inc__participant_count":1})

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

			data = json.loads(survey_participance.to_json())
			data['id'] = data['_id']['$oid']
			if error_msg:
				data['error_msg'] = error_msg
			response = create_response(200)
			response.data = data
			return response.get_response()