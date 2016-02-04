# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from core import resource
from core.jsonresponse import create_response
import models as app_models
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from modules.member.models import Member
from utils.string_util import byte_to_hex

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

class exsurveyParticipance(resource.Resource):
	app = 'apps/exsurvey'
	resource = 'exsurvey_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		items =[]
		if 'id' in request.GET:
			item_data_list = exsurveyParticipance.get_exsurveyparticipance_datas(request)
			if item_data_list:
				items = item_data_list[0]
		response = create_response(200)
		response.data = items
		return response.get_response()

	@staticmethod
	def get_exsurveyparticipance_datas(request):
		id = request.GET.get('id','')
		export_id = request.GET.get('export_id','')
		exsurvey_participances = None
		if id:
			exsurvey_participances = app_models.exsurveyParticipance.objects.filter(id=id).order_by('-created_at')
		if export_id:
			name = request.GET.get('participant_name', '')
			webapp_id = request.user_profile.webapp_id
			member_ids = []
			if name:
				hexstr = byte_to_hex(name)
				members = Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
				temp_ids = [member.id for member in members]
				member_ids = temp_ids  if temp_ids else [-1]
			start_time = request.GET.get('start_time', '')
			end_time = request.GET.get('end_time', '')
			params = {'belong_to':export_id}
			if member_ids:
				params['member_id__in'] = member_ids
			if start_time:
				params['created_at__gte'] = start_time
			if end_time:
				params['created_at__lte'] = end_time
			exsurvey_participances = app_models.exsurveyParticipance.objects(**params).order_by('-id')
		member_ids = []
		for record in exsurvey_participances:
			member_ids.append(record['member_id'])
		members = Member.objects.filter(id__in=member_ids)
		member_id2member = {member.id: member for member in members}
		item_data_list = []
		for exsurvey_participance in exsurvey_participances:
			result_list = []
			cur_member = member_id2member.get(exsurvey_participance['member_id'], None)
			if cur_member:
				try:
					name = cur_member.username.decode('utf8')
				except:
					name = cur_member.username_hexstr
				username_for_title = cur_member.username_for_title
			else:
				name = username_for_title = u'未知'
			created_at = exsurvey_participance['created_at'].strftime("%Y-%m-%d %H:%M:%S")
			termite_data = exsurvey_participance['termite_data']
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
					if product:
						item_data['item_value'] = product['product_name']
						product_dict['product_id'] = product['product_id']
						product_dict['product_owner_id'] = product['product_owner_id']
						product_dict['product_supplier_id'] = product['product_supplier_id']
						product_dict['product_name'] = product['product_name']
					else:
						item_data['item_value'] = ""
				result_list.append(item_data)
			item_data_list.append({
				'id': str(exsurvey_participance.id),
				'member_id': exsurvey_participance.member_id,
				'name': name,
				'webapp_user_name': username_for_title,
				'created_at': created_at,
				'items': result_list,
				'product_id': product_dict['product_id'] if product_dict else '',
				'product_owner_id': product_dict['product_owner_id'] if product_dict else '',
				'product_supplier_id': product_dict['product_supplier_id'] if product_dict else '',
				'product_name': product_dict['product_name'] if product_dict else ''
			})
		return item_data_list
	
	def api_put(request):
		"""
		响应PUT
		"""
		member_id = request.member.id
		# eventParticipance = app_models.exsurveyParticipance.objects.filter(belong_to=request.POST['belong_to'],member_id=member_id)
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

