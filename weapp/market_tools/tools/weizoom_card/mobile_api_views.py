# -*- coding: utf-8 -*-

__author__ = 'bert'

from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core.exceptionutil import unicode_full_stack
from core import core_setting
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from models import *
from modules.member.integral import increase_member_integral
from mall.models import *
from account.views import save_base64_img_file_local_for_webapp
import module_api
import requests
import json

def check_weizoom_card(request):
	"""
	检测微众卡用户名密码
	返回微众卡ID和余额
	data:{
		id: weizoom_card,
		money: round(weizoom_card.money, 2)
	}
	"""
	name = request.POST.get('name','')
	password = request.POST.get('password','')
	# data = dict()
	# msg, weizoom_card = module_api.check_weizoom_card(name, password,request.webapp_user,request.member,request.webapp_owner_id,request.user_profile.webapp_id)

	url = 'http://api.card.com/card/get_cards/?_method=post'
	data_card = {
		"card_infos": '[{"card_number":"%s","card_password": "%s"}]' %(name, password)
	}
	resp = requests.post(url, params=data_card)
	text = json.loads(resp.text)
	card_infos = text['data']['card_infos']

	msg = None
	if card_infos:
		card_infos = card_infos[0][name]
	else:
		msg = u'卡号或密码错误'

	if msg:
		return create_response(500, msg)
	# weizoom_card_rule = WeizoomCardRule.objects.get(id=weizoom_card.weizoom_card_rule_id)
	# is_new_member_special = weizoom_card_rule.is_new_member_special
	response = create_response(200)
	# response.data.id = weizoom_card.id
	# response.data.money = round(weizoom_card.money, 2)
	# response.data.is_new_member_special = is_new_member_special
	response.data.card_infos = card_infos
	response.data.code = 200
	return response.get_response()


# TODO delete
def change_weizoom_card_to_integral(request):
	"""
	微众卡兑换积分，暂不使用
	"""
	response = create_response(500)
	data = dict()
	card_id = request.POST.get('card_id', '')
	webapp_owner_id = request.webapp_owner_id

	if card_id:
		try:
			weizoom_card = WeizoomCard.objects.get(id=card_id)
		except:
			weizoom_card = None
			data['msg'] = u'不存在该微众卡'

		if weizoom_card and weizoom_card.status == WEIZOOM_CARD_STATUS_INACTIVE:
			data['msg'] = u'微众卡未激活'

		if weizoom_card and WeizoomCardUsedAuthKey.is_can_pay(request.COOKIES[core_setting.WEIZOOM_CARD_AUTH_KEY], card_id) and weizoom_card.status != WEIZOOM_CARD_STATUS_INACTIVE:
			integral_each_yuan = IntegralStrategySttings.get_integral_each_yuan(request.user_profile.webapp_id)
			if integral_each_yuan:
				expired_money = weizoom_card.money
				change_integral = weizoom_card.money * integral_each_yuan
				if change_integral > int(change_integral):
					change_integral = int(change_integral) + 1
				change_integral = int(change_integral)
				try:
					log = increase_member_integral(request.member, change_integral, u'积分兑换')

					weizoom_card.money = 0
					weizoom_card.status = WEIZOOM_CARD_STATUS_EMPTY
					weizoom_card.save()
					
					# 创建微众卡日志
					module_api.create_weizoom_card_log(
						webapp_owner_id,
						-1, 
						WEIZOOM_CARD_LOG_TYPE_RETURN_BY_SYSTEM, 
						weizoom_card.id, 
						expired_money,
						log.id if log else 0
					)
					#登录安全
					WeizoomCardUsedAuthKey.objects.filter(auth_key=request.COOKIES[core_setting.WEIZOOM_CARD_AUTH_KEY], weizoom_card_id=card_id).delete()
				except:
					notify_message = u"微众卡兑换积分, cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)
					response = create_response(500)
					response.data = u'兑换失败'
			else:
				response = create_response(500)
				response.data = u'兑换失败'
			
			response = create_response(200)
		elif data.has_key('msg') is False :
			response.data = u'兑换失败'

	response.data = data
	return response.get_response()