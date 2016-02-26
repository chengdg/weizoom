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

	def __init__(self, request):
		self.callback_post_request = request
		# self.order = order
		self.express = ''
		self.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.express_config = KdniaoExpressConfig
		self.express_params = ExpressRequestParams
		self.order_id = -1
		# if self.order:
		# 	self.order_id = self.order.id
		# else:
		# 	self.order_id = -1


	def success_json(self):
		return {
			"EBusinessID": self.express_config.EBusiness_id,
			"UpdateTime": self.updatetime,
			"Success": True
		}

	def error_json(self):
		return {
			"EBusinessID": self.express_config.EBusiness_id,
			"UpdateTime": self.updatetime,
			"Success": False
		}

	def analytical_json(self):
		# param_str = self.callback_post_request.POST.get('Datas', '{}')
		# print self.callback_post_request.POST
		# print dir(self.callback_post_request.POST)
		print '111111111111111'
		#print self.callback_post_request
		print ">>>>>>>>>>>"
		print "self.callback_post_request.POST>>>>>>>>>",self.callback_post_request.POST
		print ">>>>>>>>>>>"
		param_json = json.loads(self.callback_post_request.POST.get("RequestData",""))
		print "RequestData>>>>>>>>>",param_json
		datas = param_json.get("Data",[])
		#print "datas",datas
		# for key,value in self.callback_post_request.POST.items():
		# 	print key,'>>>>>>>>>>>>>>>>>>',value,'\n'
		# 	print '2222222222222'
		# print type(self.callback_post_request.POST), "Fself.callback_post_request.POST"
		# print type(param_str), "FFF"
		# print "123>>>>>>",param_str
		# return param_str
		return datas


	def save_express_details(self, data):

		# 删除之前的
		callback_id = int(data.get('CallBack', -1)) #ExpressHasOrderPushStatus的id
		express_code = int(data.get('LogisticCode', -1)) #快递号
		print "callback_id,express_code>>>>>>>>>",callback_id,express_code
		if not callback_id:
			watchdog_error(u'保存快递鸟的推送数据失败,没有返回订阅id,callback_id:{}'.format(
				callback_id), self.express_config.watchdog_type)
			return False
		# order = None
		# order = mall_api.get_order_by_id(callback_id)
		# print "order", order
		self.express = express_models.ExpressHasOrderPushStatus.get(callback_id)

		if self.order_id > 0:
			ExpressDetail.objects.filter(order_id = self.order_id).delete()
		else:
			ExpressDetail.objects.filter(express_id = self.express.id).delete()
		try:			
			express_details = data.get('Traces', {})
			print ">>>>>>>>"
			print "express_details",len(express_details),express_details
			print ">>>>>>>>"
			display_index = 1
			express_id = self.express.id if self.express else -1 #订单的推送状态的id
			print u"订单的推送状态的id",type(express_id),express_id
			for detail in express_details:
				print "ExpressDetail",detail
				express_detail = ExpressDetail.objects.create(
					order_id = self.order_id,
					express_id = express_id,
					context = detail['AcceptStation'],
					time = detail['AcceptTime'],
					ftime = detail['AcceptTime'],
					#status = detail.get('status',''), #快递鸟没有该数据
					display_index = display_index
				)
				print "create ExpressDetail ok!!!",express_detail
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
		print "update_order_status",status

		#status 1：已取件2：在途中 3：签收
		for order in orders:
			try:
				if int(status) == self.express_config.STATE_SIGNED and order.status == 4:
					mall_api.update_order_status(user=None, action=u'finish-系统', order=order)
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
		datas = self.analytical_json()

		#datas = json.loads(datas)
		if not datas:
			print u"没有接收到数据"
			return
		print "datas",type(datas)
		print datas
		print 'len(datas)',len(datas)

		for data in datas:
			print ">>>>>>>>a"
			print "data",type(data)
#			print data
			print data["EBusinessID"],type(data["EBusinessID"]),self.express_config.EBusiness_id,type(self.express_config.EBusiness_id)
			if data["EBusinessID"] == self.express_config.EBusiness_id:
				print "unicode =====   str"

			if str(data["EBusinessID"]) == self.express_config.EBusiness_id:
				print ">>>>>>>>b"

				# 保存快递信息
				is_success = self.save_express_details(data)
				

				# 获取 该 快递公司 与 快递单号 对应的order
				orders = self.get_orders()
				if orders.count() == 0:
					print '该订单的状态不是已发货或待发货！快递单号',self.express.express_number

				# 修改订单的状态
				is_update_success = self.update_order_status(data, orders)
				if is_update_success:
					print self.success_json()
				else:
					print u'修改订单状态失败！'
