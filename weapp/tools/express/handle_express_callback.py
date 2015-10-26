# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from datetime import datetime
from express_config import *
from express_request_params import *
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
import urllib2
import json
from django.conf import settings
from models import *
from mall import models as mall_models

import mall.module_api as mall_api


class ExpressCallbackHandle(object):
	'''
	快递100 推送请求处理函数
		通信协议:HTTP
		请求类型:POST
		字符集:utf-8

	url:
		http://快递100?
			param={
				"status":"polling",   	/*监控状态:
												polling:监控中，shutdown:结束，abort:中止，updateall：重新推送 */
				"lastResult":{        	/*最新查询结果，全量，倒序（即时间最新的在最前）*/
					"state":"0",    	/*快递单当前签收状态，包括0在途中、1已揽收、2疑难、3已签收、4退签、5同城派送中、6退回、7转单*/
					"ischeck":"0",      /*是否签收标记，明细状态请参考state字段*/
					"com":"yuantong",   /*快递公司编码,一律用小写字母*/
					"nu":"V030344422",  /*单号*/
					"data":[
						{
							"context":"上海分拨中心/装件入车扫描 ", /*内容*/
							"time":"2012-08-28 16:33:19",           /*时间，原始格式*/
							"ftime":"2012-08-28 16:33:19"        	/*格式化后时间*/
						},{
							"context":"上海分拨中心/下车扫描 ",    	/*内容*/
							"time":"2012-08-27 23:22:42",          	/*时间，原始格式*/
							"ftime":"2012-08-27 23:22:42"	      	/*格式化后时间*/
						}
					]
				}
			}

	return:
		{
			"result":"true",
			"returnCode":"200",
			"message":"成功"
		}

	测试接口:
		http://dev.weapp.com/tools/api/express/test_analog_push_data/?order_id=2

		http://dev.weapp.com/tools/api/express/kuaidi/callback/?callbackid=2&version=2.0
	'''

	def __init__(self, request, order, express):
		self.callback_post_request = request
		self.order = order
		self.express = express

		self.express_config = ExpressConfig
		self.express_params = ExpressRequestParams

		if self.order:
			self.order_id = self.order.id
		else:
			self.order_id = -1


	def success_json(self):
		return {
			"result": True,
			"returnCode": 200,
			"message": "成功"
		}

	def error_json(self, message="失败"):
		return {
			"result": False,
			"returnCode": 500,
			"message": message
		}

	def analytical_json(self):
		param_str = self.callback_post_request.POST.get('param', '{}')
		return json.loads(param_str)


	def save_express_details(self, json):
		# 删除之前的
		if self.order_id > 0:
			ExpressDetail.objects.filter(order_id = self.order_id).delete()
		else:
			ExpressDetail.objects.filter(express_id = self.express.id).delete()

		try:			
			express_details = json.get(self.express_params.LAST_RESULT, {}).get('data', {})
			display_index = 1
			express_id = self.express.id if self.express else -1
			for detail in express_details:
				ExpressDetail.objects.create(
					order_id = self.order_id,
					express_id = express_id,
					context = detail['context'],
					time = detail['time'],
					ftime = detail['ftime'],
					status = detail.get('status',''),
					display_index = display_index
				)
				display_index = display_index + 1

			watchdog_info(u'保存快递100的 推送数据成功，url:{}, json:{}'.format(
					self.callback_post_request.get_full_path(),
					json
				), self.express_config.watchdog_type
			)
			self.express.receive_count = self.express.receive_count + 1
			self.express.save()

			return True
		except:
			watchdog_error(u'保存快递100的 推送数据失败，url:{}, json:{}, 原因:{}'.format(
					self.callback_post_request.get_full_path(),
					json,
					unicode_full_stack()
				), self.express_config.watchdog_type
			)
			return False

	def update_order_status(self, json, orders):
		status = json.get(self.express_params.LAST_RESULT, {}).get(self.express_params.STATE)
		# 状态为 3已签收，并且order的状态为 已发货
		# 将状态改为 已完成
		for order in orders:
			try:
				if int(status) == self.express_config.STATE_SIGNED and order.status == 4:
					mall_api.update_order_status(user=None, action='finish', order=order)
					# order.status = 5
					# order.save()
			except:
				watchdog_error(u'修改订单状态失败，该订单已签收，order_id:{}, 原因:{}'.format(
						order.id,
						unicode_full_stack()
					), self.express_config.watchdog_type
				)

		return True

	def get_orders(self):
		orders = mall_models.Order.objects.filter(
			express_company_name=self.express.express_company_name, 
			express_number=self.express.express_number,
			status__in=[3, 4]
		)
		return orders

	def is_abort_by_express(self, json):
		state = json.get(self.express_params.STATUS, '')
		message = json.get(self.express_params.MESSAGE, '')
		if state == self.express_config.STATUS_ABORT and u'3天' in message:
			return True
		else:
			return False

	def save_abort_express_details(self, data):
		data_string = json.dumps(data)
		self.express.abort_receive_at = datetime.now()
		self.express.abort_receive_message = data_string
		self.express.save()

	'''
	1、解析json数据
	2、保存数据
	3、修改状态（如果是‘已发货’状态，改为‘已完成’状态，其它状态不处理）
	4、返回数据
	'''
	def handle(self):
		# if self.order.status not in [3, 4]:
		# 	return self.error_json('该订单的状态不是已发货或待发货！')

		# 解析参数
		json = self.analytical_json()

		# 是否status: abort 而且message中包含“3天”关键字
		is_abort = self.is_abort_by_express(json)
		if is_abort:
			self.save_abort_express_details(json)
			return self.error_json(u'该订单已关闭，需要重新推送！')

		# 保存快递信息
		is_success = self.save_express_details(json)
		if is_success is False:
			return self.error_json('保存快递信息失败！')

		# 获取 改 快递公司 与 快递单号 对应的order
		orders = self.get_orders()
		if orders.count() == 0:
			return self.error_json('该订单的状态不是已发货或待发货！')

		# 修改订单的状态
		is_update_success = self.update_order_status(json, orders)
		if is_update_success:
			return self.success_json()
		else:
			return self.error_json('修改订单状态失败！')
