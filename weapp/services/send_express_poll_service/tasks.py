#coding:utf8

__author__ = 'liupeiyu'

"""
@package services.send_express_poll_service.tasks
重新发送 由于网络或其它原因未发送成功的快递订阅请求
"""
from tools.express.models import ExpressHasOrderPushStatus
from tools.express.express_poll import ExpressPoll
from mall.models import Order
from datetime import datetime

from celery import task

@task
def send_express_poll_request(request, args):
	"""
	重新发送未成功的快递订阅请求service
	"""

	print "----------------start"

	count = 0
	expresses = ExpressHasOrderPushStatus.objects.filter(receive_count=0)
	for express in expresses:
		if express.send_count > 0 and len(express.abort_receive_message) == 0:
			# 已发送，并且不是已关闭的，将不再发送
			continue
		if express.send_count >= 4:
			# 发送超过4次，就不再重发
			continue
			
		orders = Order.objects.filter(
			express_company_name=express.express_company_name, 
			express_number=express.express_number
		)
				
		if orders.count() > 0:
			order = orders[0]

			if len(express.abort_receive_message) > 0:
				now = datetime.now()
				minute = (now - express.abort_receive_at).seconds/60
				if minute > 20:
					# 重发
					print u'		again send express poll--'
				else:
					continue
					
			is_success = ExpressPoll(order).get_express_poll()
			if not is_success:
				print u"!!!! error send express poll express_id:{}, number:{}, order_id:{}".format(express.id, express.express_number, order.id)
			else:
				print u"success send express poll express_id:{}, number:{}, order_id:{}".format(express.id, express.express_number, order.id)
				count = count + 1

	return u"OK send express length is {}".format(count)