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
		# card_rules = WeizoomCardRule.objects.all()
		# card_rule_list = [{
		# 	'id':card_rule.id,
		# 	'name':card_rule.name,
		# 	'count':card_rule.count
		# }for card_rule in card_rules]
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			# 'card_rule_list':json.dumps(card_rule_list)
		})
		return render_to_response('order/approval_card.html', c)

	def api_get(request):
		"""
		获取卡规则列表
		"""
		common_cur_page = request.GET.get('common_cur_page',1)
		limit_cur_page = request.GET.get('limit_cur_page',1)
		common_count_per_page = request.GET.get('common_count_per_page',8)
		limit_count_per_page = request.GET.get('limit_count_per_page',8)
		card_rule={}
		card_rule['common_card_rule']={}
		card_rule['limit_card_rule'] = {}
		card_rule['common_card_rule']['pageinfo'],card_rule['common_card_rule']['data'] = get_rule_list(0,common_cur_page, common_count_per_page, request) #通用卡
		card_rule['limit_card_rule']['pageinfo'],card_rule['limit_card_rule']['data'] = get_rule_list(1,limit_cur_page, limit_count_per_page, request) #限制卡
		card_rule['common_card_rule']['pageinfo'] = card_rule['common_card_rule']['pageinfo'].to_dict()
		card_rule['limit_card_rule']['pageinfo'] = card_rule['limit_card_rule']['pageinfo'].to_dict()
		response = create_response(200)
		response.data=card_rule
		return response.get_response()