# -*- coding: utf-8 -*-

from tools.express.express_request_params import *
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
import urllib, urllib2
import json
from django.conf import settings
from hashlib import md5
import base64
from tools.express.models import *
from tools.express.kdniao_express_config import *
import requests

express2kdniaocode = {'quanfengkuaidi': 'QFKD', 'shentong': 'STO', 'zhaijisong': 'ZJS', 'rufengda': 'RFD', 
	'debangwuliu': 'DBL', 'shunfeng': 'SF', 'yunda': 'YD', 'bpost': 'BEL', 'tiantian': 'HHTT', 
	'suer': 'SURE', 'ems': 'EMS', 'zhongtong': 'ZTO', 'kuaijiesudi': 'FAST', 'yuantong': 'YTO', 
	'huitongkuaidi': 'HTKY', 'guotongkuaidi': 'GTO', 'youzhengguonei': 'YZPY'}

class KdniaoExpressEorder(object):
	'''
	快递鸟 电子面单
		通信协议:HTTP
		请求类型:POST
		字符集:utf-8
	参数说明：

		RequestData	String	R	请求内容，JSON或XML格式,须和DataType一致
		EBusinessID	String	R	电商ID
		RequestType	String	R	请求指令类型：1005
		DataSign	String	R	数据内容签名
		DataType	String	O	请求、返回数据类型：1-xml,2-json；默认为xml格式
		PayType		Int		R	邮费支付方式:1-现付，2-到付，3-月结，4-第三方支付
		O代表必须，R代表非必须
	

	
	data格式：
	data：post_data = {
					"OrderCode": "PM201604062341339",
					"ShipperCode": "SF",
					"PayType": 1,
					"ExpType": 1,
					"Sender": {
						"Name" : "李先生",
						"Mobile" : "18888888888",
						"ProvinceName" : "李先生",
						"CityName" : "深圳市",
						"ExpAreaName" : "福田区",
						"Address" : "赛格广场5401AB"
					},
					"Receiver":{
						"Name" : "李先生",
						"Mobile" : "18888888888",
						"ProvinceName" : "李先生",
						"CityName" : "深圳市",
						"ExpAreaName" : "福田区",
						"Address" : "赛格广场5401AB"
					},
					"Commodity": [{
					  "GoodsName": "鞋子",
					  "Goodsquantity": 2,
					  "GoodsCode": '35678'
					}
					],
					"IsReturnPrintTemplate": 1
				}

	return:
		失败：
		{
			"EBusinessID": "1237100",
			"ResultCode": "105",
			"Reason": "订单号已存在，请勿重复操作"，
			"UniquerRequestNumber":"5e66486b-8fbc-4131-b875-9b13d2ad1354"
		}
		成功：
		{
		  "EBusinessID": "1237100",
		  "Order": {
			"OrderCode": "012657700387",
			"ShipperCode": "HTKY",
			"LogisticCode": "50002498503427",
			"MarkDestination": "京-朝阳(京-1)",
			"OriginCode": "200000",
			"OriginName": "上海分拨中心",
			"PackageCode": "北京"
		  },
		  "PrintTemplate":"此处省略打印模板HTML内容",
		  "EstimatedDeliveryTime":"2016-03-06",
		  "Callback":"调用时传入的Callback",
		  "Success": true,
		  "ResultCode": "100",
		  "Reason": "成功"
		}

	result: "true"表示成功，false表示失败
	'''
	
	def __init__(self, orderCode, express_company_name, sender, receiver, commodity, order_id):
		"""
		orderCode:订单号
		sender：发件人信息，dict
		receiver：收件人信息，dict
		commodity：商品信息，json
		"""
		self.orderCode = orderCode
		self.express_company_name = express2kdniaocode[express_company_name]
		self.sender = sender
		self.receiver = receiver
		self.commodity = commodity
		self.order_id = order_id #watch_dog中记录使用
		self.Business_id = KdniaoExpressConfig.EBusiness_id
		self.api_key = KdniaoExpressConfig.api_key
		self.express_config = KdniaoExpressConfig()

		# 伪造
		# self.express_company_name = 'EMS'
		# self.express_number = 1060515954609

	def _build_post_data(self):
		return {
			"OrderCode": self.orderCode,
			"ShipperCode": self.express_company_name,
			"PayType": 1,
			"ExpType": 1,
			"Sender": self.sender,
			"Receiver": self.receiver,
			"Commodity": self.commodity,
			"IsReturnPrintTemplate": 1
		}
	def _encrypt(self, param_json_data):
		return base64.b64encode(md5(param_json_data + self.api_key).hexdigest())


	def _send_response(self):
		"""
		发送电子面单请求，返回成功与否信息
		"""
		# post中的param的json
		headers = {'content-type': 'application/json'}

		# param_json_data = {'Code': self.express_company_name_kdniao,'Item': [
		# 				   {'No': str(self.express_number),'Bk': str(self.express.id)},
		# 				   ]}
		param_json_data = self._build_post_data()
		a= json.dumps(param_json_data)
		DataSign= self._encrypt(json.dumps(param_json_data))
		params = json.dumps({
		"RequestData": json.dumps(param_json_data),
		"EBusinessID": self.Business_id ,
		"RequestType": "1007",
		"DataSign": DataSign,
		"DataType": "2"
		})


		verified_result = ''
		try:
			verified_result = requests.post(KdniaoExpressConfig.eorder_url, data=params, headers=headers)
			watchdog_info(u"发送快递鸟 电子面单请求 url: {},/n param_data: {}".format(
				KdniaoExpressConfig.eorder_url, 
				params), type=self.express_config.watchdog_type)
		except:
			watchdog_error(u'发送快递鸟 电子面单请求 失败，url:{},data:{},原因:{}'.format(KdniaoExpressConfig.eorder_url,
				params,
				unicode_full_stack()), type=self.express_config.watchdog_type)

		return verified_result

	def get_express_eorder(self):
		# 如果是空不处理
		if self.express_company_name is '' or self.order_id is '':
			return False, '', {}

		# 发送订阅请求
		data = self._send_response()
		data = data.json()
		result = True if data.get('Success') == "true" or data.get('Success') is True else False

		if result:
			# 修改快递信息状态,self.express.status = 200订阅成功，0未订阅
			print_template = data['PrintTemplate']
			express_order = data["Order"]
			print_template = ('<meta charset="utf-8">\n' + print_template).encode('utf-8')
			with open('order.html', 'w') as f:
				f.write(print_template)
			print "success"
			return True, print_template,express_order
		else:
			if data and data.get('Reason'):
				print "Reason:",data.get('Reason')

				watchdog_error(u'发送快递鸟 电子面单请求存在问题，url:{},订单id:{},原因:{}'.format(KdniaoExpressConfig.eorder_url,
					self.order_id,
					data.get('Reason')), type=self.express_config.watchdog_type)
			return False, '', {}


