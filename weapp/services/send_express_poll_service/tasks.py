#coding:utf8

__author__ = 'liupeiyu'

"""
@package services.send_express_poll_service.tasks
重新发送 由于网络或其它原因未发送成功的快递订阅请求
"""
from tools.express.models import ExpressHasOrderPushStatus
from tools.express.express_poll import ExpressPoll
from mall.models import Order

from celery import task

@task
def send_express_poll_request(request, args):
	"""
	重新发送未成功的快递订阅请求service
	"""

	print "start"

	count = 0
	expresses = ExpressHasOrderPushStatus.objects.filter(send_count=0)
	for express in expresses:
		orders = Order.objects.filter(
			express_company_name=express.express_company_name, 
			express_number=express.express_number
		)
		if orders.count() > 0:
			order = orders[0]
			is_success = ExpressPoll(order).get_express_poll()
			if not is_success:
				print u"failure send express poll express_id:{}, order_id:{}".format(express.id, order.id)
			else:
				count = count + 1

	return u"OK send express length is {}".format(count)