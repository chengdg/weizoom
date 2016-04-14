# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core import paginator
import nav
from card.models import *
from card.util import get_rule_list

class CardDatail(resource.Resource):
	app = 'order'
	resource = 'card_detail'


	def api_get(request):
		"""
		获取卡规则列表
		"""
		cur_page = request.GET.get('page', 1)
		rule_id = int(request.GET.get('rule_id', 0))
		card_rules = WeizoomCardRule.objects.filter(id=int(rule_id))
		w_cards = WeizoomCard.objects.filter(weizoom_card_order_item_id__gte=1,weizoom_card_rule_id=rule_id)
		weizoom_card_order_item = WeizoomCardOrderItem.objects.filter(id__in=[w_card.weizoom_card_order_item_id for w_card in w_cards])
		rule_id2rule = {rule.id:rule for rule in card_rules}
		pageinfo, w_cards = paginator.paginate(w_cards, cur_page, 10, query_string=request.META['QUERY_STRING'])
		weizoom_card_list = []
		for w_card in w_cards:
			if w_card.weizoom_card_rule_id in rule_id2rule:
				rule = rule_id2rule[w_card.weizoom_card_rule_id]
				if w_card.operate_status == WEIZOOM_CARD_OPERATE_STATUS_ACTIVED:
					card_status = WEIZOOM_CARD_USE_STATUS2TEXT[w_card.use_status]
				else:
					card_status = WEIZOOM_CARD_OPERATE_STATUS2TEXT[w_card.operate_status]
				weizoom_card_list.append({
					'card_num': w_card.weizoom_card_id,
					'password': w_card.password,
					'card_status': card_status,
					'money': '%.2f' % rule.money,
					'balance': '%.2f' % w_card.money,
					"validate": '',
					'activated_at': '' if not w_card.activated_at else w_card.activated_at.strftime("%Y-%m-%d %H:%M:%S"),
					'remark': w_card.remark
				})
		print weizoom_card_list,66666666666
		response = create_response(200)
		response.data = {
			'rows' : weizoom_card_list,
			'weizoom_card_list' : json.dumps(weizoom_card_list),
			'pagination_info': pageinfo.to_dict()
		}
		return response.get_response()