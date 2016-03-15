# -*- coding: utf-8 -*-

__author__ = 'aix'

import os

from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from mall.promotion.card_exchange import CardExchange
from modules.member.models import MemberInfo
from mall.promotion import models as promotion_models
from market_tools.tools.weizoom_card import models as card_models

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_page(request):
	"""
	手机端卡兑换页
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

	card_exchange_dic = CardExchange.get_can_exchange_cards(request,webapp_id)

	weizoom_card_id = 0
	cur_user_has_exchange_card = promotion_models.CardHasExchanged.objects.filter(webapp_id = webapp_id,owner_id = member_id)
	cards = card_models.WeizoomCard.objects.all()
	card_id2weizoom_card_id = {card.id: card.weizoom_card_id for card in cards}
	user_has_exchange_card = False
	if cur_user_has_exchange_card.count() > 0 :
		user_has_exchange_card = True
		card_id = cur_user_has_exchange_card[0].card_id
		weizoom_card_id = card_id2weizoom_card_id.get(card_id,None)
		print weizoom_card_id,55555
	prize_list = card_exchange_dic['prize']

	if weizoom_card_id:
		for p in prize_list:
			s_w_id = int(p['s_num'])
			e_w_id = int(p['end_num'])
			if int(weizoom_card_id) >= s_w_id and int(weizoom_card_id) <= e_w_id:
				p['is_selected'] = True
			else:
				p['is_selected'] = False

	c = RequestContext(request, {
		'card_exchange_rule': card_exchange_dic,
		'member_is_bind': member_is_bind,
		'member_integral': member_integral,
		'phone_number': phone_number,
		'user_has_exchange_card': user_has_exchange_card
	})

	return render_to_response('%s/card_exchange/webapp/m_card_exchange.html' % TEMPLATE_DIR, c)