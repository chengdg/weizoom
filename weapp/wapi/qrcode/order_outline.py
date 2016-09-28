# -*- coding: utf-8 -*-
import json

from django.db.models import Q

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
		channel_qrcode_id2user_created_at = json.loads(args.get('channel_qrcode_id2user_created_at', "[]"))
		if channel_qrcode_ids:
			q_filter_data_args = {
				"channel_qrcode_id__in": channel_qrcode_ids
			}
		else:
			q_filter_data_args = {
				"channel_qrcode_id": channel_qrcode_id
			}

		total_channel_members = ChannelQrcodeHasMember.objects.filter(**q_filter_data_args).order_by(
			'-created_at')
		channel_qrcode_id2member_id = {}
		curr_qrcode_id2member_id = {}
		member_ids = []
		q_has_member_ids = []
		for member_log in total_channel_members:
			q_has_member_ids.append(member_log.member_id)
			member_ids.append(member_log.member_id)
			if not channel_qrcode_id2member_id.has_key(member_log.channel_qrcode_id):
				channel_qrcode_id2member_id[member_log.channel_qrcode_id] = [member_log.member_id]
			else:
				channel_qrcode_id2member_id[member_log.channel_qrcode_id].append(member_log.member_id)
			if not curr_qrcode_id2member_id.has_key(member_log.channel_qrcode_id):
				curr_qrcode_id2member_id[member_log.channel_qrcode_id] = [member_log.member_id]
			else:
				curr_qrcode_id2member_id[member_log.channel_qrcode_id].append(member_log.member_id)

		q_settings = ChannelQrcodeSettings.objects.filter(Q(id__in=channel_qrcode_ids) | Q(bing_member_id__in=member_ids))
		member_id2created_at = {}
		channel_qrcode_id2bing_member_id = {}
		for qs in q_settings:
			if qs.is_bing_member:
				member_ids.append(qs.bing_member_id)
				if not channel_qrcode_id2member_id.has_key(qs.id):
					channel_qrcode_id2member_id[qs.id] = [qs.bing_member_id]
				else:
					channel_qrcode_id2member_id[qs.id].append(qs.bing_member_id)
				member_id2created_at[qs.bing_member_id] = qs.created_at.strftime('%Y-%m-%d %H:%M:%S')
				channel_qrcode_id2bing_member_id[qs.id] = qs.bing_member_id

		webapp_user_id2member_id = {webappuser.id: webappuser.member_id for webappuser in WebAppUser.objects.filter(member_id__in=member_ids)}

		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		filter_data_args = {
			"webapp_user_id__in": webapp_user_id2member_id.keys(),
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
			webapp_user_id = order.webapp_user_id
			member_id = webapp_user_id2member_id.get(webapp_user_id)
			created_at = member_id2created_at.get(member_id)
			for channel_qrcode_id, member_ids in channel_qrcode_id2member_id.items():
				if member_id in member_ids:
					flag = False
					if created_at:
						if member_id in q_has_member_ids:
							if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)):
								if channel_qrcode_id2user_created_at.get(
										str(channel_qrcode_id)) <= order.created_at.strftime('%Y-%m-%d %H:%M:%S'):
									if channel_qrcode_id2bing_member_id.get(channel_qrcode_id):
										if curr_qrcode_id2member_id.get(
												channel_qrcode_id) and member_id in curr_qrcode_id2member_id.get(
											channel_qrcode_id):
											if order.created_at.strftime('%Y-%m-%d %H:%M:%S') <= created_at:
												flag = True
										else:
											if order.created_at.strftime('%Y-%m-%d %H:%M:%S') > created_at:
												flag = True
						else:
							if channel_qrcode_id2user_created_at.get(
									str(channel_qrcode_id)) <= order.created_at.strftime(
								'%Y-%m-%d %H:%M:%S'):
								flag = True
					else:
						for channel_qrcode_id, member_ids in channel_qrcode_id2member_id.items():
							if member_id in member_ids:
								if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)):
									if order.created_at.strftime(
											'%Y-%m-%d %H:%M:%S') >= channel_qrcode_id2user_created_at.get(
											str(channel_qrcode_id)):
										flag = True
					if flag:
						if order.status not in [ORDER_STATUS_CANCEL, ORDER_STATUS_GROUP_REFUNDING, ORDER_STATUS_GROUP_REFUNDED, ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED]:
							sale_price += order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
							final_price += order.final_price
							increase_orders.append(order)
						if order.is_first_order and order.status != ORDER_STATUS_NOT:
							first_orders.append(order)

		order_outline_info = {
			"increase_order_count": len(increase_orders),
			"first_order_count": len(first_orders),
			"order_sale_money": u'%.2f' % sale_price,
			"final_price": u'%.2f' % final_price
		}

		total_webapp_user_ids = [order.webapp_user_id for order in orders]

		total_member_order_count = set()
		for webapp_user_id in total_webapp_user_ids:
			total_member_order_count.add(webapp_user_id2member_id[webapp_user_id])

		channel_members = []
		webapp_user_ids = []
		member_order_count = set()
		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			for tcm in total_channel_members:
				created_at = tcm.created_at.strftime('%Y-%m-%d %H:%M:%S')
				if created_at >= start_time and created_at <= end_time:
					channel_members.append(tcm)
			for order in orders:
				created_at = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
				if created_at >= start_time and created_at <= end_time:
					webapp_user_ids.append(order.webapp_user_id)
			for webapp_user_id in webapp_user_ids:
				member_order_count.add(webapp_user_id2member_id[webapp_user_id])

		member_outline_info = {
			"increase_member_count": len(channel_members),
			"member_order_count": len(member_order_count),
			"total_member_order_count": len(total_member_order_count),
			"total_member_count": total_channel_members.count()
		}
		end = time.time()
		print end - start, "oooooooooooo"

		return {
			'items': {
				"order_outline_info": order_outline_info,
				"member_outline_info": member_outline_info
			}
		}
