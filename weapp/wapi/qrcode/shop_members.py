# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from mall.models import Order
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from utils.string_util import hex_to_byte, byte_to_hex

class QrcodeMember(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'shop_members'

	@param_required(['channel_qrcode_ids'])
	def get(args):
		"""
		获取会员
		"""
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'))
		channel_qrcodes = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids)

		channel_qrcode_ids = [c.id for c in channel_qrcodes]
		user_id = 0
		if channel_qrcodes.count() > 0:
			user_id = channel_qrcodes[0].owner_id
		userprofile = UserProfile.objects.filter(user_id=user_id)
		webapp_id = 0
		if userprofile.count() > 0:
			webapp_id = userprofile[0].webapp_id

		filter_data_args = {
			"channel_qrcode_id__in": channel_qrcode_ids
		}
		total_channel_members = ChannelQrcodeHasMember.objects.filter(**filter_data_args).order_by('-created_at')
		channel_qrcode_id2channel_member = {}
		total_member_ids = []
		for m in total_channel_members:
			total_member_ids.append(m.member_id)
			if not channel_qrcode_id2channel_member.has_key(m.channel_qrcode_id):
				channel_qrcode_id2channel_member[m.channel_qrcode_id] = [m]
			else:
				channel_qrcode_id2channel_member[m.channel_qrcode_id].append(m)

		webapp_user_id2member_id = {webappuser.id: webappuser.member_id for webappuser in WebAppUser.objects.filter(webapp_id=webapp_id, member_id__in=total_member_ids)}
		orders = Order.objects.filter(webapp_id=webapp_id, webapp_user_id__in=webapp_user_id2member_id.keys(),origin_order_id__lte=0)
		total_webapp_user_ids = [order.webapp_user_id for order in orders]

		channel_qrcode_id2total_member_order = {}
		for webapp_user_id in total_webapp_user_ids:
			member_id = webapp_user_id2member_id[webapp_user_id]
			for channel_qrcode_id, channel_members in channel_qrcode_id2channel_member.items():
				member_ids = [cm.member_id for cm in channel_members]
				if member_id in member_ids:
					if not channel_qrcode_id2total_member_order.has_key(str(channel_qrcode_id)):
						channel_qrcode_id2total_member_order[str(channel_qrcode_id)] = [member_id]
					else:
						channel_qrcode_id2total_member_order[str(channel_qrcode_id)].append(member_id)

		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)

		channel_qrcode_id2increase_member_count = {}
		webapp_user_ids = []
		channel_qrcode_id2member_order = {}
		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			for channel_qrcode_id, channel_member in channel_qrcode_id2channel_member.items():
				for tcm in channel_member:
					created_at = tcm.created_at.strftime('%Y-%m-%d %H:%M:%S')
					if created_at >= start_time and created_at <= end_time:
						if not channel_qrcode_id2increase_member_count.has_key(str(channel_qrcode_id)):
							channel_qrcode_id2increase_member_count[str(channel_qrcode_id)] = 1
						else:
							channel_qrcode_id2increase_member_count[str(channel_qrcode_id)] += 1
			for order in orders:
				created_at = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
				if created_at >= start_time and created_at <= end_time:
					webapp_user_ids.append(order.webapp_user_id)
			for webapp_user_id in webapp_user_ids:
				member_id = webapp_user_id2member_id[webapp_user_id]
				for channel_qrcode_id, channel_members in channel_qrcode_id2channel_member.items():
					member_ids = [cm.member_id for cm in channel_members]
					if member_id in member_ids:
						if not channel_qrcode_id2member_order.has_key(str(channel_qrcode_id)):
							channel_qrcode_id2member_order[str(channel_qrcode_id)] = [member_id]
						else:
							channel_qrcode_id2member_order[str(channel_qrcode_id)].append(member_id)
		channel_qrcode_id2total_member_order_count = {}
		for channel_qrcode_id, total_member_order in channel_qrcode_id2total_member_order.items():
			channel_qrcode_id2total_member_order_count[channel_qrcode_id] = len(set(total_member_order))

		channel_qrcode_id2member_order_count = {}
		for channel_qrcode_id, member_order in channel_qrcode_id2member_order.items():
			channel_qrcode_id2member_order_count[channel_qrcode_id] = len(set(member_order))

		channel_qrcode_id2channel_member_count = {}
		for channel_qrcode_id, channel_member in channel_qrcode_id2channel_member.items():
			channel_qrcode_id2channel_member_count[channel_qrcode_id] = len(channel_member)

		return {
			"channel_qrcode_id2increase_member_count": channel_qrcode_id2increase_member_count,
			"channel_qrcode_id2member_order_count": channel_qrcode_id2member_order_count,
			"channel_qrcode_id2total_member_order_count": channel_qrcode_id2total_member_order_count,
			"channel_qrcode_id2channel_member_count": channel_qrcode_id2channel_member_count
		}
