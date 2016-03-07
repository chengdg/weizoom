# -*- coding: utf-8 -*-

import json
from datetime import datetime
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from django.template import RequestContext
from django.shortcuts import render_to_response
from core.exceptionutil import unicode_full_stack

import models as app_models
from modules.member.models import Member

COUNT_PER_PAGE = 20

class GroupParticipance(resource.Resource):
	app = 'apps/group'
	resource = 'group_participance'
	
	# @login_required
	# def api_get(request):
	# 	"""
	# 	响应GET api
	# 	"""
	# 	if 'id' in request.GET:
	# 		group_participance = app_models.GroupParticipance.objects.get(id=request.GET['id'])
	# 		data = group_participance.to_json()
	# 	else:
	# 		data = {}
	# 	response = create_response(200)
	# 	response.data = data
	# 	return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		try:

			member_id = request.member.id
			relation_belong_to = request.POST['id']
			fid = request.POST['fid']
			try:
				fid_member = Member.objects.get(id=fid)
				if not fid_member.is_subscribed:
					response = create_response(500)
					response.errMsg = u'该用户已退出活动'
					return response.get_response()
			except:
				response = create_response(500)
				response.errMsg = u'不存在该会员'
				return response.get_response()
			#更新当前member的参与信息
			try:
				app_models.GroupRelations(
					belong_to= relation_belong_to,
					member_id= str(member_id),
					powered_member_id= fid
				).save()
			except:
				response = create_response(500)
				response.errMsg = u'只能参与一次'
				return response.get_response()

			#更新被参与者信息
			powered_member_info = app_models.GroupRelations.objects(belong_to=relation_belong_to, member_id=int(fid)).first()
			#调整参与数量(首先检测是否已参与)
			if not powered_member_info.has_join:
				powered_member_info.update(set__has_join=True)

			group_detail = app_models.GroupDetail(
				relation_belong_to = relation_belong_to,
				owner_id = int(fid),
				grouped_member_id = member_id,
				grouped_member_name = request.member.username_for_html,
				created_at = datetime.now()
			)
			group_detail.save()
		except:
			response = create_response(500)
			response.errMsg = u'参与失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()
		response = create_response(200)
		return response.get_response()

	def api_post(request):
		"""
		我要开团
		"""
		group_record_id = request.POST['group_record_id']
		member_id = request.POST['fid']
		group_type = request.POST['group_type']
		try:
			response = create_response(200)
			group_member_info = app_models.GroupRelations(
				belong_to = group_record_id,
				member_id = member_id,
				group_type = group_type,
				grouped_number = 1,
				grouped_member_ids = list(member_id),
				created_at = datetime.now()
			)
			group_member_info.save()
			data = json.loads(group_member_info.to_json())
			relation_belong_to = data['_id']['$oid']
			group_detail = app_models.GroupDetail(
				relation_belong_to = relation_belong_to,
				owner_id = member_id,
				grouped_member_id = member_id,
				grouped_member_name = request.member.username_for_html,
				created_at = datetime.now()
			)
			group_detail.save()
		except:
			response = create_response(500)
			response.errMsg = u'只能开团一次'
		return response.get_response()


