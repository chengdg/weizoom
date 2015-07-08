# -*- coding: utf-8 -*-

import time

from watchdog.utils import watchdog_info, watchdog_error

from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

from pay.weixin.api.sign import md5_sign
from pay.weixin.api.weixin_pay_api import WeixinHttpClient, WeixinPayApi
from pay.weixin.api.api_pay_queryorder import QueryOrderV2Message, QueryOrderV3Message
from pay.weixin.api.api_pay_unifiedorder import UnifiedOrderMessage 
from pay.weixin.api.api_pay_openid import OpenidMessage


PAY_V2 = 2
PAY_V3 = 3

IS_FOR_JSON = 'json'
IS_FOR_XML = 'xml'

########################################################################
# query_order: 查询订单api
########################################################################
def query_order(request):
	app_id = request.GET.get('app_id', '').strip()
	app_key = request.GET.get('app_key', '').strip()
	partner_id = request.GET.get('partner_id', '')
	partner_key = request.GET.get('partner_key', '')
	out_trade_no = request.GET.get('out_trade_no', '')
	pay_version = request.GET.get('pay_version', PAY_V2)
	
	data = {}
	try:
		# 查询订单获取开始时间
		query_order_start_time = int(time.time() * 1000)
		
		weixin_http_client = WeixinHttpClient()
		if int(pay_version) == PAY_V2:
			message = QueryOrderV2Message(app_id, app_key, partner_id, partner_key, out_trade_no)
			api = WeixinPayApi(weixin_http_client, is_for=IS_FOR_JSON)
		else:
			message = QueryOrderV3Message(app_id, partner_id, partner_key, out_trade_no)
			api = WeixinPayApi(weixin_http_client, is_for=IS_FOR_XML)
		data = api.query_order(message)
		
		# 查询订单获取结束时间
		query_order_end_time = int(time.time() * 1000)
		msg = u'weixin pay, stage:[query order], order_id:{}, consumed:{}ms, result:\n{}'.format(out_trade_no, (query_order_end_time - query_order_start_time), data)
		watchdog_info(msg)
		
		response = create_response(200)
		response.data = data
		return response.get_response()
	except:
		notify_message = u"weixin pay, stage:[query order], result:\n{}, exception:\n{}".format(data, unicode_full_stack())
		watchdog_error(notify_message)
		
		response = create_response(201)
		response.innerErrMsg = unicode_full_stack() 
		return response.get_response()
	
	
########################################################################
# get_unifiedorder: 获取预支付订单号api
########################################################################
def get_unifiedorder(request):
	appid = request.POST.get('appid', '').strip()
	mch_id = request.POST.get('mch_id', '').strip()
	body = request.POST.get('body', '')
	out_trade_no = request.POST.get('out_trade_no', '')
	total_fee = request.POST.get('total_fee', '')
	spbill_create_ip = request.POST.get('spbill_create_ip', '')
	notify_url = request.POST.get('notify_url', '')
	openid = request.POST.get('openid', '')	
	partner_key = request.POST.get('partner_key', '')	
	
	data = {}
	try:
		# 统一支付获取开始时间
		get_unifiedorder_start_time = int(time.time() * 1000)
		
		weixin_http_client = WeixinHttpClient()
		message = UnifiedOrderMessage(appid, mch_id, partner_key, out_trade_no, total_fee, spbill_create_ip, notify_url, openid, body)
		api = WeixinPayApi(weixin_http_client, is_for=IS_FOR_XML)
		data = api.get_unifiedorder(message)
		
		time_stamp = str(int(time.time()))
		pay_sign_args_dict = {
			'appId': appid,
			'timeStamp': time_stamp,
			'nonceStr': data['nonce_str'],
			'package=prepay_id': data['prepay_id'],
			'signType': 'MD5'
		}
		pay_sign_args_keys = sorted(pay_sign_args_dict.keys())
		pay_sign = ''
		for key in pay_sign_args_keys:
			pay_sign += "%s=%s&" % (key, pay_sign_args_dict[key])
		pay_sign += 'key=' + partner_key
		data['pay_sign'] = md5_sign(pay_sign)
		data['time_stamp'] = time_stamp
		
		# 统一支付获取结束时间
		get_unifiedorder_end_time = int(time.time() * 1000)
		msg = u'weixin pay, stage:[get unifiedorder], order_id:{}, consumed:{}ms, result:\n{}'.format(out_trade_no, (get_unifiedorder_end_time - get_unifiedorder_start_time), data)
		watchdog_info(msg)
		
		response = create_response(200)
		response.data = data
		return response.get_response()
	except:
		if data and ( not data.has_key('prepay_id') or not data.has_key('nonce_str') ):
			notify_message = u"weixin pay, stage:[get unifiedorder], order_id:{}, result:\n{}, exception:\n{}".format(out_trade_no, data, unicode_full_stack())
			watchdog_info(notify_message)
		else:
			notify_message = u"weixin pay, stage:[get unifiedorder], order_id:{}, result:\n{}, exception:\n{}".format(out_trade_no, data, unicode_full_stack())
			watchdog_error(notify_message)
		response = create_response(201)
		response.innerErrMsg = unicode_full_stack() 
		return response.get_response()

	
########################################################################
# get_openid: 授权获取openid api
########################################################################
def get_openid(request):
	appid = request.POST.get('appid', '')
	secret = request.POST.get('secret', '')
	code = request.POST.get('code', '')
	grant_type = request.POST.get('grant_type', 'authorization_code')
	
	data = {}
	try:
		# 获取openid开始时间
		get_openid_start_time = int(time.time() * 1000)
		
		weixin_http_client = WeixinHttpClient()
		message = OpenidMessage(appid, secret, code, grant_type)
		api = WeixinPayApi(weixin_http_client, is_for=IS_FOR_JSON)
		data = api.get_openid(message)
		
		if data.has_key('openid'):
			response = create_response(200)
		else:
			response = create_response(201)
			
		# 获取openid结束时间
		get_openid_end_time = int(time.time() * 1000)
		msg = u'weixin pay, stage:[get openid], appid:{}, code:{}, consumed:{}ms, result:\n{}'.format(appid, code, (get_openid_end_time - get_openid_start_time), data)
		watchdog_info(msg)
		
		response.data = data
		return response.get_response()
	except:
		notify_message = u"weixin pay, stage:[get openid], result:\n{}, exception:\n{}".format(data, unicode_full_stack())
		watchdog_error(notify_message)
		
		response = create_response(201)
		response.innerErrMsg = unicode_full_stack() 
		return response.get_response()
