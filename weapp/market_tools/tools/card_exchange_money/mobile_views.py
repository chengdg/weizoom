# -*- coding: utf-8 -*-

__author__ = 'aix'

import os

from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from mall.promotion.card_exchange_money import CardExchangeMoney
from modules.member.models import MemberInfo
from mall.promotion import models as promotion_models
from market_tools.tools.weizoom_card import models as card_models

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_page(request):
	"""
	手机端现金兑换微众卡页面
	"""
	webapp_id = request.user_profile.webapp_id
	#判断用户是否绑定手机号
	member_id = request.member.id
	member_integral = request.member.integral
	phone_number = ''
	try:
		member_info = MemberInfo.objects.get(member_id = member_id)
		member_is_bind = member_info.is_binded
		if member_is_bind:
			phone_number = member_info.phone_number
	except:
		member_is_bind = False

	card_exchange_dic = CardExchangeMoney.get_can_exchange_cards(webapp_id)

	c = RequestContext(request, {
		'card_exchange_rule': card_exchange_dic,
		'member_is_bind': member_is_bind,
		'member_integral': member_integral,
		'phone_number': phone_number,
		# 'user_has_exchange_card': user_has_exchange_card
	})

	return render_to_response('%s/card_exchange_money/webapp/m_card_exchange_money.html' % TEMPLATE_DIR, c)