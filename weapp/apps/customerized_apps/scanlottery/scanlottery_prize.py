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


class Scanlottery_prize(resource.Resource):
	app = 'apps/scanlottery'
	resource = 'scanlottery_prize'

	def api_put(request):
		"""
		响应PUT
		算法：奖池抽奖球数量=奖品总数量+奖品总数量/中奖概率
			 如，中奖率：15%，奖品总数：500个，则奖池抽奖球个数为：500/15%=3333=3333
		"""
		post = request.POST
		response = create_response(500)
		record_id = post.get('id', None)
		code = post.get('scan_code', None)
		name =  post.get('name', None)
		phone =  post.get('phone', None)
		now_datetime = datetime.today()

		member = request.member
		member_id = member.id
		isMember = member.is_subscribed

		if not record_id:
			response.errMsg = u'抽奖活动信息出错'
			return response.get_response()

		scanlottery = app_models.Scanlottery.objects.get(id=record_id)
		if not scanlottery:
			response.errMsg = u'不存在该活动或已删除'
			return response.get_response()

		#检查码有没有被使用过
		can_play_count = 0
		scanlottery_record = app_models.ScanlotteryRecord.objects(code=code)
		if scanlottery_record.count() == 0:
			# 非会员不可参与
			if isMember:
				can_play_count = 1
		# 如果当前可玩次数为0，则直接返回
		if can_play_count <= 0:
			response = create_response(500)
			response.errMsg = u'该码已经参与'
			return response.get_response()

		#首先检查活动状态
		status_text = scanlottery.status_text
		if status_text != u'进行中':
			response = create_response(500)
			response.errMsg = u'参与抽奖失败，请刷新页面重试~'
			return response.get_response()

		chance = scanlottery.chance / 100.0 #中奖率
		participants_count = scanlottery.participant_count #所有参与的人数
		winner_count = scanlottery.winner_count #中奖人数
		#根据抽奖限制，对比抽奖时间
		allow_repeat = True if scanlottery.allow_repeat == 'true' else False

		#构造奖项池
		prize_tank = []
		scanlottery_prize_dict = scanlottery.prize
		for _, item in scanlottery_prize_dict.items():
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
		cache_key = 'apps_scanlottery_%s_noprizecount' % record_id
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

		member_has_record = app_models.ScanlotteryRecord.objects(belong_to=record_id, member_id=member_id, prize_type__in=['integral','coupon','entity'])
		#如果不能重复中奖，则判断是否之前抽中过
		if not allow_repeat and member_has_record:
			response = create_response(500)
			response.errMsg = u'您已经抽到奖品了,不能重复中奖~'
			return response.get_response()

		#判定是否中奖
		scanlottery_prize_type = "no_prize"
		scanlottery_prize_data = ''

		#收集完所有奖项的数据，打乱奖池list顺序
		random.shuffle(prize_tank)
		#随机抽奖
		scanlottery_prize = random.choice(prize_tank)

		#1、奖品数为0时，不中奖
		#2、根据是否可以重复抽奖和抽到的优惠券规则判断
		SET_CACHE(cache_key, null_prize)
		if not scanlottery_prize:
			result = u'谢谢参与'
			SET_CACHE(cache_key, null_prize - 1)
		else:
			scanlottery_prize_type = scanlottery_prize['prize_type']
			temp_prize_title = result = scanlottery_prize['title']
			#如果抽到的是优惠券，则获取该优惠券的配置
			if scanlottery_prize_type == 'coupon':
				#优惠券
				scanlottery_prize_data = scanlottery_prize['prize_data']['id']
				coupon, msg, _ = get_consume_coupon(scanlottery.owner_id, 'exlottery',str(scanlottery.id), scanlottery_prize_data, member_id)
				if not coupon:
					result = u'谢谢参与'
					scanlottery_prize_type = 'no_prize'
				else:
					prize_value = scanlottery_prize['prize_data']['name']
					scanlottery_prize_dict[temp_prize_title]['prize_count'] = int(scanlottery_prize_dict[temp_prize_title]['prize_count']) - 1
			elif scanlottery_prize_type == 'integral':
				#积分
				member.consume_integral(-int(scanlottery_prize['prize_data']), u'参与扫码抽奖，抽中积分奖项')
				scanlottery_prize_data = scanlottery_prize['prize_data']
				prize_value = u'%s积分' % scanlottery_prize_data
				scanlottery_prize_dict[temp_prize_title]['prize_count'] = int(scanlottery_prize_dict[temp_prize_title]['prize_count']) - 1
			else:
				prize_value = scanlottery_prize['prize_data']
				scanlottery_prize_dict[temp_prize_title]['prize_count'] = int(scanlottery_prize_dict[temp_prize_title]['prize_count']) - 1
			#更新奖品所剩数量
			scanlottery.update(set__prize=scanlottery_prize_dict)
			scanlottery.reload()

		#写日志
		prize_value = result if result == u'谢谢参与' else prize_value
		log_data = {
			"member_id": member_id if member else 0,
			"belong_to": record_id,
			"scanlottery_name": scanlottery.name,
			"prize_type": scanlottery_prize_type,
			"prize_title": result,
			"prize_name": str(prize_value),
			"prize_data": str(scanlottery_prize_data),
			"status": False if scanlottery_prize_type=='entity' else True,
			"created_at": now_datetime,
			"code": code,
			"tel": phone,
			"name": name
		}
		scanlottery_record = app_models.ScanlotteryRecord(**log_data)
		scanlottery_record.save()

		#抽奖后，更新数据
		has_prize = False if result == u'谢谢参与' else True

		#调整参与数量和中奖人数
		newRecord = {}
		if has_prize:
			app_models.Scanlottery.objects(id=record_id).update(inc__winner_count=1)
			newRecord = {
				'created_at': now_datetime.strftime('%Y-%m-%d'),
				'prize_name': prize_value,
				'prize_title': result
			}
		app_models.Scanlottery.objects(id=record_id).update(inc__participant_count=1)

		response = create_response(200)
		response.data = {
			'result': result,
			'newRecord': newRecord,
			"prize_name": prize_value,
			'prize_type': scanlottery_prize_type,
			'can_play_count': 0,
		}
		return response.get_response()