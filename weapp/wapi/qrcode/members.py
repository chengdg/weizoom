# -*- coding: utf-8 -*-
import json

from django.db.models import Q

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

	@param_required(['channel_qrcode_ids'])
	def get(args):
		"""
		获取会员
		"""
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids',"[]"))
		channel_qrcode_id2user_created_at = json.loads(args.get('channel_qrcode_id2user_created_at',"[]"))

		filter_data_args = {
			"channel_qrcode_id__in": channel_qrcode_ids
		}
		settings_filter_args = {}

		member_name = args.get('member_name', None)
		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		if member_name:
			members = Member.objects.filter(username_hexstr__contains=byte_to_hex(member_name))
			member_ids = []
			for member in members:
				member_ids.append(member.id)
			filter_data_args["member_id__in"] = member_ids
			settings_filter_args["bing_member_id__in"] = member_ids

		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			members = Member.objects.filter(created_at__gte=start_time, created_at__lte=end_time)
			member_ids = []
			for member in members:
				member_ids.append(member.id)
			filter_data_args["member_id__in"] = member_ids
			settings_filter_args["bing_member_id__in"] = member_ids


		channel_members = ChannelQrcodeHasMember.objects.filter(**filter_data_args).order_by('-created_at')
		total_member_ids = []
		q_has_member_ids = []
		channel_qrcode_id2q_has_member_ids = {}
		channel_qrcode_id2member_id = {}
		for member_log in channel_members:
			if not channel_qrcode_id2q_has_member_ids.has_key(member_log.channel_qrcode_id):
				channel_qrcode_id2q_has_member_ids[member_log.channel_qrcode_id] = [member_log.member_id]
			else:
				channel_qrcode_id2q_has_member_ids[member_log.channel_qrcode_id].append(member_log.member_id)
			q_has_member_ids.append(member_log.member_id)
			total_member_ids.append(member_log.member_id)
			if not channel_qrcode_id2member_id.has_key(member_log.channel_qrcode_id):
				channel_qrcode_id2member_id[member_log.channel_qrcode_id] = [member_log.member_id]
			else:
				channel_qrcode_id2member_id[member_log.channel_qrcode_id].append(member_log.member_id)

		q_settings = ChannelQrcodeSettings.objects.filter(**settings_filter_args).filter(Q(id__in=channel_qrcode_ids)|Q(bing_member_id__in=total_member_ids))
		q_member_id2created_at = {}
		for qs in q_settings:
			if qs.is_bing_member:
				if str(qs.id) in channel_qrcode_ids:
					total_member_ids.append(qs.bing_member_id)
				if not channel_qrcode_id2member_id.has_key(qs.id):
					channel_qrcode_id2member_id[qs.id] = [qs.bing_member_id]
				else:
					channel_qrcode_id2member_id[qs.id].append(qs.bing_member_id)
				q_member_id2created_at[qs.bing_member_id] = qs.created_at.strftime('%Y-%m-%d %H:%M:%S')

		#处理分页
		count_per_page = int(args.get('count_per_page', '20'))
		cur_page = int(args.get('cur_page', '1'))
		pageinfo, total_member_ids = paginator.paginate(total_member_ids, cur_page, count_per_page)


		webapp_users = WebAppUser.objects.filter(member_id__in=total_member_ids)
		webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
		webapp_user_ids = set(webapp_user_id2member_id.keys())
		if webapp_user_ids:
			orders = Order.by_webapp_user_id(webapp_user_ids).filter(status__in=[ORDER_STATUS_SUCCESSED]).order_by('-created_at')
		else:
			orders = []

		final_price = 0
		channel_qrcode_id2member = {}
		for order in orders:
			member_id = webapp_user_id2member_id[order.webapp_user_id]
			created_at = q_member_id2created_at.get(member_id)
			final_price += order.final_price
			sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
			if member_id in q_has_member_ids:
				for channel_qrcode_id, member_ids in channel_qrcode_id2member_id.items():
					q_member_ids = channel_qrcode_id2q_has_member_ids.get(channel_qrcode_id)
					if created_at:
						if q_member_ids:
							if order.created_at.strftime('%Y-%m-%d %H:%M:%S') < created_at:
								if member_id in member_ids:
									if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)):
										if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)) <= order.created_at.strftime('%Y-%m-%d %H:%M:%S'):
											channel_qrcode_id2member = get_member(member_id, channel_qrcode_id, channel_qrcode_id2member, final_price,sale_price)
						else:
							if order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= created_at:
								if member_id in member_ids:
									channel_qrcode_id2member = get_member(member_id, channel_qrcode_id, channel_qrcode_id2member, final_price, sale_price)
					else:
						if order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)):
							channel_qrcode_id2member = get_member(member_id, channel_qrcode_id, channel_qrcode_id2member, final_price, sale_price)
			else:
				for channel_qrcode_id, member_ids in channel_qrcode_id2member_id.items():
					if member_id in member_ids:
						if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)):
							print order.webapp_user_id, order.created_at.strftime('%Y-%m-%d %H:%M:%S'), channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)),"ddddddddddddddddddddd"
							if order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)):
								if order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= created_at:
									channel_qrcode_id2member = get_member(member_id, channel_qrcode_id, channel_qrcode_id2member, final_price, sale_price)

		members = []
		member_id2member = {m.id: m for m in Member.objects.filter(id__in=total_member_ids).order_by('-created_at')}
		for channel_qrcode_id,member_ids in channel_qrcode_id2member_id.items():
			if str(channel_qrcode_id) in channel_qrcode_ids:
				for member_id in member_ids:
					member = member_id2member.get(member_id)
					if member:
						member_info = channel_qrcode_id2member.get(channel_qrcode_id)
						if member_info:
							info = member_info.get(member_id)
							if info:
								members.append({
									"channel_qrcode_id": channel_qrcode_id,
									"member_name": member_id2member[member_id].username_for_html,
									"follow_time": member_id2member[member_id].created_at.strftime('%Y-%m-%d %H:%M:%S'),
									"pay_times": info["order_count"],
									'pay_money': '%.2f' % info["sale_money"],
									"final_price": '%.2f' % info["final_price"]
								})
							else:
								members.append({
									"channel_qrcode_id": channel_qrcode_id,
									"member_name": member.username_for_html,
									"follow_time": member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
									"pay_times": 0,
									'pay_money': '%.2f' % 0,
									"final_price": '%.2f' % 0
								})
						else:
							members.append({
								"channel_qrcode_id": channel_qrcode_id,
								"member_name": member.username_for_html,
								"follow_time": member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
								"pay_times": 0,
								'pay_money': '%.2f' % 0,
								"final_price": '%.2f' % 0
							})

		return {
			'items': members,
			'pageinfo': paginator.to_dict(pageinfo) if pageinfo else ''
		}

def get_member(member_id,channel_qrcode_id,channel_qrcode_id2member, final_price, sale_price):
	if not channel_qrcode_id2member.has_key(channel_qrcode_id):
		channel_qrcode_id2member[channel_qrcode_id] = {
			member_id: {
				"order_count": 1,
				"final_price": final_price,
				"sale_money": sale_price
			}
		}
	else:
		member = channel_qrcode_id2member[channel_qrcode_id]
		if not member.has_key(member_id):
			member[member_id] = {
				"order_count": 1,
				"final_price": final_price,
				"sale_money": sale_price
			}
		else:
			member[member_id]["order_count"] += 1
			member[member_id]["final_price"] += final_price
			member[member_id]["sale_money"] += sale_price
	return channel_qrcode_id2member