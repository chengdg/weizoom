# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime

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

class RedPacketParticipance(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packet_participance'
	
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			red_packet_participance = app_models.RedPacketParticipance.objects.get(id=request.GET['id'])
			data = red_packet_participance.to_json()
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
			red_packet_id = request.POST['id']
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
			curr_member_red_packet_info = app_models.RedPacketParticipance.objects(belong_to=red_packet_id, member_id=member_id).first()
			ids_tmp = curr_member_red_packet_info.helped_member_id
			#并发问题临时解决方案 ---start
			control_data = {}
			control_data['belong_to'] = red_packet_id
			control_data['member_id'] = member_id
			control_data['helped_member_id'] = int(fid)
			control_data['red_packet_control'] = datetime.now().strftime('%Y-%m-%d')
			try:
				control = app_models.RedPacketControl(**control_data)
				control.save()
			except:
				response = create_response(500)
				response.errMsg = u'只能帮助一次'
				return response.get_response()
			#并发问题临时解决方案 ---end
			if not ids_tmp:
				ids_tmp = [fid]
			else:
				ids_tmp.append(fid)
			curr_member_red_packet_info.update(set__helped_member_id=ids_tmp)
			#更新被帮助者信息
			helped_member_info = app_models.RedPacketParticipance.objects(belong_to=red_packet_id, member_id=int(fid)).first()
			#调整参与数量(首先检测是否已参与)
			if not helped_member_info.has_join:
				helped_member_info.update(set__has_join=True)
			#记录每一次未关注人给予的帮助,已关注的则直接计算帮助值
			if not request.member.is_subscribed:
				red_packet_log = app_models.RedPacketLog(
					belong_to = red_packet_id,
					helper_member_id = member_id,
					be_helped_member_id = int(fid)
				)
				red_packet_log.save()
				has_helped = False
			else:
				#随机区间中获得好友帮助的金额
				red_packet_info = app_models.RedPacket.objects.get(id=red_packet_id)
				money_range_min,money_range_max = red_packet_info.money_range.split('-')
				random_money = '%.2f' % random.uniform(float(money_range_min), float(money_range_max))
				#如果这次随机的金额加上后，当前金额大于目标金额，则将目标金额与当前金额之差当做这次随机出来的数字
				current_money = helped_member_info.current_money + float(random_money)
				if current_money > helped_member_info.red_packet_money:
					random_money = helped_member_info.red_packet_money - helped_member_info.current_money
				helped_member_info.update(inc__current_money=float(random_money))
				helped_member_info.reload()
				#完成目标金额，设置红包状态为成功
				if helped_member_info.current_money == helped_member_info.red_packet_money:
					helped_member_info.update(set__red_packet_status=True)
				has_helped = True
			detail_log = app_models.RedPacketDetail(
				belong_to = red_packet_id,
				owner_id = int(fid),
				helper_member_id = member_id,
				helper_member_name = request.member.username_for_html,
				help_money = random_money,
				has_helped = has_helped,
				created_at = datetime.now()
			)
			detail_log.save()
		except Exception,e:
			print e
			response = create_response(500)
			response.errMsg = u'帮助好友失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()
		help_info = {
			'help_money': random_money,
		}
		response = create_response(200)
		response.data = {
			'help_info': help_info
		}
		return response.get_response()

	def api_post(request):
		"""
		响应POST
		"""
		red_packet_id = request.POST['id']
		fid = request.POST['fid']
		try:
			response = create_response(200)
			helped_member_info = app_models.RedPacketParticipance.objects.get(belong_to=red_packet_id, member_id=int(fid))
			if not helped_member_info.has_join:
				all_participate = app_models.RedPacketParticipance.objects(belong_to=red_packet_id)
				red_packet_info = app_models.RedPacket.objects.get(id=red_packet_id)
				red_packet_type = red_packet_info.type
				if red_packet_type == 'random':
					random_total_money = float(red_packet_info.random_total_money)
					random_packets_number = float(red_packet_info.random_packets_number)
					if random_packets_number > all_participate.count():
						random_average = random_total_money/random_packets_number #红包金额/红包个数
						red_packet_money = random_average + float(red_packet_info.random_random_number_list.pop())
						red_packet_info.update(set__random_random_number_list=red_packet_info.random_random_number_list)
					else:
						response = create_response(500)
						response.errMsg = u'红包已被抢完啦 下次早点来哦'
						return response.get_response()
				else:
					regular_packets_number = red_packet_info.regular_packets_number
					if regular_packets_number > all_participate.count():
						red_packet_money = red_packet_info.regular_per_money #普通红包领取定额金额
					else:
						response = create_response(500)
						response.errMsg = u'红包已被抢完啦 下次早点来哦'
						return response.get_response()
				helped_member_info.update(set__has_join=True,set__created_at=datetime.now(),set__red_packet_money=red_packet_money)
		except Exception,e:
			print e
			response = create_response(500)
		return response.get_response()
