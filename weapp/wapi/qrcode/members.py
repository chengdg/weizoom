# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from mall.models import Order, ORDER_STATUS_SUCCESSED, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_PAYED_NOT_SHIP, \
	ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_NOT
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from utils.string_util import hex_to_byte, byte_to_hex

class QrcodeMember(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'members'

	@param_required(['channel_qrcode_id'])
	def get(args):
		"""
		获取会员
		"""
		channel_qrcode_id = int(args.get('channel_qrcode_id'))
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids',"[]"))

		if channel_qrcode_ids:
			filter_data_args = {
				"channel_qrcode_id__in": channel_qrcode_ids
			}
		else:
			filter_data_args = {
				"channel_qrcode_id": channel_qrcode_id
			}

		member_name = args.get('member_name', None)
		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		if member_name:
			members = Member.objects.filter(username_hexstr__contains=byte_to_hex(member_name))
			member_ids = []
			for member in members:
				member_ids.append(member.id)
			filter_data_args["member_id__in"] = member_ids

		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			members = Member.objects.filter(created_at__gte=start_time, created_at__lte=end_time)
			member_ids = []
			for member in members:
				member_ids.append(member.id)
			filter_data_args["member_id__in"] = member_ids

		channel_members = ChannelQrcodeHasMember.objects.filter(**filter_data_args).order_by('-created_at')

		#处理分页
		count_per_page = int(args.get('count_per_page', '20'))
		cur_page = int(args.get('cur_page', '1'))
		pageinfo, channel_members = paginator.paginate(channel_members, cur_page, count_per_page)
		member_ids = [member_log.member_id for member_log in channel_members]
		webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)
		webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
		webapp_user_ids = set(webapp_user_id2member_id.keys())
		if webapp_user_ids:
			orders = Order.by_webapp_user_id(webapp_user_ids).filter(status__in=[ORDER_STATUS_SUCCESSED]).order_by('-created_at')
		else:
			orders = []

		webapp_user_id2final_price = {}
		webapp_user_id2sale_money = {}
		final_price = 0
		for order in orders:
			final_price += order.final_price
			if not webapp_user_id2final_price.has_key(order.webapp_user_id):
				webapp_user_id2final_price[order.webapp_user_id] = order.final_price
			else:
				webapp_user_id2final_price[order.webapp_user_id] += order.final_price

			sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
			if not webapp_user_id2sale_money.has_key(order.webapp_user_id):
				webapp_user_id2sale_money[order.webapp_user_id] = sale_price
			else:
				webapp_user_id2sale_money[order.webapp_user_id] += sale_price

		channel_members = Member.objects.filter(id__in=member_ids)
		members = []
		for channel_member in channel_members:
			final_price = 0
			pay_money = 0
			for webapp_user_id,member_id in webapp_user_id2member_id.items():
				if member_id == channel_member.id:
					final_price = webapp_user_id2final_price.get(webapp_user_id, 0)
					pay_money = webapp_user_id2sale_money.get(webapp_user_id, 0)
			members.append({
				"member_name": channel_member.username_for_html,
				"follow_time": channel_member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				"pay_times": channel_member.pay_times,
				'pay_money': '%.2f' % pay_money,
				"final_price": '%.2f' % final_price
			})

		return {
			'items': members,
			'pageinfo': paginator.to_dict(pageinfo) if pageinfo else ''
		}
