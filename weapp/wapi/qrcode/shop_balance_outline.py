# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_NOT,ORDER_STATUS_CANCEL,ORDER_STATUS_GROUP_REFUNDING,ORDER_STATUS_GROUP_REFUNDED,ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED, OrderOperationLog,STATUS2TEXT
import time
from core import dateutil

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
		channel_qrcode_id2member_id = {}
		total_member_ids = []
		for tcm in total_channel_members:
			if not channel_qrcode_id2member_id.has_key(tcm.channel_qrcode_id):
				channel_qrcode_id2member_id[tcm.channel_qrcode_id] = [tcm.member_id]
			else:
				channel_qrcode_id2member_id[tcm.channel_qrcode_id].append(tcm.member_id)
			total_member_ids.append(tcm.member_id)

		# 在二维码的会员中有人成为代言人
		bing_member_id2created_at = {}
		channel_qrcode_settings = ChannelQrcodeSettings.objects.filter(bing_member_id__in=total_member_ids)
		for cqs in channel_qrcode_settings:
			bing_member_id2created_at[cqs.bing_member_id] = cqs.created_at.strftime("%Y-%m-%d %H:%M:%S")

		bing_member_id2channel_qrcode_id = {}
		q_member_ids = []
		channel_qrcode_id2created_at = {}
		for cq in channel_qrcodes:
			channel_qrcode_id2created_at[cq.id] = cq.created_at.strftime("%Y-%m-%d %H:%M:%S")
			q_member_ids.append(cq.bing_member_id)
			if cq.is_bing_member:
				if not channel_qrcode_id2member_id.has_key(cq.id):
					channel_qrcode_id2member_id[cq.id] = [cq.bing_member_id]
				else:
					channel_qrcode_id2member_id[cq.id].append(cq.bing_member_id)
				bing_member_id2channel_qrcode_id[cq.bing_member_id] = cq.id

		total_member_ids = set(total_member_ids) | set(q_member_ids)

		webappusers = WebAppUser.objects.filter(member_id__in=total_member_ids)

		webapp_user_ids = []
		webapp_user_id2member_id = {}
		webapp_user_id2created_at = {}
		for webappuser in webappusers:
			webapp_user_ids.append(webappuser.id)
			webapp_user_id2member_id[webappuser.id] = webappuser.member_id
			if bing_member_id2created_at.get(webappuser.member_id):
				webapp_user_id2created_at[webappuser.id] = bing_member_id2created_at.get(webappuser.member_id)

		filter_data_args = {
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0,
			'created_at__gte': created_at
		}
		orders = Order.objects.filter(**filter_data_args)
		curr_order_numbers = [o.order_id for o in orders]
		# 获取在某段时间内的已完成和退款完成的订单时间
		orderoperationlogs = OrderOperationLog.objects.filter(
			order_id__in=curr_order_numbers,
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

		channel_qrcode_id2first_order = {}
		channel_qrcode_id2all_order = {}
		for order in orders:
			if not order.order_id in curr_order_numbers:
				member_id = webapp_user_id2member_id[order.webapp_user_id]
				sale_price = order.final_price + order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money + order.edit_money
				final_price = order.final_price
				#除已取消的订单

				if order.status not in [ORDER_STATUS_CANCEL]:
					for channel_qrcode_id,member_ids in channel_qrcode_id2member_id.items():
						if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)) <= order.created_at.strftime("%Y-%m-%d %H:%M:%S"):
							if member_id in member_ids:
								flag = False
								if webapp_user_id2created_at.get(int(order.webapp_user_id)):
									if bing_member_id2channel_qrcode_id.get(member_id):
										if bing_member_id2channel_qrcode_id.get(member_id) == channel_qrcode_id:
											if order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= webapp_user_id2created_at.get(order.webapp_user_id):
												flag = True
										else:
											if order.created_at.strftime('%Y-%m-%d %H:%M:%S') <= webapp_user_id2created_at.get(order.webapp_user_id):
												flag = True
									else:
										if order.created_at.strftime('%Y-%m-%d %H:%M:%S') <= webapp_user_id2created_at.get(
												order.webapp_user_id):
											flag = True
								else:
									flag = True
								if flag:
									if not channel_qrcode_id2all_order.has_key(channel_qrcode_id):
										channel_qrcode_id2all_order[channel_qrcode_id] = [{
											'order_id': order.id,
											'finished_at': order_number2finished_at.get(order.order_id, order.created_at).strftime("%Y-%m-%d %H:%M:%S"),
											'status_text': STATUS2TEXT[order.status],
											'sale_price': sale_price,
											'final_price': final_price,
											'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
										}]
									else:
										channel_qrcode_id2all_order[channel_qrcode_id].append({
											'order_id': order.id,
											'finished_at': order_number2finished_at.get(order.order_id, order.created_at).strftime("%Y-%m-%d %H:%M:%S"),
											'status_text': STATUS2TEXT[order.status],
											'sale_price': sale_price,
											'final_price': final_price,
											'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
										})

				if order.is_first_order and order.status != ORDER_STATUS_NOT:
					for channel_qrcode_id,member_ids in channel_qrcode_id2member_id.items():
						if channel_qrcode_id2user_created_at.get(str(channel_qrcode_id)) <= order.created_at.strftime("%Y-%m-%d %H:%M:%S"):
							if member_id in member_ids:
								flag = False
								if webapp_user_id2created_at.get(int(order.webapp_user_id)):
									if bing_member_id2channel_qrcode_id.get(member_id):
										if bing_member_id2channel_qrcode_id.get(member_id) == channel_qrcode_id:
											if order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= webapp_user_id2created_at.get(order.webapp_user_id):
												flag = True
										else:
											if order.created_at.strftime('%Y-%m-%d %H:%M:%S') < webapp_user_id2created_at.get(order.webapp_user_id):
												flag = True
									else:
										if order.created_at.strftime('%Y-%m-%d %H:%M:%S') < webapp_user_id2created_at.get(
												order.webapp_user_id):
											flag = True
								else:
									flag = True
								if flag:
									if not channel_qrcode_id2first_order.has_key(channel_qrcode_id):
										channel_qrcode_id2first_order[channel_qrcode_id] = [{
											'order_id': order.id,
											'finished_at': order_number2finished_at.get(order.order_id, order.created_at).strftime("%Y-%m-%d %H:%M:%S"),
											'status_text': STATUS2TEXT[order.status],
											'sale_price': sale_price,
											'final_price': final_price,
											'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
										}]
									else:
										channel_qrcode_id2first_order[channel_qrcode_id].append({
											'order_id': order.id,
											'finished_at': order_number2finished_at.get(order.order_id, order.created_at).strftime("%Y-%m-%d %H:%M:%S"),
											'status_text': STATUS2TEXT[order.status],
											'sale_price': sale_price,
											'final_price': final_price,
											'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
										})

		member_outline_info = {
			"channel_qrcode_id2first_order": channel_qrcode_id2first_order,
			"channel_qrcode_id2all_order": channel_qrcode_id2all_order,
		}
		end = time.time()
		print end - start, "shop_balance_outline@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

		return {
			'items': member_outline_info
		}