# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_NOT,ORDER_STATUS_CANCEL,ORDER_STATUS_GROUP_REFUNDING,ORDER_STATUS_GROUP_REFUNDED,ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED
import time

class QrcodeOrderOutline(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'order_outline'

	@param_required([])
	def get(args):
		"""
		获取会员
		"""
		start = time.time()
		channel_qrcode_id = int(args.get('channel_qrcode_id', 0))
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids', "[]"))
		if channel_qrcode_ids:
			q_filter_data_args = {
				"channel_qrcode_id__in": channel_qrcode_ids
			}
		else:
			q_filter_data_args = {
				"channel_qrcode_id": channel_qrcode_id
			}


		total_channel_members = ChannelQrcodeHasMember.objects.filter(**q_filter_data_args).order_by('-created_at')
		total_member_ids = [tcm.member_id for tcm in total_channel_members]
		webappusers = WebAppUser.objects.filter(member_id__in=total_member_ids)
		webapp_user_ids = [webappuser.id for webappuser in webappusers]

		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		filter_data_args = {
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0
		}

		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			filter_data_args["created_at__gte"] = start_time
			filter_data_args["created_at__lte"] = end_time

		orders = Order.objects.filter(**filter_data_args)

		increase_orders = []
		first_orders = []
		sale_price = 0
		final_price = 0
		for order in orders:
			if order.status not in [ORDER_STATUS_CANCEL, ORDER_STATUS_GROUP_REFUNDING, ORDER_STATUS_GROUP_REFUNDED, ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED]:
				sale_price += order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
				final_price += order.final_price
				increase_orders.append(order)
			if order.is_first_order and order.status != ORDER_STATUS_NOT:
				first_orders.append(order)

		member_outline_info = {
			"increase_order_count": len(increase_orders),
			"first_order_count": len(first_orders),
			"order_sale_money": u'%.2f' % sale_price,
			"final_price": u'%.2f' % final_price
		}
		end = time.time()
		print end - start, "oooooooooooo"

		return {
			'items': member_outline_info
		}
