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

class RuleIdList(resource.Resource):
	app = 'order'
	resource = 'rule_id_list'

	def api_get(request):
		"""
		获取卡规则列表
		"""
		order_id = request.GET.get('order_id', 0)
		weizoom_card_order_items = WeizoomCardOrderItem.objects.filter(weizoom_card_order_id=order_id)
		
		rule_ids = sorted([order_item.weizoom_card_rule_id for order_item in weizoom_card_order_items])
		
		response = create_response(200)
		response.data = {
			'rule_id' : rule_ids[0],
		}
		return response.get_response()