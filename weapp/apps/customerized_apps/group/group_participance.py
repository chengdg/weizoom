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
			power_id = request.POST['id']
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
					belong_to= power_id,
					member_id= str(member_id),
					powered_member_id= fid
				).save()
			except:
				response = create_response(500)
				response.errMsg = u'只能参与一次'
				return response.get_response()

			#更新被参与者信息
			powered_member_info = app_models.GroupRelations.objects(belong_to=power_id, member_id=int(fid)).first()
			#调整参与数量(首先检测是否已参与)
			if not powered_member_info.has_join:
				powered_member_info.update(set__has_join=True)
			#记录每一次未参与人给予的参与,已关注的则直接计算参与值
			if not request.member.is_subscribed:
				power_log = app_models.PowerLog(
					belong_to = power_id,
					power_member_id = member_id,
					be_powered_member_id = int(fid)
				)
				power_log.save()
				has_powered = False
			else:
				powered_member_info.update(inc__power=1)
				has_powered = True
			detail_log = app_models.GroupDetail(
				belong_to = power_id,
				owner_id = int(fid),
				power_member_id = member_id,
				power_member_name = request.member.username_for_html,
				has_powered = has_powered,
				created_at = datetime.now()
			)
			detail_log.save()
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
		group_record_id = request.POST['id']
		member_id = request.POST['fid']
		group_type = request.POST['group_type']
		try:
			response = create_response(200)
			group_member_info = app_models.GroupRelations(
				belong_to = group_record_id,
				member_id = int(member_id),
				group_type = group_type,
				grouped_number = 1,
				grouped_member_ids = list(member_id),
				created_at = datetime.now()
			)
			group_member_info.save()
		except:
			response = create_response(500)
		return response.get_response()


