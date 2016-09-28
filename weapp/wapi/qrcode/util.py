# -*- coding: utf-8 -*-
import time

from datetime import datetime

from mall.models import OrderOperationLog, Order, STATUS2TEXT
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember, \
	ChannelQrcodeBingMember
from modules.member.models import WebAppUser


def get_balance(channel_qrcode_ids, balance_time_from, args, order_status, is_first_order):
	channel_qrcodes = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids).order_by('created_at')
	if balance_time_from:
		created_at = balance_time_from
	else:
		if channel_qrcodes.count() > 0:
			created_at = channel_qrcodes.first().created_at.strftime("%Y-%m-%d %H:%M:%S")
		else:
			created_at = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

	channel_qrcode_members = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=channel_qrcode_ids)
	member_ids = [member_log.member_id for member_log in channel_qrcode_members]
	# 在二维码的会员中有人成为代言人
	bing_member_id2channel_qrcode_id = {}
	bing_member_id2created_at = {}
	# channel_qrcode_bing_members = ChannelQrcodeBingMember.objects.filter(member_id__in=member_ids)
	channel_qrcode_settings = ChannelQrcodeSettings.objects.filter(bing_member_id__in=member_ids)
	for cqs in channel_qrcode_settings:
		bing_member_id2created_at[cqs.bing_member_id] = cqs.created_at.strftime("%Y-%m-%d %H:%M:%S")
		bing_member_id2channel_qrcode_id[cqs.bing_member_id] = cqs.id

	q_member_ids = []
	channel_qrcode_id2member_id = {}
	bing_member_id2qrcode_id = {}
	for cq in channel_qrcodes:
		q_member_ids.append(cq.bing_member_id)
		if cq.is_bing_member:
			if not channel_qrcode_id2member_id.has_key(cq.id):
				channel_qrcode_id2member_id[cq.id] = [cq.bing_member_id]
			else:
				channel_qrcode_id2member_id[cq.id].append(cq.bing_member_id)
			bing_member_id2qrcode_id[cq.bing_member_id] = cq.id
	member_ids = set(member_ids) | set(q_member_ids)

	webapp_user_ids = []
	webapp_user_id2member_id = {}
	webapp_user_id2created_at = {}
	webappusers = WebAppUser.objects.filter(member_id__in=member_ids)
	for webappuser in webappusers:
		webapp_user_ids.append(webappuser.id)
		webapp_user_id2member_id[webappuser.id] = webappuser.member_id
		if bing_member_id2created_at.get(webappuser.member_id):
			webapp_user_id2created_at[webappuser.id] = bing_member_id2created_at.get(webappuser.member_id)

	filter_data_args = {
		"webapp_user_id__in": webapp_user_ids,
		"origin_order_id__lte": 0,
		"created_at__gte": created_at
	}

	cur_start_date = args.get('start_date', None)
	cur_end_date = args.get('end_date', None)

	if order_status == -1:
		filter_data_args["status__in"] = [5, 7, 9]
	else:
		filter_data_args["status__in"] = [7, 9]

	if is_first_order != -1:
		filter_data_args["is_first_order"] = is_first_order

	channel_orders = Order.objects.filter(**filter_data_args)
	order_numbers = [co.order_id for co in channel_orders]
	order_number2finished_at = {}
	# 处理筛选
	if cur_start_date and cur_end_date:
		if cur_start_date < created_at:
			cur_start_date = created_at
		orderoperationlogs = OrderOperationLog.objects.filter(
			order_id__in=order_numbers,
			action__in=[u'完成', u'退款完成'],
			created_at__gte=cur_start_date,
			created_at__lte=cur_end_date
		).exclude(order_id__contains='^')

		for op in orderoperationlogs:
			order_number2finished_at[op.order_id] = op.created_at

	orders = []
	for channel_order in channel_orders:
		member_id = webapp_user_id2member_id[channel_order.webapp_user_id]
		sale_price = channel_order.final_price + channel_order.coupon_money + channel_order.integral_money + channel_order.weizoom_card_money + channel_order.promotion_saved_money + channel_order.edit_money
		final_price = channel_order.final_price
		flag = False
		if webapp_user_id2created_at.get(channel_order.webapp_user_id):
			if bing_member_id2channel_qrcode_id.get(member_id):
				if bing_member_id2channel_qrcode_id.get(member_id) in channel_qrcode_ids:
					if channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= webapp_user_id2created_at.get(channel_order.webapp_user_id) and balance_time_from <= channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'):
						flag = True
				else:
					if channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S') <= webapp_user_id2created_at.get(channel_order.webapp_user_id) and balance_time_from <= channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'):
						flag = True
			else:
				if bing_member_id2qrcode_id.get(member_id):
					if channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= webapp_user_id2created_at.get(channel_order.webapp_user_id) and balance_time_from <= channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'):
						flag = True
		else:
			if balance_time_from <= channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'):
				flag = True
		if flag:
			orders.append({
				"order_id": channel_order.id,
				"order_number": channel_order.order_id,
				"is_first_order": channel_order.is_first_order,
				"status_text": STATUS2TEXT[channel_order.status],
				"sale_price": sale_price,  # 销售额
				"finished_at": order_number2finished_at.get(channel_order.order_id, channel_order.update_at).strftime(
					'%Y-%m-%d %H:%M:%S'),
				"final_price": final_price,
				"created_at": channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			})
	return orders
