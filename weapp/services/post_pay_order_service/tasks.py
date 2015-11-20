# -*- coding: utf-8 -*-
import random

from watchdog.utils import watchdog_alert, watchdog_warning
from core.exceptionutil import unicode_full_stack

from mall import models as mall_models
from mall import module_api as mall_api
from webapp.modules.mall import util as mall_util
from core import dateutil
from market_tools.tools.template_message import module_api as template_message_api
import json
from celery import task

def serve(request, args):
	event_specific_data = args['event_specific_data']
	order_order_id = event_specific_data['order_order_id']
	#记录日志
	mall_api.record_operation_log(order_order_id, u'客户', u'支付')
	mall_api.record_status_log(order_order_id, u'客户', mall_models.ORDER_STATUS_NOT, mall_models.ORDER_STATUS_PAYED_NOT_SHIP)

	webapp_id = request.user_profile.webapp_id
	webapp_user = request.webapp_user
	order = mall_models.Order.objects.get(order_id=order_order_id)

	#支付完成之后的webapp_user操作
	try:
		webapp_user.complete_payment(request, order)
	except:
		alert_message = u"post_pay_order service: 调用webapp_user.complete_payment失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

	#发送模板消息
	try:
		template_message_api.send_order_template_message(order.webapp_id, order.id, 0)
	except:
		alert_message = u"post_pay_order service: 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
		watchdog_warning(alert_message)
	#todo zhaolei  需要优化，这样写不容易排错
	print "zlllllllll--------------------send_order_email"
	from webapp.handlers import event_handler_util
	from utils import json_util
	event_data = {'order':json.dumps(order.to_dict(),cls=json_util.DateEncoder)}
	event_handler_util.handle(event_data, 'send_order_email')
	print "zlllllllll--------------------send_order_email"
	# try:
	# 	mall_util.email_order(order=order)
	# except:
	# 	notify_message = u"post_pay_order service: 订单状态为已付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order.order_id, webapp_id, unicode_full_stack())
	# 	watchdog_alert(notify_message)


@task
def post_pay_order(request0, args):
	from services.service_manager import create_request
	request = create_request(args)
	serve(request, args)
	return 'OK'
