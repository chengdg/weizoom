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

FIRST_NAV = 'rule_order'
SECOND_NAV = 'approval_card'

class approvalCard(resource.Resource):
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