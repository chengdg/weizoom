# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from mall.models import Order, ORDER_STATUS_CANCEL, ORDER_STATUS_GROUP_REFUNDING, ORDER_STATUS_GROUP_REFUNDED, \
	ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED, ORDER_STATUS_NOT
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *

class ShopOrders(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'shop_orders'

	@param_required(['channel_qrcode_ids'])
	def get(args):
		"""
		帐号管理
		"""
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'))
		channel_qrcode = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids).order_by('created_at').first()
		created_at = channel_qrcode.created_at.strftime("%Y-%m-%d %H:%M:%S")

		total_channel_members = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=channel_qrcode_ids).order_by('-created_at')
		channel_qrcode_id2member_id = {}
		total_member_ids = []
		for m in total_channel_members:
			total_member_ids.append(m.member_id)
			if not channel_qrcode_id2member_id.has_key(m.channel_qrcode_id):
				channel_qrcode_id2member_id[m.channel_qrcode_id] = [m.member_id]
			else:
				channel_qrcode_id2member_id[m.channel_qrcode_id].append(m.member_id)

		webapp_user_id2member_id = {webappuser.id: webappuser.member_id for webappuser in WebAppUser.objects.filter(member_id__in=total_member_ids)}

		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		is_export = args.get('is_export', None)
		if is_export:
			filter_data_args = {
				"webapp_user_id__in": webapp_user_id2member_id.keys(),
				"origin_order_id__lte": 0,
				"created_at__gte": created_at
			}
		else:
			filter_data_args = {
				"webapp_user_id__in": webapp_user_id2member_id.keys(),
				"origin_order_id__lte": 0,
				"created_at__gte": created_at,
			}
			if start_date and end_date:
				start_time = start_date + ' 00:00:00'
				end_time = end_date + ' 23:59:59'
				filter_data_args["created_at__gte"] = start_time
				filter_data_args["created_at__lte"] = end_time

		orders = Order.objects.filter(**filter_data_args)
		channel_qrcode_id2increase_order_count = {}
		channel_qrcode_id2first_order_count = {}
		channel_qrcode_id2final_price = {}
		channel_qrcode_id2order_sale_money = {}
		#下单时间
		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			for order in orders:
				webapp_user_id = order.webapp_user_id
				member_id = webapp_user_id2member_id.get(webapp_user_id)
				created_at = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
				if created_at >= start_time and created_at <= end_time:
					for channel_qrcode_id, member_ids in channel_qrcode_id2member_id.items():
						if member_id in member_ids:
							if order.status not in [ORDER_STATUS_CANCEL, ORDER_STATUS_GROUP_REFUNDING, ORDER_STATUS_GROUP_REFUNDED, ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED]:
								sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
								final_price = order.final_price
								if not channel_qrcode_id2increase_order_count.has_key(channel_qrcode_id):
									channel_qrcode_id2increase_order_count[channel_qrcode_id] = 1
								else:
									channel_qrcode_id2increase_order_count[channel_qrcode_id] += 1

								if not channel_qrcode_id2final_price.has_key(channel_qrcode_id):
									channel_qrcode_id2final_price[channel_qrcode_id] = final_price
								else:
									channel_qrcode_id2final_price[channel_qrcode_id] += final_price

								if not channel_qrcode_id2order_sale_money.has_key(channel_qrcode_id):
									channel_qrcode_id2order_sale_money[channel_qrcode_id] = sale_price
								else:
									channel_qrcode_id2order_sale_money[channel_qrcode_id] += sale_price
							if order.is_first_order and order.status != ORDER_STATUS_NOT:
								if not channel_qrcode_id2first_order_count.has_key(channel_qrcode_id):
									channel_qrcode_id2first_order_count[channel_qrcode_id] = 1
								else:
									channel_qrcode_id2first_order_count[channel_qrcode_id] += 1

		if is_export:
			channel_qrcode_id2order_count = {}
			channel_qrcode_id2total_order_sale_money = {}
			channel_qrcode_id2total_final_price = {}
			channel_qrcode_id2total_first_order_count = {}
			for order in orders:
				webapp_user_id = order.webapp_user_id
				member_id = webapp_user_id2member_id.get(webapp_user_id)
				for channel_qrcode_id, member_ids in channel_qrcode_id2member_id.items():
					if member_id in member_ids:
						if not channel_qrcode_id2order_count.has_key(channel_qrcode_id):
							channel_qrcode_id2order_count[channel_qrcode_id] = 1
						else:
							channel_qrcode_id2order_count[channel_qrcode_id] += 1
						if order.status not in [ORDER_STATUS_CANCEL,ORDER_STATUS_GROUP_REFUNDING,ORDER_STATUS_GROUP_REFUNDED,ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED]:
							sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
							final_price = order.final_price
							if not channel_qrcode_id2total_order_sale_money.has_key(channel_qrcode_id):
								channel_qrcode_id2total_order_sale_money[channel_qrcode_id] = sale_price
							else:
								channel_qrcode_id2total_order_sale_money[channel_qrcode_id] += sale_price

							if not channel_qrcode_id2total_final_price.has_key(channel_qrcode_id):
								channel_qrcode_id2total_final_price[channel_qrcode_id] = final_price
							else:
								channel_qrcode_id2total_final_price[channel_qrcode_id] += final_price

						if order.is_first_order and order.status != ORDER_STATUS_NOT:
							if not channel_qrcode_id2total_first_order_count.has_key(channel_qrcode_id):
								channel_qrcode_id2total_first_order_count[channel_qrcode_id] = 1
							else:
								channel_qrcode_id2total_first_order_count[channel_qrcode_id] += 1

			return {
				"channel_qrcode_id2increase_order_count": channel_qrcode_id2increase_order_count,
				"channel_qrcode_id2first_order_count": channel_qrcode_id2first_order_count,
				"channel_qrcode_id2order_count": channel_qrcode_id2order_count,
				"channel_qrcode_id2total_first_order_count": channel_qrcode_id2total_first_order_count,
				"channel_qrcode_id2total_order_sale_money": channel_qrcode_id2total_order_sale_money,
				"channel_qrcode_id2total_final_price": channel_qrcode_id2total_final_price,
				"channel_qrcode_id2order_sale_money": channel_qrcode_id2order_sale_money,
				"channel_qrcode_id2final_price": channel_qrcode_id2final_price
			}
		else:
			return {
				"channel_qrcode_id2increase_order_count": channel_qrcode_id2increase_order_count,
				"channel_qrcode_id2first_order_count": channel_qrcode_id2first_order_count,
				"channel_qrcode_id2order_sale_money": channel_qrcode_id2order_sale_money,
				"channel_qrcode_id2final_price": channel_qrcode_id2final_price
			}
