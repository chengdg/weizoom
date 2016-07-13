# -*- coding: utf-8 -*-

import json
import random
import datetime as dt
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
from utils.cache_util import GET_CACHE, SET_CACHE

import models as app_models
from mall import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from mall.promotion import models as coupon_models
from market_tools.tools.coupon.util import consume_coupon
from termite import pagestore as pagestore_manager
from modules.member.models import Member as member_models

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20


class exlottery_prize(resource.Resource):
	app = 'apps/exlottery'
	resource = 'exlottery_prize'

	def api_post(request):
		"""
		响应POST
		"""
		tel = request.POST['tel']
		exlottery_id = request.POST['id']
		member_id = request.member.id
		try:
			if tel:
				latest_record = app_models.ExlottoryRecord.objects(member_id=member_id, belong_to=exlottery_id).first()
				latest_record.update(set__tel=tel)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'更新数据失败'
		return response.get_response()

	def api_put(request):
		"""
		响应PUT
		算法：奖池抽奖球数量=奖品总数量+奖品总数量/中奖概率
			 如，中奖率：15%，奖品总数：500个，则奖池抽奖球个数为：500/15%=3333=3333
		"""
		post = request.POST
		response = create_response(500)
		record_id = post.get('id', None)
		code = post.get('ex_code', None)
		now_datetime = datetime.today()

		member = request.member
		member_id = member.id
		webapp_user_id = request.webapp_user.id

		if not record_id:
			response.errMsg = u'抽奖活动信息出错'
			return response.get_response()

		exlottery = app_models.Exlottery.objects.get(id=record_id)
		if not exlottery:
			response.errMsg = u'不存在该活动或已删除'
			return response.get_response()

		#检查码有没有被使用过
		can_play_count = 0
		exlottery_participance = app_models.ExlotteryParticipance.objects(code=code, belong_to=record_id, member_id=member_id)
		if exlottery_participance.count() == 1:
			# 如果绑定，验证抽奖码有没有抽奖
			if exlottery_participance.first().status == app_models.NOT_USED:
				can_play_count = 1
		# 如果当前可玩次数为0，则直接返回
		if can_play_count <= 0:
			response = create_response(500)
			response.errMsg = u'该抽奖码已经被使用过~'
			return response.get_response()

		#首先检查活动状态
		status_text = exlottery.status_text
		if status_text != u'进行中':
			response = create_response(500)
			response.errMsg = u'参与抽奖失败，请刷新页面重试~'
			return response.get_response()

		chance = exlottery.chance / 100.0 #中奖率
		participants_count = exlottery.participant_count #所有参与的人数
		winner_count = exlottery.winner_count #中奖人数
		#根据抽奖限制，对比抽奖时间
		allow_repeat = True if exlottery.allow_repeat == 'true' else False
		# expend = exlottery.expend
		# delivery = exlottery.delivery

		# if not member or member.integral < expend:
		# 	response = create_response(500)
		# 	response.errMsg = u'积分不足'
		# 	return response.get_response()

		#构造奖项池
		prize_tank = []
		exlottery_prize_dict = exlottery.prize
		for _, item in exlottery_prize_dict.items():
			prize_count = int(item['prize_count'])
			for i in range(prize_count):
				prize_item = {
					'title': item['title'],
					'prize_count': prize_count,
					'prize_type': item['prize_type'],
					'prize_data': item['prize_data']
				}
				prize_tank.append(prize_item)
		curr_tank_size = len(prize_tank)
		cache_key = 'apps_exlottery_%s_noprizecount' % record_id
		cache_count = GET_CACHE(cache_key)
		if cache_count or cache_count == 0:
			null_prize = int(cache_count)
		else:
			null_prize = int(curr_tank_size / chance) - curr_tank_size
		prize_tank.extend([None for _ in range(null_prize)])
		if len(prize_tank) <= 0:
			response = create_response(500)
			response.errMsg = u'奖品已抽光'
			return response.get_response()

		member_has_record = app_models.ExlottoryRecord.objects(belong_to=record_id, member_id=member_id, prize_type__in=['integral','coupon','entity'])
		#如果不能重复中奖，则判断是否之前抽中过
		if not allow_repeat and member_has_record:
			response = create_response(500)
			response.errMsg = u'您已经抽到奖品了,不能重复中奖~'
			return response.get_response()

		#扣除抽奖消耗的积分
		# member.consume_integral(expend, u'参与抽奖，消耗积分')
		#奖励抽奖赠送积分
		# member.consume_integral(-delivery, u'参与抽奖，获得参与积分')
		#判定是否中奖
		exlottery_prize_type = "no_prize"
		exlottery_prize_data = ''

		#收集完所有奖项的数据，打乱奖池list顺序
		random.shuffle(prize_tank)
		#随机抽奖
		exlottery_prize = random.choice(prize_tank)

		#1、奖品数为0时，不中奖
		#2、根据是否可以重复抽奖和抽到的优惠券规则判断
		SET_CACHE(cache_key, null_prize)
		if not exlottery_prize:
			result = u'谢谢参与'
			SET_CACHE(cache_key, null_prize - 1)
		else:
			exlottery_prize_type = exlottery_prize['prize_type']
			temp_prize_title = result = exlottery_prize['title']
			#如果抽到的是优惠券，则获取该优惠券的配置
			if exlottery_prize_type == 'coupon':
				#优惠券
				exlottery_prize_data = exlottery_prize['prize_data']['id']
				coupon, msg, _ = get_consume_coupon(exlottery.owner_id, 'exlottery',str(exlottery.id), exlottery_prize_data, member_id)
				if not coupon:
					result = u'谢谢参与'
					exlottery_prize_type = 'no_prize'
				else:
					prize_value = exlottery_prize['prize_data']['name']
					exlottery_prize_dict[temp_prize_title]['prize_count'] = int(exlottery_prize_dict[temp_prize_title]['prize_count']) - 1
			elif exlottery_prize_type == 'integral':
				#积分
				member.consume_integral(-int(exlottery_prize['prize_data']), u'参与抽奖，抽中积分奖项')
				exlottery_prize_data = exlottery_prize['prize_data']
				prize_value = u'%s积分' % exlottery_prize_data
				exlottery_prize_dict[temp_prize_title]['prize_count'] = int(exlottery_prize_dict[temp_prize_title]['prize_count']) - 1
			else:
				prize_value = exlottery_prize['prize_data']
				exlottery_prize_dict[temp_prize_title]['prize_count'] = int(exlottery_prize_dict[temp_prize_title]['prize_count']) - 1
			#更新奖品所剩数量
			exlottery.update(set__prize=exlottery_prize_dict)
			exlottery.reload()

		#写日志
		prize_value = result if result == u'谢谢参与' else prize_value
		log_data = {
			"member_id": member_id if member else 0,
			"belong_to": record_id,
			"exlottery_name": exlottery.name,
			"prize_type": exlottery_prize_type,
			"prize_title": result,
			"prize_name": str(prize_value),
			"prize_data": str(exlottery_prize_data),
			"status": False if exlottery_prize_type=='entity' else True,
			"created_at": now_datetime,
			"code": code
		}
		exlottery_record = app_models.ExlottoryRecord(**log_data)
		exlottery_record.save()
		#更新码的使用时间
		exlottery_code = app_models.ExlotteryCode.objects(belong_to=record_id, code=code).first()
		exlottery_code.update(set__use_time=exlottery_record.created_at)
		#抽奖后，更新数据
		has_prize = False if result == u'谢谢参与' else True

		exlottery_participance.update(set__status=app_models.HAS_USED)
		exlottery_participance.first().reload()
		#调整参与数量和中奖人数
		newRecord = {}
		if has_prize:
			app_models.Exlottery.objects(id=record_id).update(inc__winner_count=1)
			newRecord = {
				'created_at': now_datetime.strftime('%Y-%m-%d'),
				'prize_name': prize_value,
				'prize_title': result
			}
		app_models.Exlottery.objects(id=record_id).update(inc__participant_count=1)

		response = create_response(200)
		response.data = {
			'result': result,
			'newRecord': newRecord,
			"prize_name": prize_value,
			'prize_type': exlottery_prize_type,
			'can_play_count': 0,
			# 'remained_integral': member_models.objects.get(id=member_id).integral
		}
		return response.get_response()