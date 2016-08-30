# -*- coding: utf-8 -*-
import json
import time

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog


class QrcodeOrder(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'orders'

	@param_required(['channel_qrcode_id'])
	def get(args):
		"""
		获取订单
		"""
		order_ids = json.loads(args.get('order_ids'))

		orders = Order.objects.filter(id__in=order_ids)

		order_id2created_at = {}
		for order in orders:
			order_id2created_at[order.id] = order.created_at.strftime('%Y-%m-%d %H:%M:%S'),

		return {
			'items': order_id2created_at
		}
