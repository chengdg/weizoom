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
		record_id = post['id']
		response = create_response(200)
		result = 0
		if record_id:
			lottery = app_models.lottery.objects.get(id=record_id)
			chance = lottery.chance / 100.0 #中奖率
			participants_count = lottery.participant_count #所有参与的人数
			winner_count = lottery.winner_count #中奖人数
			lottery_type = True if lottery.type == 'true' else False
			#判定是否中奖
			if participants_count == 0 or winner_count / float(participants_count) >= chance:
				result = u'谢谢参与'
			else:
				#中奖，构造奖项池
				prize_tank = []
				coupon_id = -1
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
			response.data = {'index': result}
		else:
			response = create_response(500)
		return response.get_response()