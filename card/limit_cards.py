# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from core import resource
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required
from core import paginator
from models import *
from weapp.models import *
import nav
import util

class OrdinaryCardList(resource.Resource):
	app = 'card'
	resource = 'limit_cards'

	@login_required
	def get(request):
		"""
		显示某一规则下的卡列表
		"""
		weizoom_card_rule_id = request.GET.get('weizoom_card_rule_id', '-1')
		c = RequestContext(request, {
			'first_nav_name': nav.FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': nav.CARD_LIMIT_NAV,
			'weizoom_card_rule_id': weizoom_card_rule_id
		})
		return render_to_response('card/limit_cards.html', c)

	@login_required
	def api_get(request):
		"""
		卡列表
		"""
		pageinfo, cur_weizoom_cards = util.get_card_list(request)

		response = create_response(200)
		response.data.rows = cur_weizoom_cards
		response.data.pagination_info = pageinfo.to_dict()
		return response.get_response()