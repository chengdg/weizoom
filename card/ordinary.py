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
		weizoom_card_id_prefix = request.POST.get('weizoom_card_id_prefix', '')
		if weizoom_card_id_prefix not in [card_rule.weizoom_card_id_prefix for card_rule in WeizoomCardRule.objects.all()]:
			util.create_weizoom_card_rule(card_class,request)
			response = create_response(200)
		else:
			response = create_response(500)
			response.errMg = u'您填写的卡的前缀已存在，请修改后再提交!'
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		更新卡规则信息
		"""
		rule_id = request.POST.get('rule_id',0)
		remark = request.POST.get('remark','')
		count = int(request.POST.get('count',0))
		rule = WeizoomCardRule.objects.filter(id=rule_id)
		print rule_id,remark,"gggggggggg"
		if remark:
			rule.update(remark=remark)
		elif count:
			cur_count = rule[0].count
			count = cur_count + count
			rule.update(count=count)
		response = create_response(200)
		return response.get_response()

