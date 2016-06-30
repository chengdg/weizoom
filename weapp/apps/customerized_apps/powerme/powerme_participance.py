# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

import models as app_models
import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from modules.member.models import Member

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class PowerMeParticipance(resource.Resource):
	app = 'apps/powerme'
	resource = 'powerme_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			powerme_participance = app_models.PowerMeParticipance.objects.get(id=request.GET['id'])
			data = powerme_participance.to_json()
		else:
			data = {}
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	def api_put(request):
		"""
		响应PUT
		"""
		try:

			member_id = request.member.id
			power_id = request.POST['id']
			fid = request.POST['fid']
			user_id = request.webapp_owner_info.user_profile.user_id
			username = User.objects.get(id=user_id).username
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
			detail = app_models.PoweredDetail.objects(belong_to=power_id,power_member_id=member_id)
			if username == 'weshop' and detail.count() > 0:
				app_models.PoweredLimitRelation(
					belong_to=power_id,
					member_id=member_id,
					powered_member_id=fid,
					created_at=datetime.now()
				).save()
				p_member_id= detail.first().owner_id
				username_size_ten = Member.objects.get(id=p_member_id).username_size_ten
				response = create_response(200)
				response.data.powered_member_name = username_size_ten
			else:
				#更新当前membre的参与信息
				try:
					app_models.PowerMeRelations(
						belong_to= power_id,
						member_id= str(member_id),
						powered_member_id= fid
					).save()
				except:
					response = create_response(500)
					response.errMsg = u'只能助力一次'
					return response.get_response()
				# curr_member_power_info = app_models.PowerMeParticipance.objects(belong_to=power_id, member_id=member_id).first()
				# ids_tmp = curr_member_power_info.powered_member_id
				#并发问题临时解决方案 ---start
				# control_data = {}
				# control_data['belong_to'] = power_id
				# control_data['member_id'] = member_id
				# control_data['powered_member_id'] = int(fid)
				# control_data['powerme_control'] = datetime.now().strftime('%Y-%m-%d')
				# try:
				# 	control = app_models.PowerMeControl(**control_data)
				# 	control.save()
				# except:
				# 	response = create_response(500)
				# 	response.errMsg = u'只能助力一次'
				# 	return response.get_response()
				#并发问题临时解决方案 ---end
				# if not ids_tmp:
				# 	ids_tmp = [fid]
				# else:
				# 	ids_tmp.append(fid)
				# curr_member_power_info.update(set__powered_member_id=ids_tmp)
				# ids_tmp = list(set(ids_tmp))
				# sync_result = curr_member_power_info.modify(
				# 	query={'powered_member_id__ne': ids_tmp},
				# 	set__powered_member_id=ids_tmp
				# )
				# print sync_result, '==========================='
				# if not sync_result:
				# 	response = create_response(500)
				# 	response.errMsg = u'操作过于频繁！'
				# 	return response.get_response()
				#更新被助力者信息
				powered_member_info = app_models.PowerMeParticipance.objects(belong_to=power_id, member_id=int(fid)).first()
				#调整参与数量(首先检测是否已参与)
				if not powered_member_info.has_join:
					powered_member_info.update(set__has_join=True)
				#记录每一次未参与人给予的助力,已关注的则直接计算助力值
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
				detail_log = app_models.PoweredDetail(
					belong_to = power_id,
					owner_id = int(fid),
					power_member_id = member_id,
					power_member_name = request.member.username_for_html,
					has_powered = has_powered,
					created_at = datetime.now()
				)
				detail_log.save()
				response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'助力失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()
		return response.get_response()

	def api_post(request):
		"""
		响应POST
		"""
		power_id = request.POST['id']
		fid = request.POST['fid']
		try:
			response = create_response(200)
			powered_member_info = app_models.PowerMeParticipance.objects.get(belong_to=power_id, member_id=int(fid))
			if not powered_member_info.has_join:
				powered_member_info.update(set__has_join=True,set__created_at=datetime.now())
		except:
			response = create_response(500)
		return response.get_response()
