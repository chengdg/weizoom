#coding:utf8
"""@package services.post_save_order_service.tasks
未读订单计数

@note 已增加BDD feature

"""

from watchdog.utils import watchdog_alert, watchdog_info
from core.exceptionutil import unicode_full_stack

from mall import models as mall_models
from mall import module_api as mall_api
from webapp.modules.mall import util as mall_util

from celery import task

def serve(request, args):
	#mall_models.MallCounter.increase_unread_order(request.webapp_owner_id, 1) #增加未读订单计数
	mall_models.increase_unread_order(request.webapp_owner_id, 1) #增加未读订单计数
	watchdog_info("increased unread order by 1 in MallCounter, oid: {}".format(request.webapp_owner_id))
	
	event_specific_data = args['event_specific_data']
	order_order_id = event_specific_data['order_order_id']
	mall_api.record_operation_log(order_order_id, u'客户', u'下单')

	order = mall_models.Order.objects.get(order_id=order_order_id)
	try:
		mall_util.email_order(order=order)
	except:
		notify_message = u"订单状态为等待付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order.order_id, request.webapp_owner_id, unicode_full_stack())
		watchdog_alert(notify_message)
		#print("ALERT: {}".format(notify_message))
	#print 'finish'


@task
def post_save_order(request0, args):
	from services.service_manager import create_request
	request = create_request(args)
	serve(request, args)
