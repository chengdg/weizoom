# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from express_config import *
from express_request_params import *
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
import urllib2
import json

# 返回结果：
# Message	消息体
# Data	    数据集合
# Time	    每条数据的时间
# Context	每条数据的状态
# state	    快递单当前的状态
#           0：在途中,
#           1：已发货，
#           2：疑难件，
#           3：已签收 ，
#           4：已退货。
# status	查询的结果状态。
#           0：运单暂无结果，
#           1：查询成功，
#           2：接口出现异常，
#           408：验证码出错（仅适用于APICode url，可忽略)
class ExpressOrderQuery(object):
	'''
	url:
		http://api.kuaidi100.com/api?
			id=[]&
			com=[]&
			nu=[]&
			valicode=[]&
			show=[0|1|2|3]&
			muti=[0|1]&
			order=[desc|asc]
	'''
	EXPRESS_ORDER_QUERY_URL_TMPL ="http://api.kuaidi100.com/api?id={}&com={}&nu={}&show=0&muti=1&order={}"
#	EXPRESS_ORDER_QUERY_URL_TMPL ="http://dev.weapp.com:8000/tools/api/express/test/?id={}&com={}&nu={}&show=0&muti=1"

	def __init__(self, request, express_company, express_number, order_by):
		self.authorize_post_request = request
		self.express_company = express_company
		self.express_number = express_number
		self.order_by = order_by

		self.express_config = ExpressConfig
		self.express_params = ExpressRequestParams

	def _verify_response(self):
		"""用登陆返回的code，获取信息,发送请求"""
		verity_url = self.EXPRESS_ORDER_QUERY_URL_TMPL.format(
			self.express_config.app_key,
			self.express_company,
			self.express_number,
			self.order_by
		)

		verified_result = ''
		try:
			verify_response = urllib2.urlopen(verity_url)
			verified_result = verify_response.read().strip()
			watchdog_info(u'从快递100获取订单信息，url:{}'.format(verity_url), 'EXPRESS')
		except:
			notify_message = u'从快递100获取订单信息失败，url:{},原因:{}'.format(verity_url, unicode_full_stack())
			watchdog_error(notify_message)

		return verified_result


	def _is_verified_authorize(self):
		result = self._verify_response()
		result = self._decode(result.strip())
		data = self._parse_result(result)
		return data

	def _decode(self, result):
		return result.decode('utf-8')

	def _parse_result(self, result):
		data = dict()
		try:
			data = json.loads(result)
#			status = int(data['status'])
#			if status >= 0 and status < 3:
#				data['message'] = self.express_config.STATUSES[status]
#			else:
#				data['message'] = self.express_config.STATUSES[3]

			watchdog_info(u'从快递100获取订单信息，data{}'.format(result), 'EXPRESS')
		except:
			notify_message = u'解析快递100获取订单信息失败，url:{},原因:{}'.format(result, unicode_full_stack())
			watchdog_error(notify_message)
		return data


	def get_express_order_data(self):
		data = self._is_verified_authorize()
		if data == {}:
			return None
		else:
			return data
