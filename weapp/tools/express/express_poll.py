# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from express_config import *
from express_request_params import *
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
import urllib, urllib2
import json
from django.conf import settings
from models import *
import datetime


class ExpressPoll(object):
	'''
	快递100 订阅请求
		通信协议:HTTP
		请求类型:POST
		字符集:utf-8

	url:
		http://www.kuaidi100.com/poll?
			schema=json/xml&
			param={
				"company":"yuantong",           //订阅的快递公司的编码，一律用小写字母，见章五《快递公司编码》
				"number":"12345678",           	//订阅的快递单号，单号的最大长度是32个字符
				"from":"广东深圳",              //出发地城市(可选)
				"to":"北京朝阳",                //目的地城市，到达目的地后会加大监控频率
				"key":"*********",              //授权码，签订合同后发放
				"parameters":{
					"callbackurl":" http://www.您的域名.com/kuaidi?callbackid=...", //回调地址
					"salt":"any string",      //签名用随机字符串（可选）
					"resultv2":"1"            //添加此字段表示开通行政区域解析功能（仅对开通签收状态服务用户有效）
				}
			}

	return:
		{
			"result":"true",
			"returnCode":"200",
			"message":"提交成功"
		}

	result: "true"表示成功，false表示失败
	returnCode:
		200: 提交成功
		701: 拒绝订阅的快递公司
		700: 订阅方的订阅数据存在错误（如不支持的快递公司、单号为空、单号超长等）
		600: 您不是合法的订阅者（即授权Key出错）
		500: 服务器错误
		501:重复订阅

	测试接口:	
		http://dev.weapp.com/tools/api/express/test_kuaidi_poll/?code=1

	'''

	def __init__(self, order):
		self.express_company_name = order.express_company_name if order.express_company_name else ''
		self.express_number = order.express_number if order.express_number else ''
		self.order = order
		self.order_id = order.id
		self.area = order.get_str_area
		self.express = None
		self.webapp_id = order.webapp_id

		self.express_config = ExpressConfig()
		self.express_params = ExpressRequestParams

	def _get_api(self):
		if self.express:
			return self.express_config.callback_url.format(settings.DOMAIN, self.express.id)

		return self.express_config.callback_url.format(settings.DOMAIN, '-99')
		# return self.express_config.callback_url.format('docker.test.gaoliqi.com', self.order_id)

	def _poll_response(self):
		"""
		发送快递100 订阅请求，返回成功与否信息
		"""
		# post中的param的json
		param_json_data = {		
			self.express_params.COMPANY: self.express_company_name,
			self.express_params.NUMBER: self.express_number,
			self.express_params.TO: self.area,
			self.express_params.KEY: self.express_config.app_key, 
			self.express_params.PARAMETERS: {
				self.express_params.CALLBACK_URL: self._get_api()
			}
		}
		# 将PARAMETERS的json转换为字符串
		param_str = json.dumps(param_json_data)

		json_data = {
			self.express_params.SCHEMA: self.express_config.schema,
			self.express_params.PARAM: param_str
		}

		# print param_str
		verified_result = ''
		try:
			param_data = urllib.urlencode(json_data)
			# print '-------------------------------------------'
			# print param_data

			if settings.IS_UNDER_BDD:
				from test.bdd_util import WeappClient
				bdd_client = WeappClient()
				response = bdd_client.post('/tools/api/express/test_kuaidi_poll/?code=1', param_json_data)
				verified_result = response.content

			else:
				request = urllib2.Request(self.express_config.get_api_url(), param_data)
				response = urllib2.urlopen(request)
				verified_result = response.read()

			watchdog_info(u"发送快递100 订阅请求 url: {},/n param_data: {}, /n response: {}".format(
				self.express_config.get_api_url(), 
				param_str,
				verified_result.decode('utf-8')), type=self.express_config.watchdog_type)
		except:
			watchdog_error(u'发送快递100 订阅请求 失败，url:{},data:{},原因:{}'.format(self.express_config.get_api_url(),
				param_str,
				unicode_full_stack()), type=self.express_config.watchdog_type)

		return verified_result


	def _send_poll_requset(self):
		result = self._poll_response()
		result = self._decode(result.strip())
		data = self._parse_result(result)
		return data

	def _decode(self, result):
		return result.decode('utf-8')

	def _parse_result(self, result):
		data = dict()
		
		if result is None or len(result) == 0:
			return data

		try:
			data = json.loads(result)
			watchdog_info(u'从快递100获取订单信息，data{}'.format(result), self.express_config.watchdog_type)
		except:
			notify_message = u'解析快递100获取订单信息失败，url:{}, data:{}, 原因:{}'.format(result, data, unicode_full_stack())
			watchdog_error(notify_message, self.express_config.watchdog_type)
		return data


	def _is_poll_by_order(self):
		try:
			pushs = ExpressHasOrderPushStatus.objects.filter(
					# order_id = self.order_id,
					express_company_name = self.order.express_company_name,
					express_number = self.order.express_number
					)
			if pushs.count() > 0:
				push = pushs[0]

				# 不需要重新发送订阅请求的状态
				if push.status in EXPRESS_NOT_PULL_STATUSES:
					return True

				# 超过4次发送就不再发送次快递
				if push.send_count >= 4:
					return True
					
				# 关闭，重发订阅
				if push.abort_receive_message and len(push.abort_receive_message) > 0:
					import json
					json = json.loads(push.abort_receive_message)
					if json.get(self.express_params.STATUS, '') == self.express_config.STATUS_ABORT:
						return False

				# 第一次发送订阅
				if push.status == EXPRESS_PULL_SUCCESS_STATUS and push.send_count > 0:
					return True

			return False
		except:
			watchdog_error(u'快递100tool_express_has_order_push_status表异常，获取订单信息，express_company_name:{}，express_number:{}'.format(self.order.express_company_name, self.order.express_number), self.express_config.watchdog_type)
			return False


	def _save_poll_order_id(self):
		# ExpressDetail.objects.filter(order_id=self.order_id).delete()
		pushs = ExpressHasOrderPushStatus.objects.filter(
			express_company_name = self.order.express_company_name,
			express_number = self.order.express_number
		)

		if pushs.count() > 0:
			return pushs[0]

		else:
			express = ExpressHasOrderPushStatus.objects.create(
				order_id = -1,
				status = EXPRESS_PULL_NOT_STATUS,
				express_company_name = self.order.express_company_name,
				express_number = self.order.express_number,
				service_type = EXPRESS_100,
				webapp_id = self.webapp_id
			)
			return express


	def get_express_poll(self):
		# 如果是空不处理
		if self.express_company_name is '' or self.express_number is '':
			return False

		# 是否已经订阅过该订单，并且成功
		status = self._is_poll_by_order()
		if status:
			return True

		# 保存快递信息	
		self.express = self._save_poll_order_id()

		#暂无物流信息没有更新状态时，商家正在通知快递公司揽件
		if ExpressDetail.objects.filter(express_id=self.express.id).count() == 0:
			context = u'商家正在通知快递公司揽件'
			dtime = datetime.datetime.now()
			ExpressDetail.objects.create(
					express_id = self.express.id,
					context = context,
					time = dtime,
					ftime = dtime,
					status = -1,
					display_index = 1
				)

		# 发送订阅请求
		data = self._send_poll_requset()
		result = True if data.get('result') == "true" or data.get('result') is True else False

		if result:
			# 修改快递信息状态
			self.express.status = data.get('returnCode')
			self.express.send_count = self.express.send_count + 1
			self.express.abort_receive_message = ""
			self.express.save()
			return True
		else:
			if data and data.get('returnCode'):
				self.express.status = data.get('returnCode')
				self.express.save()
			return False
