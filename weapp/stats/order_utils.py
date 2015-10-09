#coding: utf8
"""
有关订单数据的函数

"""

from mall.models import *

def get_paid_orders(webapp_id, start_date, end_date):
	"""
	获得有效订单

	所谓有效订单是指：已经支付过的、没有退单的订单

	@param webapp_id webapp_id
	@param start_date 开始年月日
	@param end_date 结束年月日

	@author victor
	"""
	orders = Order.by_webapp_id(webapp_id).filter(
			created_at__range=(start_date, end_date), \
			status__in=(ORDER_STATUS_PAYED_SUCCESSED, \
				ORDER_STATUS_PAYED_NOT_SHIP, \
				ORDER_STATUS_PAYED_SHIPED, \
				ORDER_STATUS_SUCCESSED))
	#print([(order.id, order.status) for order in orders])
	return orders	
