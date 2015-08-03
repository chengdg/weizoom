# -*- coding: utf-8 -*-
"""@package cache.order_cache
订单统计数据的缓存接口

BDD feature: `user_center_cache.feature`


"""
from __future__ import absolute_import
from mall.models import *
from mall import models as mall_models

from utils import cache_util
from django.db.models import signals
from weapp.hack_django import post_update_signal
from django.core.exceptions import ObjectDoesNotExist
import cache

__author__ = 'victor'


def get_count_of_unfinished_product_review_picture(webapp_user_id):
    '''

    返回webapp_user已完成订单中， 未完成晒图的商品数量


    '''
    count = 0
    # 得到用户所有已完成订单
    orders = mall_models.Order.objects.filter(webapp_user_id=webapp_user_id, status=mall_models.ORDER_STATUS_SUCCESSED)

    # 得到用户所以已完成订单中的商品order_has_product.id列表
    orderIds = [order.id for order in orders]
    order_has_product_list_ids = []
    for i in mall_models.OrderHasProduct.objects.filter(order_id__in=orderIds):
        order_has_product_list_ids.append(i.id)

    # 得到用户已晒图的商品order_has_product.id列表
    prp = set()
    for i in mall_models.ProductReviewPicture.objects.filter(order_has_product_id__in=order_has_product_list_ids):
        prp.add(i.order_has_product_id)

    count = len(order_has_product_list_ids) - len(prp)

    return count


def _get_order_stats_fromdb(cache_key, webapp_user_id):
	"""
	从数据获取订单统计数据
	"""
	def inner_func():
		#print "in get_user_product_from_db.inner_func()"
		try:
			# TODO: 需要优化：一次SQL，获取全部数据
			stats = {
				"total_count": Order.objects.filter(webapp_user_id=webapp_user_id).count(),
				"not_paid": Order.objects.filter(webapp_user_id=webapp_user_id, status=ORDER_STATUS_NOT).count(),
				"not_ship_count": Order.objects.filter(webapp_user_id=webapp_user_id, status=ORDER_STATUS_PAYED_NOT_SHIP).count(),
				"shiped_count": Order.objects.filter(webapp_user_id=webapp_user_id, status=ORDER_STATUS_PAYED_SHIPED).count(),
				"review_count": get_count_of_unfinished_product_review_picture(webapp_user_id),
			}
			ret = {
				'keys': [cache_key],
				'value': stats
			}
			return ret
		except:
			#print '%s (%s)' % (e.message, type(e))
			return None
	return inner_func


def get_order_stats_cache_key(webapp_user_id):
	"""
	订单统计数据Redis key
	"""
	return "webapp_order_stats_{wo:%d}" % (webapp_user_id)



def get_order_stats(webapp_user_id):
	"""
	获取订单的统计数据

	@param webapp_user_id  webapp_user_id

	缓存的key ：webapp_order_stats_{wo:`<webapp_user_id>`}

	缓存的数据：

	- 总订单数
	- 待支付订单数

	@note 缓存失效条件：订单统计数据的缓存会在以下情况失效

	- Order.save的时候会由信号触发回调函数 `update_webapp_order_cache()`，导致订单对应的 `webapp_user_id` 用户订单统计数据失效。
	"""

	# 借助缓存
	key = get_order_stats_cache_key(webapp_user_id)
	stats = cache_util.get_from_cache(key, _get_order_stats_fromdb(key, webapp_user_id))
	if stats is not None:
		return (stats["total_count"], stats["not_paid"], stats["not_ship_count"], stats["shiped_count"], stats["review_count"])
	else:
		# 总订单数
		history_order_count = Order.objects.filter(webapp_user_id=webapp_user_id).count()
		# "待支付"订单数量
		not_payed_order_count = Order.objects.filter(webapp_user_id=webapp_user_id, status=ORDER_STATUS_NOT).count()
		# "待发货"订单数量
		not_ship_order_count = Order.objects.filter(webapp_user_id=webapp_user_id, status=ORDER_STATUS_PAYED_NOT_SHIP).count()
		# "已发货"订单数量
		shiped_order_count = Order.objects.filter(webapp_user_id=webapp_user_id, status=ORDER_STATUS_PAYED_SHIPED).count()
		# "待评价" 订单数量
		review_count = get_count_of_unfinished_product_review_picture(webapp_user_id)

		return (history_order_count, not_payed_order_count, not_ship_order_count, shiped_order_count, review_count)


def update_webapp_order_cache(instance, **kwargs):
	"""
	Order.save时触发信号回调函数

	@param instance Order的实例
	@param kwargs   其他参数，包括'sender'、'created'、'signal'、'raw'、'using'

	当在Django有Order.save的操作时会触发此函数。
	如果instance是有效的Order，则取将Order.webapp_user_id对应用户的订单数据缓存删除。

	"""
	#print("in update_webapp_order_cache(), kwargs: %s" % kwargs)
	if isinstance(instance, Order):
		webapp_user_id = instance.webapp_user_id
	else:
		from itertools import chain
		instances = chain(instance)
		for order in instances:
			webapp_user_id = order.webapp_user_id
			if webapp_user_id:
				try:
					key = get_order_stats_cache_key(webapp_user_id)
					cache_util.delete_cache(key)
				except:
					pass

	return


"""
注册signal: 当Order出现save操作时，触发update_webapp_order_cache()
"""
post_update_signal.connect(update_webapp_order_cache,
	sender=Order, dispatch_uid="order.update")
signals.post_save.connect(update_webapp_order_cache,
	sender=Order, dispatch_uid="order.save")


def update_webapp_order_by_review_picture_cache(instance, **kwargs):
	if hasattr(cache, 'request'):
		webapp_user_id = cache.request.webapp_user.id
		try:
			key = get_order_stats_cache_key(webapp_user_id)
			cache_util.delete_cache(key)
		except:
			pass

signals.post_save.connect(update_webapp_order_by_review_picture_cache,
	sender=ProductReviewPicture, dispatch_uid="productReviewPicture.save")
