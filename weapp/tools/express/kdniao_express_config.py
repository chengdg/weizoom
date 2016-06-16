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

	# 快递鸟订阅请求地址（测试）(无论bdd还是真实环境都是这个url)
	req_url="http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"
	#电子面单地址
	eorder_url = 'http://testapi.kdniao.cc:8081/api/eorderservice'

	# api_url = "http://www.kuaidi100.com/poll"
	# # api_url = "http://{}/tools/api/express/test_kuaidi_poll/?code=1".format(settings.DOMAIN)

	# 参数格式
	schema = "json"

	# 回调地址
	callback_url = "http://{}/tools/api/express/kdniao/callback/"


	"""
	快递单当前签收状态

	1：已取件2：在途中 3：签收
	"""

	STATE_EXPRESS_GOT = 1
	STATE_ON_THE_WAY = 2
	STATE_SIGNED = 3
	
