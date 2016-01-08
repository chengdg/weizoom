# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from core import resource
from core.jsonresponse import create_response
import models as app_models
from apps import request_util
from modules.member import integral as integral_api
from modules.member import models as member_models
from mall.promotion import utils as mall_api
from utils.string_util import byte_to_hex

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
		items ={}
		username_for_title = u''
		if 'id' in request.GET:
			item_data_list = voteParticipance.get_vote_participance_datas(request)
			if item_data_list:
				data = item_data_list[0]
				items = data['items']
				username_for_title = data['username_for_title']
		response = create_response(200)
		response.data = {
			'webapp_user_name': username_for_title,
			'items': items
		}
		return response.get_response()

	@staticmethod
	def get_vote_participance_datas(request):
		#展示个人数据的id
		id =request.GET.get('id',None)
		#用于导出的export_id
		export_id =request.GET.get('export_id',None)
		vote_participances = None
		if id:
			vote_participances = app_models.voteParticipance.objects.filter(id=id)
		if export_id:
			name = request.GET.get('participant_name', '')
			webapp_id = request.user_profile.webapp_id
			member_ids = []
			if name:
				hexstr = byte_to_hex(name)
				members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
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
			vote_participances = app_models.voteParticipance.objects(**params).order_by('-id')
		item_data_list = []
		member_ids = []
		for record in vote_participances:
			member_ids.append(record['member_id'])
		members = member_models.Member.objects.filter(id__in=member_ids)
		member_id2member = {member.id: member for member in members}
		for vote_participance in vote_participances:
			termite_data = vote_participance['termite_data']
			item_list = []
			cur_member = member_id2member.get(vote_participance['member_id'], None)
			if cur_member:
				try:
					name = cur_member.username.decode('utf8')
				except:
					name = cur_member.username_hexstr
				username_for_title = cur_member.username_for_title
			else:
				name = username_for_title = u'未知'
			created_at = vote_participance['created_at'].strftime("%Y-%m-%d %H:%M:%S")
			for k in sorted(termite_data.keys()):
				v = termite_data[k]
				pureName = k.split('_')[1]
				item_data = {}
				item_data['item_name'] = pureName
				if v['type'] in ['appkit.selection', 'appkit.imageselection', 'appkit.textselection']:
					value_list = []
					for inner_k, inner_v in v['value'].items():
						temp_dict = {}
						if inner_v['isSelect']:
							temp_dict['title'] = inner_k.split('_')[1]
							if inner_v.has_key('image'):
								temp_dict['image'] = inner_v['image']
							value_list.append(temp_dict)
					item_data['item_value'] = value_list
				else:
					if pureName in ITEM_FOR_DISPLAY:
						item_data['item_name'] = ITEM_FOR_DISPLAY[pureName]
					else:
						item_data['item_name'] = pureName
					item_data['item_value'] = [{'title': v['value']}]
				item_list.append(item_data)
			item_data_list.append({
				'name': name,
				'username_for_title': username_for_title,
				'created_at': created_at,
				'items': item_list
			})
		return item_data_list
	
	def api_put(request):
		"""
		响应PUT
		"""
		member_id = request.member.id
		eventParticipance = app_models.voteParticipance.objects.filter(belong_to=request.POST['belong_to'],member_id=member_id)
		if eventParticipance.count() >0:
			response = create_response(500)
			response.data = u"您已参加过该活动！"
			return response.get_response()
		else:
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