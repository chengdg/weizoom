# -*- coding: utf-8 -*-

__author__ = 'justing'

from datetime import datetime
from kdniao_express_config import *
from express_request_params import *
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
import urllib2
import json
from django.conf import settings
from models import *
from mall import models as mall_models
from tools.express import models as express_models
import mall.module_api as mall_api


class KdniaoCallbackHandle(object):
	'''
	快递鸟 推送请求处理函数
		通信协议:HTTP
		请求类型:POST
		字符集:utf-8

	url:http://{}/tools/api/express/kdniao/callback/".format(settings.DOMAIN)
	参数：查看快递鸟接口技术文档
	
	测试接口:
		http://dev.weapp.com/tools/api/express/test_kdniao_push_data/
	'''

	def __init__(self, datas):
		self.datas = datas
		self.express = ''
		self.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.express_config = KdniaoExpressConfig
		self.express_params = ExpressRequestParams
		self.order_id = -1

	def save_express_details(self, data):
		# 删除之前的
		callback_id = int(data.get('CallBack', -1)) #CallBack作为ExpressHasOrderPushStatus的id
		express_code = int(data.get('LogisticCode', -1)) #快递号
		if not callback_id:
			watchdog_error(u'保存快递鸟的推送数据失败,没有返回订阅id,callback_id:{}'.format(
				callback_id), self.express_config.watchdog_type)
			return False

		self.express = express_models.ExpressHasOrderPushStatus.get(callback_id)

		if self.order_id > 0:
			ExpressDetail.objects.filter(order_id = self.order_id).delete()
		else:
			ExpressDetail.objects.filter(express_id = self.express.id).delete()
		try:			
			express_details = data.get('Traces', {})
			display_index = 1
			express_id = self.express.id if self.express else -1 #订单的推送状态的id

			for detail in express_details:
				express_detail = ExpressDetail.objects.create(
					order_id = self.order_id,
					express_id = express_id,
					context = detail['AcceptStation'],
					time = detail['AcceptTime'],
					ftime = detail['AcceptTime'],
					#status = detail.get('status',''), #快递鸟没有该数据
					display_index = display_index
				)
				display_index = display_index + 1

			watchdog_info(u'保存快递鸟的推送数据成功，express_id:{}, json:{}'.format(
					express_id,
					data
				), self.express_config.watchdog_type
			)
			self.express.receive_count = self.express.receive_count + 1
			self.express.save()

			return True
		except:
			watchdog_error(u'保存快递鸟的推送数据失败，express_id:{}, json:{}, 原因:{}'.format(
					express_id,
					data,
					unicode_full_stack()
				), self.express_config.watchdog_type
			)
			return False

	def update_order_status(self, data, orders):
		status = data.get("State")

		#status 1：已取件2：在途中 3：签收
		for order in orders:
			try:
				if int(status) == self.express_config.STATE_SIGNED and order.status == 4:
					mall_api.update_order_status(user=None, action=u'finish-系统', order=order)

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


	'''
	1、保存数据(解析数据在kdniao_callback函数中已完成)
	2、修改状态（如果是‘已发货’状态，改为‘已完成’状态，其它状态不处理）
	'''
	def handle(self):
		if not self.datas:
			watchdog_error( u"快递鸟:没有接收到数据", self.express_config.watchdog_type)
			return

		for data in self.datas:
			if str(data["EBusinessID"]) == self.express_config.EBusiness_id:

				# 保存快递信息
				is_success = self.save_express_details(data)
				
				# 获取 该 快递公司 与 快递单号 对应的order
				orders = self.get_orders()
				if orders.count() == 0:
					print u"express order status error该订单的状态不是已发货或待发货！快递单号",self.express.express_number
				# 修改订单的状态
				is_update_success = self.update_order_status(data, orders)
