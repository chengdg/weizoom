# -*- coding: utf-8 -*-
from core import api_resource
from wapi.decorators import param_required
from wapi.decorators import auth_required
from mall import module_api as mall_api
from mall import models
from datetime import datetime
from tools.regional import views as regional_util
from tools.express import util as tools_express_util

class OrderShip(api_resource.ApiResource):

	app = 'open'
	resource = 'order_ship'

	@auth_required
	@param_required(['order_id','logistics_name','logistics_number'])
	def post(args):
		"""

		"""
		order_id = args['order_id']
		logistics_name = args['logistics_name']
		logistics_number = args['logistics_number']
		express_data = tools_express_util.get_express_company_json()
		is_100 = False
		for express in express_data:
			if logistics_name == express['value']:
				is_100 = True
		is_update_express = False
		order = models.Order.objects.filter(order_id=order_id)
		if len(order):
			order = order[0]
			err_msg = None
			is_success = None
			# 已取消的订单不能发货
			if order.status != models.ORDER_STATUS_PAYED_NOT_SHIP:
				is_success = False
				err_msg = u'该订单不处于待发货状态'
			else:
				# 订单发货，和批量发货所用的方法相同
				is_success = mall_api.ship_order(order.id, logistics_name, logistics_number,
											is_update_express=is_update_express, is_100=is_100)
			result = {'is_success':is_success,
					  'err_msg':err_msg}
		else:
			result = {'is_success':False,
					  'err_msg':"订单不存在"}
		return result

