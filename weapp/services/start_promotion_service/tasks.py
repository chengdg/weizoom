#coding:utf8
"""@package services.start_promotion_service.tasks
start_promotion_service 的Celery task实现

"""
from django.conf import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info
from datetime import datetime

from mall.promotion import models as promotion_models
from mall import models as mall_models

from celery import task
from utils import cache_util


@task
def start_promotion(request0, args):
	"""
	将promotion的状态改为"进行中"的服务

	@param request 无用，为了兼容
	@param args dict类型
	"""
	# 构造request对象
	print '\n\n'
	print '-*-' * 30
	print 'start service @%s', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	promotion_id = str(args['id']).strip()
	if not promotion_id:
		print 'No promotion_id. Return directly'
		return

	if int(promotion_id) == 0:
		#处理全部促销
		now = datetime.today()
		promotion_ids = [promotion.id for promotion in promotion_models.Promotion.objects.filter(status=promotion_models.PROMOTION_STATUS_NOT_START, start_date__lte=now)]
		promotion_models.Promotion.objects.filter(id__in=promotion_ids).update(status=promotion_models.PROMOTION_STATUS_STARTED)
		watchdog_info('将promotion(%s)状态改为PROMOTION_STATUS_STARTED' % promotion_ids)
	else:
		promotion_models.Promotion.objects.filter(id=promotion_id).update(status=promotion_models.PROMOTION_STATUS_STARTED)
		promotion_ids = [promotion_id]
		watchdog_info('将promotion(%s)状态改为PROMOTION_STATUS_STARTED' % promotion_id)
	
	product_ids = [r.product_id for r in promotion_models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)]
	products = list(mall_models.Product.objects.filter(id__in=product_ids))
	for product in products:
		key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (product.owner_id, product.id)
		print 'delete redis key %s' % key
		cache_util.delete_cache(key)
		
	return "OK"
