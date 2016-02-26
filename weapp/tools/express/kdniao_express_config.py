# -*- coding: utf-8 -*-

__author__ = 'justing'

from django.conf import settings

class KdniaoExpressConfig(object):
	"""
	快递配置信息
	"""

	def __init__(self):
		pass
	EBusiness_id = "1256042" #商户id
	api_key = "6642ea21-2d79-4ebc-a451-de4922dcf412"

	watchdog_type = "EXPRESS"

	# 快递鸟订阅请求地址（测试）
	req_url="http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"
	# 快递100订阅请求地址
	api_url = "http://www.kuaidi100.com/poll"
	# api_url = "http://{}/tools/api/express/test_kuaidi_poll/?code=1".format(settings.DOMAIN)
	def get_api_url(self):
		if settings.MODE == 'develop' or settings.MODE == 'test':
			return "http://{}/tools/api/express/test_kuaidi_poll/?code=1".format(settings.DOMAIN)
		else:
			return self.api_url

	# 参数格式
	schema = "json"

	# 授权码
	app_key = "zKcFdoLd2775"

	# 回调地址
	callback_url = "http://{}/tools/api/express/kuaidi/callback/?callbackid={}&version=2.0"

	"""
	跟踪的订单状态
	polling  监控中
	shutdown  结束
	abort  中止
	updateall  重新推送
	"""
	STATUS_POLLING = 'polling'
	STATUS_SHUTDOWN = 'shutdown'
	STATUS_ABORT = 'abort'
	STATUS_UPDATEALL = 'updateall'

	STATUSES = {
		STATUS_POLLING: "监控中",
		STATUS_SHUTDOWN: "结束",
		STATUS_ABORT: "中止",
		STATUS_UPDATEALL: "重新推送"
	}

	"""
	快递单当前签收状态
	0在途中、
	1已揽收、
	2疑难、
	3正常签收或者退回签收、
	4退签、
	5同城派送中、
	6退回、
	7转单
	1：已取件2：在途中 3：签收
	"""
	# STATE_ON_THE_WAY = 0
	# STATE_POSTING = 1
	# STATE_DIFFICULT = 2

	STATE_ON_THE_WAY = 2
	STATE_SIGNED = 3
	
	# STATE_SIGN = 4
	# STATE_DELIVERY_IN_THE_CITY = 5
	# STATE_RETURN = 6
	# STATE_SINGLE = 7
