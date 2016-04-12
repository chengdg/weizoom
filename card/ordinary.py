# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core.jsonresponse import JsonResponse, create_response

from django.shortcuts import render_to_response
from django.template import RequestContext

from core import resource
from models import *
import json
import nav
import util

class CreateWeizoomCardRule(resource.Resource):
	app = 'card'
	resource = 'ordinary'

	def get(request):
		"""
		创建通用卡规则的页面
		"""
		c = RequestContext(request, {
			'first_nav_name': nav.FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': nav.CARD_ORDINARY_NAV
		})
		return render_to_response('card/ordinary.html', c)

	@login_required
	def api_put(request):
		"""
		创建通用卡规则
		"""
		card_class = WEIZOOM_CARD_ORDINARY  #卡的种类为通用卡
		try:
			util.create_weizoom_card_rule(card_class,request)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'您填写的卡的前缀已存在，请修改后再提交!'
		return response.get_response()
