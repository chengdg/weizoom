# -*- coding: utf-8 -*-

__author__ = 'aix'

from core.jsonresponse import create_response
from webapp.modules.user_center import request_api_util
from market_tools.tools.weizoom_card import models as card_models
from mall.promotion import models as promotion_models
from mall.promotion import card_exchange
from modules.member.models import MemberInfo,Member

def exchange_card(request):
	"""
	兑换卡的api请求
	@param request:
	@return:
	"""
	s_num = request.POST.get('s_num','')
	end_num = request.POST.get('end_num','')
	has_integral = request.POST.get('has_integral','')
	need_integral = request.POST.get('need_integral','')

	request.member.integral = int(has_integral) - int(need_integral)
	request.member.save()
	owner_id = request.webapp_owner_id

	card_ids_list = card_exchange.get_can_exchange_cards_list(s_num,end_num,owner_id)

	webapp_id = request.user_profile.webapp_id
	member_id = request.member.id
	owner_name = request.member.username_for_html

	promotion_models.CardHasExchanged.objects.create(
 		webapp_id = webapp_id,
 		card_id = card_ids_list[0],
 		owner_id = member_id,
 		owner_name = owner_name 
 	)

	response = create_response(200)
	response.data = request.member.integral
	return response.get_response()

def send_captcha(request):
	return request_api_util.send_captcha(request)

def binding_phone(request):
	return request_api_util.binding_phone(request)