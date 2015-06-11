# -*- coding: utf-8 -*-
import random

from watchdog.utils import watchdog_alert, watchdog_warning
from core.exceptionutil import unicode_full_stack

from mall import models as mall_models
from mall import module_api as mall_api
from webapp.modules.mall import util as mall_util
from core import dateutil
from market_tools.tools.template_message import module_api as template_message_api

from celery import task

def __gen_thanks_card_secret():
	"""
	__gen_thanks_card_secret: 生成感恩密码
	"""
	secret = random.randint(1000000, 9999999)
	if mall_models.ThanksCardOrder.objects.filter(thanks_secret=secret).count() > 0:
		return __gen_thanks_card_secret()
	else:
		return secret


def serve(request, args):
	event_specific_data = args['event_specific_data']
	order_order_id = event_specific_data['order_order_id']
	#记录日志
	mall_api.record_operation_log(order_order_id, u'客户', u'支付')
	mall_api.record_status_log(order_order_id, u'客户', mall_models.ORDER_STATUS_NOT, mall_models.ORDER_STATUS_PAYED_NOT_SHIP)

	webapp_id = request.user_profile.webapp_id
	webapp_user = request.webapp_user
	order = mall_models.Order.objects.get(order_id=order_order_id)

	#记录购买统计项
	try:
		mall_models.PurchaseDailyStatistics.objects.create(
			webapp_id = webapp_id,
			webapp_user_id = webapp_user.id,
			order_id = order.order_id,
			order_price = order.final_price,
			date = dateutil.get_today()
		)

		#更新webapp_user的has_purchased字段
		webapp_user.set_purchased()
	except:
		alert_message = u"post_pay_order service: 调用webapp_user.complete_payment失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

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

	#生成感恩卡密码
	try:
		order_has_products = mall_models.OrderHasProduct.objects.filter(order_id=order.id)
		is_thanks_card_order = False
		for order_has_product in order_has_products:
			product = mall_models.Product.objects.get(id = order_has_product.product_id)
			if product.is_support_make_thanks_card:
				is_thanks_card_order = True
				for i in range(order_has_product.number):	#购买几个商品创建几个密码
					secret = __gen_thanks_card_secret()
					member_id = 0	#bdd测试不支持request.member
					if request.member:
						member_id = request.member.id
					mall_models.ThanksCardOrder.objects.create(
						order_id= order.id,
						thanks_secret= secret,
						card_count= 0,
						listen_count= 0,
						is_used= False,
						title='',
						content='',
						type=mall_models.IMG_TYPE,
						att_url='',
						member_id=member_id)
			if is_thanks_card_order:
				mall_models.Order.objects.filter(order_id=order.order_id).update(type = mall_models.THANKS_CARD_ORDER)
	except:
		alert_message = u"post_pay_order service: 生成感恩密码失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user') and request.user:
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

	try:
		mall_util.email_order(order=order)
	except:
		notify_message = u"post_pay_order service: 订单状态为已付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order.order_id, webapp_id, unicode_full_stack())
		watchdog_alert(notify_message)


@task
def post_pay_order(request0, args):
	from services.service_manager import create_request
	request = create_request(args)
	serve(request, args)
	return 'OK'
