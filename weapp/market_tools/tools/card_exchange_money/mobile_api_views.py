# -*- coding: utf-8 -*-

__author__ = 'aix'

import json
from core.jsonresponse import create_response
from webapp.modules.user_center import request_api_util
from market_tools.tools.weizoom_card import models as card_models
from mall.promotion import models as promotion_models
from mall.promotion import card_exchange_money
from modules.member.models import MemberInfo,Member

def exchange_card(request):
	"""
	兑换卡的api请求
	@param request:
	@return:
	"""
	card_number = json.loads(request.POST.get('card_number',''))
	need_integral = request.POST.get('need_integral','')
	member = request.member
	response = create_response(500)
	if member:
		integral = member.integral
		if int(integral) < int(need_integral):
			response.errMsg = u'现在积分不足,快去获取更多积分吧！'
			return response.get_response()
		member_id = member.id
		owner_name = member.username_hexstr
		webapp_id = request.user_profile.webapp_id
		owner_id = request.webapp_owner_id
		try:
			for number in card_number:
				s_num = number.split('-')[0]
				end_num = number.split('-')[1]
				card_ids_list = card_exchange_money.get_can_exchange_cards_list(s_num,end_num)
				if len(card_ids_list) <= 0:
					response.errMsg = u'该种卡库存不足'
					return response.get_response()
				promotion_models.CardHasExchanged.objects.create(
			 		webapp_id = webapp_id,
			 		card_id = sorted(card_ids_list)[0],
			 		owner_id = member_id,
			 		owner_name = owner_name
			 	)

			member_detail = Member.objects.get(id = member_id)
			member_detail.consume_integral(int(need_integral), u'兑换微众卡,消耗积分')
			response = create_response(200)
			response.data = request.member.integral
			return response.get_response()
		except:
			response.errMsg = u'兑换失败'
			return response.get_response()
		
	else:
		response.errMsg = u'会员信息出错'
		return response.get_response()

def send_captcha(request):
	return request_api_util.send_captcha(request)

def binding_phone(request):
	return request_api_util.binding_phone(request)