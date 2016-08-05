# -*- coding: utf-8 -*-
import time

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog


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
		channel_qrcode_id = int(args.get('channel_qrcode_id'))
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
			"origin_order_id__lte": 0,

		}
		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		filter_data_args["status__in"] = [ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED]
		#处理筛选
		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			start = time.time()

			# order_numbers = [op.order_id for op in OrderOperationLog.objects.filter(created_at__gte=start_time,created_at__lte=end_time)]

			order_numbers = [op.order_id for op in OrderOperationLog.objects.filter(action__in=[u'完成', u'退款完成'],created_at__gte=start_time,created_at__lte=end_time)]
			end = time.time()
			print end - start,"pppppppppp"
			filter_data_args["order_id__in"] = order_numbers

		channel_orders = Order.objects.filter(**filter_data_args).order_by('-created_at')

		orders = []
		for channel_order in channel_orders:
			sale_price = channel_order.final_price + channel_order.coupon_money + channel_order.integral_money + channel_order.weizoom_card_money + channel_order.promotion_saved_money + channel_order.edit_money
			orders.append({
				"order_id": channel_order.id,
				"is_first_order": channel_order.is_first_order,
				"status_text": STATUS2TEXT[channel_order.status],
				"sale_price": sale_price,  #销售额
			})

		return {
			'items': orders,
		}
