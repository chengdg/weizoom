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
from modules.member import models as member_models

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
	app = 'apps/exsurvey'
	resource = 'exsurvey_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			exsurvey_participance = app_models.exsurveyParticipance.objects.get(id=request.GET['id'])
			members = member_models.Member.objects.filter(id=exsurvey_participance.member_id)
			if members >0:
				member = members[0]
				if member.is_subscribed:
					webapp_user_name = member.username_for_html
				else:
					webapp_user_name = u"非会员"
			termite_data = exsurvey_participance.termite_data
			item_data_list = []

			product_dict = {}
			for k in sorted(termite_data.keys()):
				v = termite_data[k]
				pureName = k.split('_')[1]
				item_data = {}
				if v['type'] in['appkit.textlist', 'appkit.shortcuts']:
					item_data['type'] = v['type']
					if pureName in TEXT_NAME:#判断是否是自定义的填写项
						item_data['item_name'] = TEXT_NAME[pureName]
					else:
						item_data['item_name'] = pureName
					item_data['item_value'] = v['value']
				elif v['type'] == 'appkit.qa':
					item_data['type'] = v['type']
					item_data['item_name'] = pureName
					item_data['item_value'] = v['value']
				elif v['type'] == 'appkit.selection':
					item_data['type'] = v['type']
					item_data['item_name'] = pureName
					item_data['item_value'] = []
					for sub_k, sub_v in sorted(v['value'].items()):
						if sub_v['isSelect']:
							item_data['item_value'].append(sub_k.split('_')[1])
				elif v['type'] == 'appkit.uploadimg':
					item_data['type'] = []
					item_data['item_name'] = pureName
					item_data['item_value'] = v['value']
				elif v['type'] == 'appkit.dropdownbox':
					product = v['value']
					item_data['type'] = v['type']
					item_data['item_name'] = pureName
					item_data['item_value'] = product['product_name']
					product_dict['product_id'] = product['product_id']
					product_dict['product_owner_id'] = product['product_owner_id']
					product_dict['product_supplier_id'] = product['product_supplier_id']
					product_dict['product_name'] = product['product_name']
				item_data_list.append(item_data)
		else:
			exsurvey_participance = None
			webapp_user_name = ''
			item_data_list = {}
			product_dict = {}
		response = create_response(200)

		response.data = {
			'webapp_user_name': webapp_user_name,
			'items': item_data_list,
			'member_id': exsurvey_participance.member_id if exsurvey_participance else '',
			'created_at' : exsurvey_participance.created_at.strftime("%Y-%m-%d %H:%M:%S") if exsurvey_participance else '',
			'id': str(exsurvey_participance.id) if exsurvey_participance else '',
			'product_id': product_dict['product_id'] if product_dict else '',
			'product_owner_id': product_dict['product_owner_id'] if product_dict else '',
			'product_supplier_id': product_dict['product_supplier_id'] if product_dict else '',
			'product_name': product_dict['product_name'] if product_dict else ''
		}
		return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		member_id = request.member.id
		eventParticipance = app_models.exsurveyParticipance.objects.filter(belong_to=request.POST['belong_to'],member_id=member_id)
		# if eventParticipance.count() >0:
		# 	response = create_response(500)
		# 	response.data = u"您已参加过该活动！"
		# 	return response.get_response()
		# else:
		data = request_util.get_fields_to_be_save(request)
		survey_participance = app_models.exsurveyParticipance(**data)
		survey_participance.save()

		#调整参与数量
		app_models.exsurvey.objects(id=data['belong_to']).update(**{"inc__participant_count":1})

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

