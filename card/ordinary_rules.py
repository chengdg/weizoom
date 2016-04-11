# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from core import resource
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required
from core import paginator
import util
from models import *
import nav

class ordinaryRuleList(resource.Resource):
	app = 'card'
	resource = 'ordinary_rules'

	@login_required
	def get(request):
		"""
		显示卡规则列表
		"""
		card_class = WEIZOOM_CARD_ORDINARY  #通用卡
		c = RequestContext(request, {
			'first_nav_name': nav.FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': nav.CARD_ORDINARY_NAV,
		})
		return render_to_response('card/ordinary_rules.html', c)

	@login_required
	def api_get(request):
		"""
		通用卡卡规则列表
		"""
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', 1))
		card_calss = WEIZOOM_CARD_ORDINARY
		pageinfo, cur_weizoom_card_rules = util.get_rule_list(card_calss, cur_page, count_per_page, request)
		response = create_response(200)
		response.data.rows = cur_weizoom_card_rules
		response.data.pagination_info = pageinfo.to_dict()

		return response.get_response()