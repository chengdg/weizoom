# -*- coding: utf-8 -*-
import time

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog
# from datetime import datetime
import datetime

class QrcodeBalance(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'balance'

	@param_required(['channel_qrcode_id'])
	def get(args):
		"""
		获取结算的数据
		现金总收入：订单提成+首单提成
		订单提成：（店铺总销售额-店铺退款金额）*？%
		首单提成：已完成的首次下单个数*？
		店铺总销售额：已完成订单的总额
		店铺退款金额：该订单上次已结算过，但本期次订单发生了退款，这类的退款订单金额
		"""
		start = time.time()
		channel_qrcode_id = int(args.get('channel_qrcode_id'))
		balance_time_from = args.get('balance_time_from','2016-06-24 00:00:00')
		channel_qrcode = ChannelQrcodeSettings.objects.filter(id=channel_qrcode_id)
		user_id = 0
		if channel_qrcode.count() > 0:
			user_id = channel_qrcode[0].owner_id
		userprofile = UserProfile.objects.filter(user_id=user_id)
		webapp_id = 0
		if userprofile.count() > 0:
			webapp_id = userprofile[0].webapp_id

		member_ids = [member_log.member_id for member_log in ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=channel_qrcode_id)]
		webapp_user_ids = [webappuser.id for webappuser in WebAppUser.objects.filter(webapp_id=webapp_id, member_id__in=member_ids)]

		filter_data_args = {
			"webapp_id": webapp_id,
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0
		}
		print balance_time_from,"dddddddddd"
		if balance_time_from:
			filter_data_args["created_at__gte"] = balance_time_from

		cur_start_date = args.get('start_date', None)
		cur_end_date = args.get('end_date', None)
		print cur_start_date,cur_end_date,"ppppppppppppppppp"
		filter_data_args["status__in"] = [ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED]
		channel_orders = Order.objects.filter(**filter_data_args).order_by('-created_at')
		order_numbers = [co.order_id for co in channel_orders]
		order_number2index = {}
		date_range = []
		order_log_numbers = []
		order_number2finished_at = {}
		#处理筛选
		if cur_start_date and cur_end_date:
			date_last = cur_end_date
			start_y_str, start_m_str, start_d_str = cur_start_date.split('-')
			end_y_str, end_m_str, end_d_str = cur_end_date.split('-')
			start_y = int(start_y_str)
			start_m = int(start_m_str)
			end_y = int(end_y_str)
			end_m = int(end_m_str)
			if start_y == end_y:
				if start_m == end_m:
					#获取开始时间的当月第一天
					date_first = '%s-%s-01' % (start_y_str, start_m_str)
					date_last = (datetime.datetime(start_y, start_m + 1, 1) - datetime.timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")
					date_range.append([date_first, date_last])
				else:
					diff_m = end_m - start_m
					for i in range(diff_m+1):
						cur_m = start_m + i
						date_first = '%s-%s-01' % (start_y_str, str(cur_m) if len(str(cur_m)) >2 else '0'+ str(cur_m))
						date_last = (datetime.datetime(start_y, cur_m + 1, 1) - datetime.timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")
						date_range.append([date_first, date_last])
			orderoperationlogs = OrderOperationLog.objects.filter(
				order_id__in=order_numbers,
				action__in=[u'完成', u'退款完成'],
				created_at__gte=cur_start_date,
				created_at__lte=cur_end_date
			)

			for date_list in date_range:
				i = 1
				for op in orderoperationlogs:
					if op.created_at.strftime("%Y-%m-%d %H:%M:%S") >= cur_start_date and op.created_at.strftime("%Y-%m-%d %H:%M:%S") <= cur_end_date:
						order_log_numbers.append(op.order_id)
					if op.created_at.strftime("%Y-%m-%d %H:%M:%S") >= date_list[0] and op.created_at.strftime("%Y-%m-%d %H:%M:%S") <= date_list[1] and op.action == u'完成':
						order_number2index[op.order_id] = i
						i += 1
					order_number2finished_at[op.order_id] = op.created_at

		orders = []
		for channel_order in channel_orders:
			if channel_order.order_id in order_log_numbers:
				sale_price = channel_order.final_price + channel_order.coupon_money + channel_order.integral_money + channel_order.weizoom_card_money + channel_order.promotion_saved_money + channel_order.edit_money
				final_price = channel_order.final_price + channel_order.weizoom_card_money
				orders.append({
					"order_id": channel_order.id,
					"order_number": channel_order.order_id,
					"is_first_order": channel_order.is_first_order,
					"status_text": STATUS2TEXT[channel_order.status],
					"sale_price": sale_price,  #销售额
					"finished_at": order_number2finished_at.get(channel_order.order_id, channel_order.update_at).strftime('%Y-%m-%d %H:%M:%S'),
					"final_price": final_price,
					"created_at": channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				})
		end = time.time()
		print end - start, "pppppppppp"

		return {
			'items': orders
		}
