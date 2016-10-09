# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_NOT,ORDER_STATUS_CANCEL,ORDER_STATUS_GROUP_REFUNDING,ORDER_STATUS_GROUP_REFUNDED,ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED, OrderOperationLog,STATUS2TEXT
import time
from core import dateutil
import util

class ShopBalanceOutline(api_resource.ApiResource):
	"""
	帐号管理
	"""
	app = 'qrcode'
	resource = 'shop_balance_outline'

	@param_required(['channel_qrcode_ids'])
	def get(args):
		"""
		获取会员
		"""
		start = time.time()
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'))
		order_numbers = json.loads(args.get('order_numbers', ''))
		channel_qrcode_id2user_created_at = json.loads(args.get('channel_qrcode_id2user_created_at'))

		channel_qrcodes = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids).order_by('created_at')
		if channel_qrcodes.count() > 0:
			created_at = channel_qrcodes.first().created_at.strftime("%Y-%m-%d %H:%M:%S")
		else:
			created_at = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

		total_channel_members = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=channel_qrcode_ids).order_by('-created_at')
		total_member_ids = []
		for tcm in total_channel_members:
			total_member_ids.append(tcm.member_id)

		q_member_ids = []
		for cq in channel_qrcodes:
			if cq.is_bing_member:
				q_member_ids.append(cq.bing_member_id)

		total_member_ids = set(total_member_ids) | set(q_member_ids)

		webappusers = WebAppUser.objects.filter(member_id__in=total_member_ids)

		webapp_user_ids = []
		for webappuser in webappusers:
			webapp_user_ids.append(webappuser.id)

		filter_data_args = {
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0,
			"created_at__gte": created_at
		}

		orders = Order.objects.filter(**filter_data_args).exclude(order_id__in=order_numbers)
		balance_outline_info = util.get_balance_outline(orders, channel_qrcodes, created_at, channel_qrcode_ids,order_numbers, channel_qrcode_id2user_created_at)
		# balance_outline_info = util.get_balance_outline(channel_qrcode_ids, order_numbers, channel_qrcode_id2user_created_at)

		return {
			'items': balance_outline_info
		}