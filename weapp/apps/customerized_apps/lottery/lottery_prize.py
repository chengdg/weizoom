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

import models as app_models
from mall import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from mall.promotion import models as coupon_models
from market_tools.tools.coupon.util import consume_coupon
from termite import pagestore as pagestore_manager
from modules.member.models import Member as member_models

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20


class lottery_prize(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery_prize'

	def api_get(request):
		"""
		响应GET
		"""
		lottery_id = request.GET['id']
		member_id = request.member.id
		all_prize_type_list = ['integral', 'coupon', 'entity']
		lotteries = app_models.lottoryRecord.objects(belong_to=lottery_id, member_id=member_id, prize_type__in=all_prize_type_list)

		data = [{
			'created_at': l.created_at.strftime('%Y-%m-%d'),
			'prize_name': l.prize_name,
			'prize_title': l.prize_title
		} for l in lotteries]
		#获取当前用户剩余积分
		response = create_response(200)
		response.data.history = data
		response.data.remained_integral = request.member.integral

		return response.get_response()

	def api_post(request):
		"""
		响应POST
		"""
		tel = request.POST['tel']
		lottery_id = request.POST['id']
		member_id = request.member.id
		try:
			if tel:
				latest_record = app_models.lottoryRecord.objects(member_id=member_id, belong_to=lottery_id).first()
				latest_record.update(set__tel=tel)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'更新数据失败'
		return response.get_response()


	def api_put(request):
		"""
		响应PUT
		"""

		post = request.POST
		response = create_response(500)
		record_id = post['id']
		data = {}
		now_datetime = datetime.today()
		if not record_id:
			response.errMsg = u'抽奖活动信息出错'
			return response.get_response()

		lottery = app_models.lottery.objects.get(id=record_id)
		if not lottery:
			response.errMsg = u'不存在该活动或已删除'
			return response.get_response()

		webapp_user_id = request.webapp_user.id

		chance = lottery.chance / 100.0 #中奖率
		participants_count = lottery.participant_count #所有参与的人数
		winner_count = lottery.winner_count #中奖人数
		limitation = lottery.limitation_times #抽奖限制
		#根据抽奖限制，对比抽奖时间
		allow_repeat = True if lottery.allow_repeat == 'true' else False
		expend = lottery.expend
		delivery = lottery.delivery
		delivery_setting = lottery.delivery_setting

		member = getattr(request, 'member', None)

		if member.integral < expend:
			response = create_response(500)
			response.errMsg = u'积分不足，请先关注'
			return response.get_response()

		member_id = member.id
		data['member_id'] = member_id
		data['webapp_user_id'] = webapp_user_id
		lottery_participances = app_models.lotteryParticipance.objects(belong_to=record_id, member_id=member_id)
		if lottery_participances.count() != 0:
			lottery_participance = lottery_participances.first()
		else:
			#如果当前用户没有参与过该活动，则创建新记录
			data['belong_to'] = record_id
			data['lottery_date'] = now_datetime
			data['owner_id'] = request.user.id
			data['can_play_count'] = limitation #根据抽奖活动限制，初始化可参与次数
			lottery_participance = app_models.lotteryParticipance(**data)
			lottery_participance.save()

		#扣除抽奖消耗的积分
		member.consume_integral(expend, u'参与抽奖，消耗积分')
		#判定是否中奖
		lottery_prize_type = "no_prize"
		lottery_prize_data = ''
		if participants_count == 0 or (winner_count / float(participants_count) >= chance):
			result = u'谢谢参与'
			#根据送积分规则，查询当前用户是否已中奖
			if delivery_setting == 'false' or not lottery_participance.has_prize:
				member.consume_integral(-delivery, u'参与抽奖，获得参与积分')
		else:
			#中奖，构造奖项池
			prize_tank = []
			lottery_prize_count = 0
			pagestore = pagestore_manager.get_pagestore('mongo')
			page = pagestore.get_page(lottery.related_page_id, 1)
			page_components = page['component']['components']
			for sub_components in page_components:
				if sub_components['type'] == 'appkit.lotterydescription':
					sub_components = sub_components['components']
					for c in sub_components:
						model = c['model']
						prize = model['prize']

						prize_count = int(model['prize_count'])
						lottery_prize_count += prize_count
						prize_item = {
							'title': model['title'],
							'prize_count': prize_count,
							'prize_type': prize['type'],
							'prize_data': prize['data']
						}
						prize_tank.append(prize_item)
			#收集完所有奖项的数据，打乱奖池list顺序
			random.shuffle(prize_tank)
			#随机抽奖
			lottery_prize = random.choice(prize_tank)
			lottery_prize_type = lottery_prize['prize_type']
			#1、奖品数为0时，不中奖
			#2、根据是否可以重复抽奖和抽到的优惠券规则判断
			if lottery_prize_count == 0  or (not allow_repeat and lottery_participance.has_prize):
				result = u'谢谢参与'
			else:
				temp_prize_title = result = lottery_prize['title']
				#奖项的奖品数为0则不中奖
				lottery_prize_count = int(lottery.prize[result])
				if lottery_prize_count > 0:
					#如果抽到的是优惠券，则获取该优惠券的配置
					if lottery_prize_type == 'coupon':
						#优惠券
						lottery_prize_data = couponRule_id = lottery_prize['prize_data']['id']
						coupon_rule = coupon_models.CouponRule.objects.get(id=couponRule_id)
						coupon_limit = coupon_rule.limit_counts
						has_coupon_count = app_models.lottoryRecord.objects(member_id=member_id, belong_to=record_id, prize_type='coupon', prize_data=couponRule_id).count()
						if has_coupon_count >= coupon_limit:
							result = u'谢谢参与'
						else:
							consume_coupon(lottery.owner_id, lottery_prize_data, member_id)
							prize_value = lottery_prize['prize_data']['name']
					elif lottery_prize_type == 'integral':
						#积分
						member.consume_integral(-int(lottery_prize['prize_data']), u'参与抽奖，抽中积分奖项')
						lottery_prize_data = lottery_prize['prize_data']
						prize_value = u'%d积分' % lottery_prize_data
					else:
						prize_value = lottery_prize['prize_data']
					lottery.prize[temp_prize_title] = lottery_prize_count-1
					lottery.save()
				else:
					result = u'谢谢参与'

		#写日志
		prize_value = result if result == u'谢谢参与' else prize_value
		log_data = {
			"member_id": member_id if member else 0,
			"belong_to": record_id,
			"lottery_name": lottery.name,
			"prize_type": lottery_prize_type,
			"prize_title": result,
			"prize_name": str(prize_value),
			"prize_data": str(lottery_prize_data),
			"status": False if lottery_prize_type=='entity' else True,
			"created_at": now_datetime
		}
		app_models.lottoryRecord(**log_data).save()

		#抽奖后，更新数据
		has_prize = False if result == u'谢谢参与' else True
		lottery_participance.update(**{"set__has_prize":has_prize, "inc__total_count":1})
		#根据抽奖次数限制，更新可抽奖次数
		lottery_participance.update(dec__can_play_count=1)
		lottery_participance.reload()
		#调整参与数量和中奖人数
		newRecord = {}
		if has_prize:
			app_models.lottery.objects(id=record_id).update(inc__winner_count=1)
			newRecord = {
				'created_at': now_datetime.strftime('%Y-%m-%d'),
				'prize_name': prize_value,
				'prize_title': result
			}
		app_models.lottery.objects(id=record_id).update(inc__participant_count=1)

		response = create_response(200)
		response.data = {
			'result': result,
			'newRecord': newRecord,
			"prize_name": prize_value,
			'prize_type': lottery_prize_type,
			'can_play_count': lottery_participance.can_play_count,
			'remained_integral': member_models.objects.get(id=member_id).integral
		}
		return response.get_response()