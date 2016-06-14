# -*- coding: utf-8 -*-

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from utils.string_util import hex_to_byte, byte_to_hex
from mall.models import Order
import time

class QrcodeMemberOutline(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'member_outline'

	@param_required(['channel_qrcode_id'])
	def get(args):
		"""
		获取会员
		"""
		start = time.time()
		channel_qrcode_id = int(args.get('channel_qrcode_id'))
		channel_qrcode = ChannelQrcodeSettings.objects.filter(id=channel_qrcode_id)
		user_id = 0
		if channel_qrcode.count() > 0:
			user_id = channel_qrcode[0].owner_id
		userprofile = UserProfile.objects.filter(user_id=user_id)
		webapp_id = 0
		if userprofile.count() > 0:
			webapp_id = userprofile[0].webapp_id

		filter_data_args = {
			"channel_qrcode_id": channel_qrcode_id
		}
		total_channel_members = ChannelQrcodeHasMember.objects.filter(**filter_data_args).order_by('-created_at')
		total_member_ids = [tcm.member_id for tcm in total_channel_members]
		webapp_user_id2member_id = {webappuser.id: webappuser.member_id for webappuser in WebAppUser.objects.filter(webapp_id=webapp_id, member_id__in=total_member_ids)}
		orders = Order.objects.filter(webapp_id=webapp_id, webapp_user_id__in=webapp_user_id2member_id.keys(), origin_order_id__lte=0)
		total_webapp_user_ids = [order.webapp_user_id for order in orders]

		total_member_order_count = set()
		for webapp_user_id in total_webapp_user_ids:
			total_member_order_count.add(webapp_user_id2member_id[webapp_user_id])

		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)

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
		print end - start, "pppppppppp"

		return {
			'items': member_outline_info
		}
