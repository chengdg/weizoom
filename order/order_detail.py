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

FIRST_NAV = 'rule_order'
SECOND_NAV = 'rule_order'

class OrderDatail(resource.Resource):
	app = 'order'
	resource = 'order_detail'

	@login_required
	def get(request):
		"""
		显示卡规则列表
		"""
		card_rule_order_id = request.GET.get('order_id',0)
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'card_rule_order_id': card_rule_order_id
		})
		return render_to_response('order/order_detail.html', c)

	def api_get(request):
		"""
		获取卡规则列表
		"""
		cur_page = request.GET.get('page', 1)
		order_id = request.GET.get('order_id', 0)
		weizoom_card_order_items = WeizoomCardOrderItem.objects.filter(weizoom_card_order_id=order_id)
		card_rules = WeizoomCardRule.objects.all()
		w_cards = WeizoomCard.objects.filter(weizoom_card_order_item_id__gte=1)

		rule_id2rule = {rule.id:rule for rule in card_rules}
		rule_id2weizoom_card_id = {}
		for w_card in w_cards:
			if w_card.weizoom_card_rule_id in rule_id2weizoom_card_id:
				rule_id2weizoom_card_id[w_card.weizoom_card_rule_id].append(w_card.weizoom_card_id)
			else:
				rule_id2weizoom_card_id[w_card.weizoom_card_rule_id] = [w_card.weizoom_card_id]
		
		pageinfo, weizoom_card_order_items = paginator.paginate(weizoom_card_order_items, cur_page, 10, query_string=request.META['QUERY_STRING'])
		order_item_list = []
		for order_item in weizoom_card_order_items:
			rule_id = order_item.weizoom_card_rule_id
			count = order_item.weizoom_card_order_item_num
			valid_restrictions = rule_id2rule[rule_id].valid_restrictions
			money = float('%.2f' %rule_id2rule[rule_id].money)
			weizoom_card_ids = [] if rule_id not in rule_id2weizoom_card_id else sorted(rule_id2weizoom_card_id[rule_id])
			weizoom_card_id_first = weizoom_card_ids[0]
			weizoom_card_id_last = weizoom_card_ids[-1]
			order_item_list.append({
				'rule_id': '%s' % rule_id,
				'name': u'' if rule_id not in rule_id2rule else rule_id2rule[rule_id].name,
				'money': '%s' % money,
				'count': count,
				'total_money' : '%.2f' %(money*count),
				'card_kind': WEIZOOM_CARD_CLASS2TEXT[rule_id2rule[rule_id].card_class],
				'valid_restrictions': u'满%.f使用' % valid_restrictions if valid_restrictions != -1 else u'不限制',
				'shop_limit_list': rule_id2rule[rule_id].shop_limit_list,
				'card_range': u'%s-%s' % (weizoom_card_id_first, weizoom_card_id_last)
			})
		print order_item_list,7777777777777777
		response = create_response(200)
		response.data = {
			'rows' : order_item_list,
			'pagination_info': pageinfo.to_dict()
		}
		return response.get_response()