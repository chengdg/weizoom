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
from kdniao_express_callback import KdniaoCallbackHandle
from tools.express.tasks import task_kdniao_callback
from kdniao_express_config import KdniaoExpressConfig
from datetime import datetime
from django.conf import settings
import urllib, urllib2, cookielib
import models as express_models
import mall.models as mall_models
import requests

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
	if version == '2.0':
		order = mall_models.Order.objects.get(id=order_id)
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

	if is_finish == 'abort':
		param_json['status'] = "abort"
		param_json['message'] = u"3天查询无记录"
		param_json['lastResult']['data'] = []
		param_json['lastResult']['message'] = u"快递公司参数异常：单号不存在或者已经过期"		

	# 将PARAMETERS的json转换为字符串
	param_str = json.dumps(param_json)
	# print '-------------------------------------------'
	# print api_url
	# print param_str
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
	response = JsonResponse()
	callback_id = request.GET.get('callbackid', -1)
	version = request.GET.get('version', '1')
	order = None
	if version == '2.0':
		express = express_models.ExpressHasOrderPushStatus.get(callback_id)
	else:
		order = mall_api.get_order_by_id(callback_id)
		express = express_models.ExpressHasOrderPushStatus.get_by_order(order)

	data = ExpressCallbackHandle(request, order, express).handle()

	# response.data = data
	# response.data['callback_id'] = callback_id
	# response.data['version'] = version
	for key,value in data.items():
		response.__dict__[key] = value

	return response.get_response()

def kdniao_callback(request):
	print '=================='
	#print request
	print '=================='
	response = JsonResponse()
	#KdniaoCallbackHandle(request).handle()
	task_kdniao_callback.delay(request)
	updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	success_json =  {
		"EBusinessID": KdniaoExpressConfig.EBusiness_id,
		"UpdateTime": updatetime,
		"Success": True,
		"Reason":""
	}
	response.data = success_json
	return response.get_response()



def test_kdniao_push_data(request):	
	#例子www.xxxx.aspx?RequestData=xxxxxx(
	api_url = "http://{}/tools/api/express/kdniao/callback/?RequestData={}".format(settings.DOMAIN, '')
	# 快递信息
	param_json = {
	"EBusinessID": "1256042",
	"Count": "2",
	"PushTime": "2015/3/11 16:21:06",
	"Data": [
		{
			"EBusinessID": "1256042",
			"OrderCode": "",
			"ShipperCode": "EMS",
			"LogisticCode": "5042260908504",
			"Success": True,
			"Reason": "",
			"State": "2",
			"CallBack": "5",
			"Traces": [
				{
					"AcceptTime": "2015-03-06 21:16:58",
					"AcceptStation": "123123深圳市横岗速递营销部已收件，（揽投员姓名：钟定基;联系电话：）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-07 14:25:00",
					"AcceptStation": "离开深圳市 发往广州市",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-08 00:17:00",
					"AcceptStation": "到达广东速递物流公司广航中心处理中心（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-08 01:15:00",
					"AcceptStation": "离开广州市 发往北京市（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-09 09:01:00",
					"AcceptStation": "到达北京黄村转运站处理中心（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-09 18:39:00",
					"AcceptStation": "离开北京市 发往呼和浩特市（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-10 18:06:00",
					"AcceptStation": "到达  呼和浩特市 处理中心",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-11 09:53:48",
					"AcceptStation": "呼和浩特市邮政速递物流分公司金川揽投部安排投递（投递员姓名：安长虹;联系电话：18047140142）",
					"Remark": ""
				}
			]
		},
		{
			"EBusinessID": "1256042",
			"OrderCode": "",
			"ShipperCode": "EMS",
			"LogisticCode": "5042260943004",
			"Success": True,
			"Reason": "",
			"State": "2",
			"CallBack": "4",
			"Traces": [
				{
					"AcceptTime": "2015-03-07 15:26:09",
					"AcceptStation": "深圳市横岗速递营销部已收件，（揽投员姓名：阿凡达周宏彪;联系电话：13689537568）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-08 16:32:00",
					"AcceptStation": "离开深圳市 发往广州市",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-09 00:58:00",
					"AcceptStation": "到达广东速递物流公司广航中心处理中心（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-09 01:15:00",
					"AcceptStation": "离开广州市 发往北京市（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-10 05:20:00",
					"AcceptStation": "到达北京黄村转运站处理中心（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-10 11:59:00",
					"AcceptStation": "离开北京市 发往廊坊市（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-10 14:23:00",
					"AcceptStation": "到达廊坊市处理中心（经转）",
					"Remark": ""
				},
				{
					"AcceptTime": "2015-03-11 08:55:00",
					"AcceptStation": "离开廊坊市 发往保定市（经转）",
					"Remark": ""
				}
			]
		}
	]
}



	# 将PARAMETERS的json转换为字符串
	
	#request = urllib2.Request(url = api_url, data = urllib.urlencode(param_json))
	#
	#
	#
	# request = urllib2.Request(url = api_url, data = json.dumps(param_json))
	# print "data>>>>>",json.dumps(param_json)
	# cookie = cookielib.CookieJar()  
	# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) 
	# response = opener.open(request) 
	# print "2222222"
	# # request = urllib2.Request(api_url, param_data)
	# print "22222223"
	# #response = urllib2.urlopen(request)
	# print "22222224"
	# print "verified_result",response
	# verified_result = response.read()
	
	#方法1
	json_data ={"RequestData":json.dumps(param_json)}
	#json_data = json.dumps(param_json)
	# verified_result = post(api_url,json.dumps(json_data))
	r = requests.post(api_url, json_data)

	print "verified_result",r.text
	print "22222225"
	return HttpResponse(r.text, 'application/json; charset=utf-8')
	#方法1
	"""
	#方法2
	verified_result = post(api_url,json.dumps(param_json))
	# print "verified_result",response
	# verified_result = response.read()
	return HttpResponse(verified_result, 'application/json; charset=utf-8') 
	#方法2
	"""
def post(url, data): 
    req = urllib2.Request(url) 
    #data = urllib.urlencode(data) 
    #enable cookie 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
    response = opener.open(req, data) 
    return response.read() 