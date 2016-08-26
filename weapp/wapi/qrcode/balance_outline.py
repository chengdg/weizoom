# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_NOT,ORDER_STATUS_CANCEL,ORDER_STATUS_GROUP_REFUNDING,ORDER_STATUS_GROUP_REFUNDED,ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED, OrderOperationLog,STATUS2TEXT
import time

class QrcodeBalanceOutline(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'balance_outline'

	@param_required(['channel_qrcode_id'])
	def get(args):
		"""
		获取会员
		"""
		start = time.time()
		channel_qrcode_id = int(args.get('channel_qrcode_id'))
		order_numbers = json.loads(args.get('order_numbers', ''))

		channel_qrcode = ChannelQrcodeSettings.objects.get(id=channel_qrcode_id)
		created_at = channel_qrcode.created_at.strftime("%Y-%m-%d %H:%M:%S")

		total_channel_members = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=channel_qrcode_id).order_by('-created_at')
		total_member_ids = [tcm.member_id for tcm in total_channel_members]
		webapp_user_ids = [webappuser.id for webappuser in WebAppUser.objects.filter(member_id__in=total_member_ids)]

		filter_data_args = {
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0,
			"created_at__gte": created_at
		}


		# 获取在某段时间内的已完成和退款完成的订单时间
		orderoperationlogs = OrderOperationLog.objects.filter(
			action__in=[u"完成", u"退款完成"],
			created_at__gte=created_at
		).exclude(order_id__contains='^')

		order_number2finished_at = {opl.order_id: opl.created_at for opl in orderoperationlogs}
		refund_order_number = []
		for opl in orderoperationlogs:
			if opl.action == u'退款完成':
				refund_order_number.append(opl.order_id)

		if order_numbers:
			curr_order_numbers = set(order_numbers) - set(refund_order_number)
		else:
			curr_order_numbers = refund_order_number

		orders = Order.objects.filter(**filter_data_args).exclude(order_id__in=curr_order_numbers)

		first_orders = []
		all_order = []
		for order in orders:
			sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
			final_price = order.final_price + order.weizoom_card_money
			#除已取消的订单
			if order.status not in [ORDER_STATUS_CANCEL]:
				all_order.append({
					'order_id': order.id,
					'finished_at': order_number2finished_at.get(order.order_id,order.created_at).strftime("%Y-%m-%d %H:%M:%S"),
					'status_text': STATUS2TEXT[order.status],
					'sale_price': sale_price,
					'final_price': final_price,
					'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
				})

			if order.is_first_order and order.status != ORDER_STATUS_NOT:
				first_orders.append({
					'order_id': order.id,
					'finished_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
					'status_text': STATUS2TEXT[order.status],
					'sale_price': sale_price,
					'final_price': final_price,
					'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
				})

		member_outline_info = {
			"first_orders": first_orders,
			"all_order": all_order,
		}
		end = time.time()
		print end - start, "bbbbbbbbbbb"

		return {
			'items': member_outline_info
		}
