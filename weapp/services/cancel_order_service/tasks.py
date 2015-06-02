#coding:utf8
"""@package services.cancel_order_service.tasks
取消订单的service

"""
from django.conf import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info

from mall.promotion import models as promotion_models

from celery import task


@task
def cancel_order(request, args):
	"""
	取消订单的service

	@param request 无用，为了兼容
	@param args dict类型，内含order_id, reason
	"""
	# 构造request对象
	promotion_id = args['id']
	promotion_models.Promotion.objects.filter(id=promotion_id).update(status=promotion_models.PROMOTION_STATUS_FINISHED)
	watchdog_info('将promotion(%s)状态改为PROMOTION_STATUS_FINISHED' % promotion_id)
	return "OK"
