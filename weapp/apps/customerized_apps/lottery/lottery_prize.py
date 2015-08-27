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
from weixin2 import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from mall.promotion import models as coupon_models

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20


class lottery_prize(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery_prize'

	def api_put(request):
		"""
		响应PUT
		"""

		post = request.POST
		response = create_response(500)
		record_id = post['id']
		data = {}
		if not record_id:
			response.errMsg = u'抽奖活动信息出错'
			return response.get_response()

		webapp_user = getattr(request, 'webapp_user', None)
		if webapp_user:
			webapp_user_id = request.webapp_user.id
			data['webapp_user_id'] = webapp_user_id
		else:
			response.errMsg = u'用户信息出错'
			return response.get_response()

		lottery = app_models.lottery.objects.get(id=record_id)
		if not lottery:
			response.errMsg = u'不存在该活动或已删除'
			return response.get_response()

		chance = lottery.chance / 100.0 #中奖率
		participants_count = lottery.participant_count #所有参与的人数
		winner_count = lottery.winner_count #中奖人数
		limitation = lottery.limitation #抽奖限制
		#根据抽奖限制，对比抽奖时间
		lottery_type = True if lottery.type == 'true' else False
		expend = lottery.expend
		delivery = lottery.delivery
		delivery_setting = lottery.delivery_setting

		member = getattr(request, 'member', None)

		if not member and expend == 0:
			response = create_response(500)
			response.errMsg = u'积分不足，请先关注'
			return response.get_response()

		try:
			if member:
				member_id = request.member.id
				data['member_id'] = member_id
				lottery_participance = app_models.lotteryParticipance.objects.get(belong_to=record_id, member_id=member_id)
			else:
				lottery_participance = app_models.lotteryParticipance.objects.get(belong_to=record_id, webapp_user_id=webapp_user_id)
		except:
			#如果当前用户没有参与过该活动，则创建新记录
			data['belong_to'] = record_id
			data['lottery_date'] = datetime.today()
			data['owner_id'] = request.user.id
			data['count'] = 2 if limitation == 'twice_per_day' else 1 #根据抽奖活动限制，初始化可参与次数
			lottery_participance = app_models.lotteryParticipance(**data)
			lottery_participance.save()

		#根据送积分规则，查询当前用户是否已中奖
		if delivery_setting == 'true':
			pass
		webapp_user.consume_integral(-int(delivery), u'参与抽奖，获得参与积分')
		#判定是否中奖
		if participants_count == 0 or winner_count / float(participants_count) >= chance:
			result = u'谢谢参与'
		else:
			#中奖，构造奖项池
			prize_tank = []
			lottery_prize_count = 0
			pagestore = pagestore_manager.get_pagestore('mongo')
			page = pagestore.get_page(lottery.related_page_id, 1)
			page_components = page['component']['components']
			for sub_components in page_components:
				if sub_components.type == 'appkit.lotterydescription':
					sub_components = sub_components['components']
					for c in sub_components['components']:
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
			#1、奖品数为0时，不中奖
			#2、根据是否可以重复抽奖和抽到的优惠券规则判断
			if lottery_prize_count == 0:
				result = u'谢谢参与'
			else:
				# if lottery_type:
				# 	#如果抽到的是优惠券，则获取该优惠券的配置
				# 	if lottery_prize['prize_type'] == 'coupon':
				# 		coupon_rule = coupon_models.CouponRule.objects.get(id=lottery_prize['prize_data']['id'])
				# 		coupon_limit = coupon_rule.limit_counts
				# 		if coupon_limit <= 1:
							#查询该用户是否已抽到过该优惠券
				result = lottery_prize['title']
				#发奖
		response = create_response(200)
		response.data = {'index': result}
		return response.get_response()