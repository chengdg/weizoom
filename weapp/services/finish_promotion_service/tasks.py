#coding:utf8
"""@package services.finish_promotion_service.tasks
finish_promotion_service 的Celery task实现

"""
import sys
from django.conf import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from datetime import datetime

from mall.promotion import models as promotion_models
from mall import models as mall_models

from celery import task
from utils import cache_util


class FakeRequest(object):
	def __init__(self):
		pass


def cancel_order_for_promotion(promotion_ids):
	from webapp.handlers import event_handler_util
	from webapp.modules.mall import request_api_util
	try:
		for promotion_id in promotion_ids:
			promotion = promotion_models.Promotion.objects.get(id=promotion_id)
			user = promotion.owner
			order_ids = [relation.order_id for relation in mall_models.OrderHasPromotion.objects.filter(promotion_id=promotion_id)]
			invalid_order_ids = [order.id for order in mall_models.Order.objects.filter(id__in=order_ids, status=mall_models.ORDER_STATUS_NOT)]
			for order_id in invalid_order_ids:
				request = FakeRequest()
				request.user = user
				request.POST = {
					"order_id": order_id,
					"action": "cancel"
				}
				request.GET = {
					"reason": "promotion %s is finished" % promotion_id
				}
				request_api_util.update_order_status(request)
	except:
		watchdog_error(u"failed to send cancel order event by finish promotion, cause:\n{}".format(unicode_full_stack()))


@task
def finish_promotion(request0, args):
	"""
	将promotion的状态改为"已结束"的服务

	@param request 无用，为了兼容
	@param args dict类型
	"""
	print '\n\n'
	print '-*-' * 30
	print '[finish_promotion]'
	print 'start service @%s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print 'args: %s' % args
	promotion_id = str(args['id']).strip()
	promotion_type = args.get('type', None)
	if promotion_id != 0 and not promotion_id:
		print 'No promotion_id. Return directly'
		return

	promotion_ids = []
	should_process_all_promotions = False
	try:
		promotion_id = int(promotion_id)
		if promotion_id == 0:
			should_process_all_promotions = True
			promotion_ids.append(0)
		else:
			promotion_ids = [promotion_id]
	except:
		promotion_ids = promotion_id.split(',')

	if not promotion_ids:
		print 'No promotion_ids. Return directly'
		return

	if should_process_all_promotions:
		#处理全部促销
		now = datetime.today()
		id2promotion = dict([(promotion.id, promotion) for promotion in promotion_models.Promotion.objects.filter(status=promotion_models.PROMOTION_STATUS_STARTED, end_date__lte=now)])
		promotion_ids = id2promotion.keys()
		promotions = id2promotion.values()
		promotion_models.Promotion.objects.filter(id__in=promotion_ids).update(status=promotion_models.PROMOTION_STATUS_FINISHED)
		watchdog_info(u'将promotion(%s)状态改为PROMOTION_STATUS_FINISHED' % promotion_ids)
		#修改过期优惠券规则的库存
		coupon_rule_ids = []
		for promotion in promotions:
			if promotion.type == promotion_models.PROMOTION_TYPE_COUPON:
				coupon_rule_ids.append(promotion.detail_id)
		promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids).update(remained_count=0, is_active=False)
	else:
		if promotion_type == promotion_models.PROMOTION_TYPE_COUPON:
			promotion_models.Promotion.objects.filter(id__in=promotion_ids).update(status=promotion_models.PROMOTION_STATUS_DISABLE)
			promotion_detail_ids = [promotion.detail_id for promotion in promotion_models.Promotion.objects.filter(id__in=promotion_ids)]
			promotion_models.CouponRule.objects.filter(id__in=promotion_detail_ids).update(remained_count=0, is_active=False)
			watchdog_info(u'将promotion(%s)状态改为PROMOTION_STATUS_DISABLE' % promotion_ids)
		else:
			promotion_models.Promotion.objects.filter(id__in=promotion_ids).update(status=promotion_models.PROMOTION_STATUS_FINISHED)
			watchdog_info(u'将promotion(%s)状态改为PROMOTION_STATUS_FINISHED' % promotion_ids)

	product_ids = [r.product_id for r in promotion_models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)]
	products = list(mall_models.Product.objects.filter(id__in=product_ids))
	for product in products:
		key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (product.owner_id, product.id)
		print 'delete redis key %s' % key
		cache_util.delete_cache(key)

	cancel_order_for_promotion(promotion_ids)
	return "OK"
