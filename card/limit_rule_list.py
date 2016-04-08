# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from core import resource
from core.jsonresponse import JsonResponse, create_response
from weapp import export
from django.contrib.auth.decorators import login_required
from core import paginator
from weapp.card import util
from weapp.card_models import *
from weapp.order.userprofile_models import *

class ordinaryRuleList(resource.Resource):
	app = 'weapp'
	resource = 'limit_cards'

	@login_required
	def get(request):
		"""
		显示卡规则列表
		"""
		card_class = WEIZOOM_CARD_LIMIT  #限制卡

		c = RequestContext(request, {
			'first_nav_name': export.MONEY_CARD_FIRST_NAV,
			'second_navs': export.get_card_second_navs(request),
			'second_nav_name': export.MONEY_CARD_MANAGER_NAV,
			'third_nav_name': export.MONEY_CARD_LIMIT_CREATE_NAV,
			'card_class': card_class,
		})
		return render_to_response('templates/editor/list_weizoom_card.html', c)

	@login_required
	def api_get(request):
		"""
		卡规则列表
		"""
		count_per_page = int(request.GET.get('count_per_page', '1'))
		cur_page = int(request.GET.get('page', 1))
		card_calss = WEIZOOM_CARD_LIMIT
		print card_calss," dddddddddddddd"
		pageinfo, cur_weizoom_card_rules = util.get_rule_list(card_calss, cur_page, count_per_page, request)
		response = create_response(200)
		response.data.items = cur_weizoom_card_rules
		response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
		response.data.pageinfo = paginator.to_dict(pageinfo)

		return response.get_response()

def _get_type_value(filter_value):
	if filter_value == '-1':
		return -1
	try:
		for item in filter_value.split('|'):
			if item.split(':')[0] == 'cardType':
				return int(item.split(':')[1])
		return -1
	except:
		return -1
def _get_attr_value(filter_value):
	if filter_value == '-1':
		return -1
	try:
		for item in filter_value.split('|'):
			if item.split(':')[0] == 'cardAttr':
				return int(item.split(':')[1])
		return -1
	except:
		return -1