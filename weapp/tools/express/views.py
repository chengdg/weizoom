# -*- coding: utf-8 -*-

__author__ = "liupeiyu"

import json

from django.http import HttpResponseRedirect, HttpResponse
from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core.exceptionutil import full_stack, unicode_full_stack
from watchdog.utils import watchdog_fatal, watchdog_info
from express_order_query import *
import util
import mall.module_api as mall_api
from handle_express_callback import ExpressCallbackHandle
from django.conf import settings
import urllib, urllib2
import models as express_models

EXPRESS_TYPE = 'EXPRESS_API'

########################################################################
# get_test: 模拟快递100返回json数据
########################################################################
def get_test(request):
	com = request.GET.get('nu', '')
	if len(com.strip()) == 0:
		data_info = u"""{"message":"ok","status":"0","state":"0","data":[]}"""
	else:
		data_info = u"""{"message":"ok","status":"1","state":"3","data":[{"time":"2012-07-07 13:35:14","context":"客户已签收"},{"time":"2012-07-07 09:10:10","context":"离开 [北京_房山营业所_石景山营业厅] 派送中，递送员[温]，电话[]"},{"time":"2012-07-06 19:46:38","context":"到达 [北京_房山营业所_石景山营业厅]"},{"time":"2012-07-06 15:22:32","context":"离开 [北京_房山营业所_石景山营业厅] 派送中，递送员[温]，电话[]"},{"time":"2012-07-06 15:05:00","context":"到达 [北京_房山营业所_石景山营业厅]"},{"time":"2012-07-06 13:37:52","context":"离开 [北京_同城中转站] 发往 [北京_房山营业所_石景山营业厅]"},{"time":"2012-07-06 12:54:41","context":"到达 [北京_同城中转站]"},{"time":"2012-07-06 11:11:03","context":"离开 [北京运转中心_航空_驻站班组] 发往 [北京_同城中转站]"},{"time":"2012-07-06 10:43:21","context":"到达 [北京运转中心_航空_驻站班组]"},{"time":"2012-07-05 21:18:53","context":"离开 [福建_厦门支公司] 发往 [北京运转中心_航空]"},{"time":"2012-07-05 20:07:27","context":"已取件，到达 [福建_厦门支公司]"}]}"""
	return HttpResponse(data_info, 'application/json; charset=utf-8')


def test_kuaidi_poll(request):	
	code = request.GET.get('code', 1)
	if int(code) == 1:
		data_info = u"""{
			"result": "true",
			"returnCode": "200",
			"message":"提交成功"
		}"""

	else:
		data_info = u"""{
			"result": "false",
			"returnCode": "500",
			"message": "提交失败"
		}"""

	return HttpResponse(data_info, 'application/json; charset=utf-8')

def test_analog_push_data(request):	
	order_id = request.GET.get('order_id', 2)
	is_finish = request.GET.get('is_finish', 'error')
	version = request.GET.get('v', '1')
	if version == 2:
		express = express_models.ExpressHasOrderPushStatus.get_by_order(order)
		order_id = express.id

	api_url = "http://{}/tools/api/express/kuaidi/callback/?callbackid={}&version={}".format(settings.DOMAIN, order_id, version)
	# 快递信息
	param_json = {
		"status":"polling",
		"lastResult":{
			"state":"0",
			"ischeck":"0",
			"com":"yuantong",
			"nu":"V030344422",
			"data":[{
				"context":"快递员派送",
				"time":"2012-08-30 09:09:36",
				"ftime":"2012-08-30 09:09:36"
			},{
				"context":"到北京",
				"time":"2012-08-29 10:23:04",
				"ftime":"2012-08-29 10:23:04"
			},{
				"context":"上海分拨中心/装件入车扫描 ",
				"time":"2012-08-28 16:33:19",
				"ftime":"2012-08-28 16:33:19"
			},{
				"context":"上海分拨中心/下车扫描 ",
				"time":"2012-08-27 23:22:42", 
				"ftime":"2012-08-27 23:22:42",
			},{
				"context":"收件",
				"time":"2012-08-27 18:22:42", 
				"ftime":"2012-08-27 18:22:42",
			}]
		}
	}
	if is_finish == 'success':
		param_json['status'] = "shutdown"
		param_json['lastResult']['state'] = "3"
		param_json['lastResult']['data'].insert(0, {"context": "本人已签收", "time": "2012-08-30 16:52:02", "ftime": "2012-08-30 16:52:02"})

	# 将PARAMETERS的json转换为字符串
	param_str = json.dumps(param_json)
	print '-------------------------------------------'
	print api_url
	print param_str
	json_data = {
		"param": param_str
	}
	param_data = urllib.urlencode(json_data)
	request = urllib2.Request(api_url, param_data)
	response = urllib2.urlopen(request)
	verified_result = response.read()
	return HttpResponse(verified_result, 'application/json; charset=utf-8')


########################################################################
# get_order_info: 获得快递单信息
########################################################################
def get_order_info(request):
	express_company = request.GET.get('company', '')
	express_number = request.GET.get('number', '')
	order_by = request.GET.get('order_by', 'desc')

	response = create_response(200)
	try:
		query = ExpressOrderQuery(request, express_company, express_number, order_by)
		json_data = query.get_express_order_data()
		response.data = json_data
	except:
		response = create_response(500)
		response.errMsg = u'获取失败'
		response.innerErrMsg = full_stack()
		watchdog_fatal(u'代码错误！%s' % response.innerErrMsg, EXPRESS_TYPE)

	return response.get_response()


########################################################################
# get_companies: 获得快递公司信息
########################################################################
def get_companies(request):
	response = create_response(200)
	response.data = util.get_express_company_json()
	return response.get_response()


def kuaidi_callback(request):
	"""
	快递100 推送回调接口
	"""
	response = create_response(200)
	callback_id = request.GET.get('callbackid', -1)
	version = request.GET.get('version', '1')
	order = None
	if version == '2.0':
		express = express_models.ExpressHasOrderPushStatus.get(callback_id)
	else:
		order = mall_api.get_order_by_id(callback_id)
		express = express_models.ExpressHasOrderPushStatus.get_by_order(order)

	data = ExpressCallbackHandle(request, order, express).handle()

	response.data = data
	response.data['callback_id'] = callback_id
	response.data['version'] = version
	return response.get_response()