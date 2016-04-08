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

class createWeizoomCardRule(resource.Resource):
	app = 'card'
	resource = 'create_ordinary'

	def get(request):
		"""
		创建通用卡规则的页面
		"""
		c = RequestContext(request, {
			'first_nav_name': nav.FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': nav.CARD_ORDINARY_NAV
		})
		return render_to_response('card/create_ordinary.html', c)

	@login_required
	def api_put(request):
		"""
		创建通用卡规则
		"""
		card_class = WEIZOOM_CARD_ORDINARY  #卡的种类为通用卡
		name = request.POST.get('name', '')
		weizoom_card_id_prefix = request.POST.get('weizoom_card_id_prefix', '')
		money = request.POST.get('money', '')
		remark = request.POST.get('remark', '')
		count = int(request.POST.get('count', ''))
		card_kind = int(request.POST.get('card_kind', 0))  #卡的类型
		shop_limit_list = request.POST.get('shop_limit_list','-1')
		is_new_member_special = int(request.POST.get('is_new_member_special', 0))
		valid_restrictions = request.POST.get('fullUseValue', -1)

		if weizoom_card_id_prefix not in [card_rule.weizoom_card_id_prefix for card_rule in WeizoomCardRule.objects.all()]:
			rule = WeizoomCardRule.objects.create(
				owner_id=request.user.id,
				name=name,
				weizoom_card_id_prefix=weizoom_card_id_prefix,
				money=money,
				remark=remark,
				count=count,
				card_class=card_class,
				card_kind=card_kind,
				shop_limit_list=shop_limit_list,
				is_new_member_special=is_new_member_special,
				valid_restrictions=valid_restrictions if valid_restrictions else -1
				)
			print name,weizoom_card_id_prefix,money,remark,count,card_kind,shop_limit_list,is_new_member_special,"pppppppppp"
			#生成微众卡
			create_weizoom_card(rule, count, request)

			response = create_response(200)
			response.data.id = rule.id
		else:
			response = create_response(500)
			response.errMsg = u'您填写的卡的前缀已存在，请修改后再提交!'
		return response.get_response()


def create_weizoom_card(rule,count,request,is_append=False):
	"""
	生成微众卡
	"""
	count = int(count)
	weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=rule.id).order_by('-id')
	if weizoom_cards:
		card_number = int(weizoom_cards[0].weizoom_card_id[:3])
	else:
		card_number = int(u'000000')

	passwords = set([w.password for w in WeizoomCard.objects.filter(owner=request.user)])

	create_list = []
	for i in range(count):
		card_number = int(card_number) + 1
		card_number = '%06d' % card_number
		weizoom_card_id = '%s%s' % (str(rule.weizoom_card_id_prefix), card_number)
		password = create_weizoom_card_password(passwords)
		create_list.append(WeizoomCard(
			owner_id=request.user.id,
			weizoom_card_rule_id=rule.id,
			weizoom_card_id=weizoom_card_id,
			money=rule.money,
			password=password,
			active_card_user_id=0
		))
		print "hhhh"
		passwords.add(password)
	WeizoomCard.objects.bulk_create(create_list)


def create_weizoom_card_password(passwords):
	"""
	生成微众卡密码
	"""
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	while True:
		password = '%s' % ''.join(random.sample(random_args_value, 7))
		if password not in passwords:
			break

	return password
