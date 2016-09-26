# -*- coding: utf-8 -*-
import json
import time

from django.contrib.auth.models import User

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember, \
	ChannelQrcodeBingMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog, \
	ORDER_STATUS_GROUP_REFUNDED
from core import dateutil
import util

class QrcodeBalance(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'balance'

	@param_required(['channel_qrcode_ids'])
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
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'))
		order_status = int(args.get('order_status', '-1'))
		is_first_order = int(args.get('is_first_order', '-1'))
		balance_time_from = args.get('balance_time_from',None)

		orders = util.get_balance(channel_qrcode_ids, balance_time_from, args, order_status, is_first_order)
		end = time.time()
		print end - start, "bbbbbbbbbbbbbbbbb"

		return {
			'items': orders
		}