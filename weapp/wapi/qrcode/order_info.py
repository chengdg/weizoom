# -*- coding: utf-8 -*-
import json
import time

from core import api_resource, paginator
from wapi.decorators import param_required
from mall.models import Order, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog


class QrcodeOrderInfo(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'order_info'

	@param_required(['order_ids'])
	def get(args):
		"""
		获取订单
		"""
		order_ids = json.loads(args.get('order_ids'))
		is_first_order = int(args.get('is_first_order', 0))

		filter_args = {
			"id__in": order_ids
		}

		if is_first_order:
			filter_args["is_first_order"] = is_first_order
		orders = Order.objects.filter(**filter_args).order_by('-created_at')


		order_id2created_at = {}
		curr_orders = []
		for order in orders:
			sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
			order_id2created_at[order.id] = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
			curr_orders.append({
				"order_id": order.id,
				"order_number": order.order_id,
				"final_price": order.final_price,
				"status_text": STATUS2TEXT[order.status],
				"sale_price": sale_price,
				"created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				"is_first_order": order.is_first_order
			})

		return {
			'order_id2created_at': order_id2created_at,
			'orders': curr_orders
		}
