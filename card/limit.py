# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core.jsonresponse import JsonResponse, create_response

from django.shortcuts import render_to_response
from django.template import RequestContext

import random
from core import resource
from models import *
import json
import nav
import util

class CreateWeizoomCardRule(resource.Resource):
	app = 'card'
	resource = 'limit'

	def get(request):
		"""
		创建限制规则的页面
		"""
		c = RequestContext(request, {
			'first_nav_name': nav.FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': nav.CARD_LIMIT_NAV
		})
		return render_to_response('card/limit.html', c)

	@login_required
	def api_put(request):
		"""
		创建限制卡规则
		"""
		card_class = WEIZOOM_CARD_LIMIT  #卡的种类为限制卡
		weizoom_card_id_prefix = request.POST.get('weizoom_card_id_prefix', '')
		if weizoom_card_id_prefix not in [card_rule.weizoom_card_id_prefix for card_rule in WeizoomCardRule.objects.all()]:
			util.create_weizoom_card_rule(card_class,request)
			response = create_response(200)
		else:
			response = create_response(500)
			response.errMg = u'您填写的卡的前缀已存在，请修改后再提交!'
		return response.get_response()
