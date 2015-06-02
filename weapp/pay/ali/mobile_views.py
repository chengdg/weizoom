# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import json
import time
from datetime import datetime

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse

from core.exceptionutil import unicode_full_stack

from watchdog.utils import *

from webapp.modules.mall.models import Order
from account.models import UserProfile, UserAlipayOrderConfig

from pay.ali.api.ali_pay_api import AliHttpClient, AliPayApi
from pay.ali.api.api_pay_token import TokenMessage
from pay.ali.api.alipay_request_params import *
from pay.ali.api.alipay_core import *
from pay.ali.api import api_settings

from BeautifulSoup import BeautifulSoup

def _extract_result_from_response(response_data):
	assert (response_data)

	# 以“&”字符切割字符串
	name_value_pairs = response_data.split('&')
	# 把切割后的字符串数组变成变量与数值组合的字典数组
	params = {}
	for name_value_pair in name_value_pairs:
		# 获得第一个=字符的位置
		pos = name_value_pair.find('=')
		name = name_value_pair[:pos]
		value = name_value_pair[pos+1:]
		params[name] = value
	result = {}
	if params.has_key('res_data'):
		res_data = params['res_data']
		res_data_soup = BeautifulSoup(res_data)
		result['token'] = res_data_soup.request_token.text
	else:
		res_error = params['res_error']
		res_error_soup = BeautifulSoup(res_error)
		result['code'] = res_error_soup.code.text
		result['msg'] = res_error_soup.msg.text
		result['detail'] = res_error_soup.detail.text

	return result

def _build_auth_and_execute_raw_request_param(token, partner, key, input_charset, sign_type):
	assert (token)
 
	params = {}
	params[AlipayRequestParams.SERVICE] = api_settings.AUTH_AND_EXECUTE_SERVICE
	params[AlipayRequestParams.PARTNER] = partner
	params['key'] = key
	params[AlipayRequestParams.INPUT_CHARSET] = input_charset
	params[AlipayRequestParams.SEC_ID] = sign_type
	params[AlipayRequestParams.FORMAT] = api_settings.FORMAT
	params[AlipayRequestParams.V] = api_settings.V
 		
	req_data = "<auth_and_execute_req><request_token>{}</request_token></auth_and_execute_req>".format(token)
 
	params[AlipayRequestParams.REQ_DATA] = req_data
 
	return params

def index(request):
	woid = request.GET.get('woid', None)
	order_id = request.GET.get('order_id', None)
	related_config_id = request.GET.get('related_config_id', None)
	
	if not woid or not order_id or not related_config_id:
		return HttpResponse('woid or order_id or related_config_id is none')
	
	data = {}
	try:
		user_profile = UserProfile.objects.get(user_id=woid)
		call_back_url = "http://{}/alipay/mall/pay_result/get/{}/{}/".format(user_profile.host, woid, related_config_id)
		notify_url = "http://{}/alipay/mall/pay_notify_result/get/{}/{}/".format(user_profile.host, woid, related_config_id)
	 	
		order = Order.objects.get(order_id=order_id)
		
		if order.edit_money:
			pay_order_id = '{}-{}'.format(order_id, str(order.edit_money).replace('.','').replace('-',''))
		else:
			pay_order_id = order_id
		
		if settings.USE_MOCK_PAY_API:
			alipay_url = 'http://pay.weapp.com:8003/mockapi/alipay/do_pay/?config_id={}&order_id={}&price={}&call_back_url={}'.format(
				related_config_id, pay_order_id, order.final_price, call_back_url)
		else:
			alipay_config = UserAlipayOrderConfig.objects.get(id=related_config_id)
			partner = alipay_config.partner
			key = alipay_config.key
			input_charset = alipay_config.input_charset
			sign_type = alipay_config.sign_type
			seller_email = alipay_config.seller_email
			
			ali_http_client = AliHttpClient()
			message = TokenMessage(partner, key, input_charset, sign_type, seller_email, pay_order_id, float(order.final_price), notify_url, call_back_url)
			api = AliPayApi(ali_http_client)
			data = api.get_token(message)
			
			result = _extract_result_from_response(data)
			
			msg = u'ali pay, stage:[index], order_id:{}, result:\n{}'.format(order_id, result)
			watchdog_info(msg)
			
			if result.has_key('token'):
				auth_and_execute_requst_params = _build_auth_and_execute_raw_request_param(result['token'], partner, key, input_charset, sign_type)
				request_params_with_sign = build_request_param_with_sign(auth_and_execute_requst_params)
				alipay_url = build_request_url(api_settings.ALIPAY_GATEWAY, request_params_with_sign)
			else:
				return HttpResponse(json.dumps(result), 'application/json; charset=utf-8')
	except:
		print unicode_full_stack()
		error_msg = u'ali pay, stage:[index], result:\n{}, exception:\n{}'.format(data, unicode_full_stack())
		watchdog_error(error_msg)

	return HttpResponseRedirect(alipay_url)
	