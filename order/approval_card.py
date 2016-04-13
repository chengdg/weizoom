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
SECOND_NAV = 'approval_card'

class ApprovalCard(resource.Resource):
	app = 'order'
	resource = 'approval_card'

	@login_required
	def get(request):
		"""
		显示卡规则列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
		})
		return render_to_response('order/approval_card.html', c)

	def api_get(request):
		"""
		获取卡规则列表
		"""
		cardruletype = request.GET.get('cardruletype','common')
		if cardruletype=='common':
			pageinfo, weizoom_card = get_rule_list(0,request)
		else:
			pageinfo, weizoom_card = get_rule_list(1,request)
		response = create_response(200)
		response.data.rows = weizoom_card
		response.data.pagination_info = pageinfo.to_dict()
		return response.get_response()