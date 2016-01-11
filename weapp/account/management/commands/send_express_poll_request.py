# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from django.core.management.base import BaseCommand, CommandError
from tools.express.models import ExpressHasOrderPushStatus, EXPRESS_NOT_PULL_STATUSES
from tools.express.express_poll import ExpressPoll
from mall.models import Order
from datetime import datetime

"""
重新发送 由于网络或其它原因未发送成功的快递订阅请求

EXPRESS_NOT_PULL_STATUSES = [
	EXPRESS_PULL_REFUSE_STATUS,
	EXPRESS_PULL_INFO_ERROR_STATUS,
	EXPRESS_PULL_REPEAT_STATUS
]
express.status 在EXPRESS_NOT_PULL_STATUSES 内的不再发送订阅请求
"""

class Command(BaseCommand):
	help = "send express poll request"
	args = ''

	def handle(self, **options):
		"""
		重新发送未成功的快递订阅请求service
		"""

		print "----------------start"

		skip_count = 0
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

				# 跳过
				if express.status in EXPRESS_NOT_PULL_STATUSES:
					skip_count = skip_count + 1
					print u'-------- skip status in 700, 701, 501; id={}'.format(express.id)
					continue

				if express.abort_receive_message and len(express.abort_receive_message) > 0:
					now = datetime.now()
					minute = (now - express.abort_receive_at).seconds/60
					if minute > 20:
						# 重发
						print u'		again send express poll--'
					else:
						continue
						
				is_success = ExpressPoll(order).get_express_poll()
				try:					
					if not is_success:
						print u"!!!! error send express poll express_id:{}, number:{}, order_id:{}".format(express.id, express.express_number, order.id)
					else:
						count = count + 1					
						print u"success send express poll express_id:{}, number:{}, order_id:{}".format(express.id, express.express_number, order.id)
				except:
					print u"!!!!!!!! system error express_id:{}".format(express.id)

		return u"OK send express length is count={}; skip_count={}".format(count, skip_count)