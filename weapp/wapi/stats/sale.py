# -*- coding: utf-8 -*-
from core import api_resource, dateutil
from wapi.decorators import param_required
from wapi.wapi_utils import get_webapp_id_via_username

import stats.util as stats_util
from mall.models import *

class Sale(api_resource.ApiResource):
	"""
	为大数据系统提供销售相关数据
	"""
	app = 'stats'
	resource = 'sale'

	@param_required(['un'])
	def get(args):
		"""
		为大数据系统提供销售相关数据

		@param un username
		"""
		username = args.get('un')

		webapp_id = get_webapp_id_via_username(username)

		low_date = '2014-01-01 00:00:00'
		high_date = '%s 23:59:59' % dateutil.get_yesterday_str('today')

		#成交金额
		transaction_money = 0.00
		transaction_nums = get_transaction_orders(webapp_id,low_date,high_date)
		for transaction in transaction_nums:
			tmp_transaction_money = round(transaction.final_price,2) + round(transaction.weizoom_card_money,2)
			transaction_money += tmp_transaction_money

		#成交订单
		transaction_orders = (get_transaction_orders(webapp_id,low_date,high_date)).count()
		#购买总人数
		buyer_count = stats_util.get_buyer_count(webapp_id,low_date,high_date)
		#复购人数
		repeat_buying_member_count = stats_util.get_repeat_buying_member_count(webapp_id, low_date, high_date)
		#成交商品数
		deal_product_count = stats_util.get_deal_product_count(webapp_id, low_date, high_date)
		
		return {
			'total_orders': transaction_orders,
			'total_money': transaction_money,
			'product_count': deal_product_count,
			'buyer_count': buyer_count,
			'repeat_buying_member_count': repeat_buying_member_count
		}


#获取成交订单
def get_transaction_orders(webapp_id,low_date,high_date):
	orders = belong_to(webapp_id)
	transaction_orders = orders.filter(
		Q(created_at__range=(low_date,high_date)),
		Q(status__in=(ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED))
		)
	return transaction_orders