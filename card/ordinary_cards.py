# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from core import resource
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required
from core import paginator
from card.models import *
import nav

class OrdinaryCardList(resource.Resource):
	app = 'card'
	resource = 'ordinary_cards'

	@login_required
	def get(request):
		"""
		显示某一规则下的卡列表
		"""
		weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
		c = RequestContext(request, {
			'first_nav_name': nav.FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': nav.CARD_ORDINARY_NAV,
			'weizoom_card_rule_id': weizoom_card_rule_id
		})
		return render_to_response('card/ordinary_cards.html', c)

	@login_required
	def api_get(request):
		"""
		卡列表
		"""
		weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
		weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=weizoom_card_rule_id)
		is_export = False

		#获得已经过期的微众卡id
		today = datetime.today()
		card_ids_need_expire = []
		for card in weizoom_cards:
			#记录过期并且是未使用的微众卡id
			if card.expired_time:
				if card.expired_time < today:
					card_ids_need_expire.append(card.id)
		if len(card_ids_need_expire) > 0:
			WeizoomCard.objects.filter(id__in=card_ids_need_expire).update(is_expired=True)
		pageinfo, weizoom_cards = paginator.paginate(weizoom_cards, 1, 10, query_string=request.META['QUERY_STRING'])

		print weizoom_card_rule_id,"pppppppppppp"
		weizoom_card_rule = WeizoomCardRule.objects.get(id=weizoom_card_rule_id)
		cur_weizoom_cards = []
		for c in weizoom_cards:
			money = '%.2f' % c.money  #余额
			rule_money = '%.2f' % weizoom_card_rule.money  #面值

			cur_weizoom_cards.append({
				"id": c.id,
				"storage_status": c.storage_status,
				"storage_status_text": WEIZOOM_CARD_STORAGE_STATUS2TEXT[c.storage_status],
				"weizoom_card_id": c.weizoom_card_id,
				"password": c.password,
				"active_card_user_id": c.active_card_user_id,#激活卡用户的id
				"user_id": request.user.id,#当前用户的id
				"money": money, # 余额
				"storage_time": c.storage_time.strftime('%Y-%m-%d %H:%M:%S') if c.activated_at else "",
				"is_expired": c.is_expired,
				"department": c.department,
				"activated_to": c.activated_to,
				"remark": c.remark if c.remark else '',
				"rule_money": rule_money
			})

		response = create_response(200)
		response.data.rows = cur_weizoom_cards
		response.data.pagination_info = pageinfo.to_dict()
		return response.get_response()


def _get_cardNumber_value(filter_value):
	if filter_value == '-1':
		return -1
	try:
		for item in filter_value.split('|'):
			if item.split(':')[0] == 'card_number':
				return item.split(':')[1]
		return -1
	except:
		return -1

def _get_status_value(filter_value):
	if filter_value == '-1':
		return -1
	try:
		for item in filter_value.split('|'):
			if item.split(':')[0] == 'cardStatus':
				return int(item.split(':')[1])
		return -1
	except:
		return -1
