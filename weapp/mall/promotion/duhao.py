# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime

from celery import task

from mall.promotion import models as promotion_models
from mall import models as mall_models
from modules.member import models as member_models
from utils import ding_util
from mall import module_api


from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource, paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall import export

from watchdog.utils import watchdog_alert

import utils
from django.conf import settings



VIRTUAL_ORDER_TYPE = [mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE]
# WESHOP_DING_GROUP_ID = '105507196'  #微众商城FT团队钉钉id
WESHOP_DING_GROUP_ID = '80035247'  #发消息测试群

def deliver_virtual_product(request, args):
	"""
	每隔一分钟自动发货一次

	@param request 无用，为了兼容
	@param args dict类型
	"""
	print 'start service virtual_product {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	#获取所有虚拟子订单
	order2products = mall_models.OrderHasProduct.objects.filter(
			order__status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
			order__type__in=VIRTUAL_ORDER_TYPE,
			order__origin_order_id__gt=0
		)

	oid2order = {}
	oid2product_id2count = {}
	for o2p in order2products:
		order = o2p.order
		product = o2p.product
		oid = order.id

		oid2order[oid] = o2p.order
		if not oid2product_id2count.has_key(oid):
			oid2product_id2count[oid] = {}
		oid2product_id2count[oid][product.id] = o2p.number

	print 'virtual order count:', len(oid2order)
	for oid in oid2product_id2count:
		can_update_order_status = True  #是否可以更改订单的发货状态
		print 'process order id:', oid
		order = oid2order[oid]

		#获取会员信息
		member = member_models.WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		if not member:
			message = u'获取member信息失败，订单id：%s,商品id：%d' % (order.order_id, product_id)
			print message
			ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
			continue

		product_id2count = oid2product_id2count[oid]
		for product_id in product_id2count:
			count = product_id2count[product_id]
			print '  process product id:%d, buy count:%d' % (product_id, count)
			virtual_products = promotion_models.VirtualProduct.objects.filter(product_id=product_id, is_finished=False)
			if virtual_products.count() > 0:
				virtual_product = virtual_products[0]

				#判断该订单里的这个商品是否已经被发过货了，如果发过则不重复发放，且can_update_order_status不变为False
				existed_records = promotion_models.VirtualProductHasCode.objects.filter(virtual_product=virtual_product, oid=order.id)
				if existed_records.count() > 0:
					message = u'该商品已经发过货，无需重复发货，订单id：%s,商品id：%d,福利卡券活动id：%d' % (order.order_id, product_id, virtual_product.id)
					print message
					ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
					continue

				#按id顺序发放
				codes = promotion_models.VirtualProductHasCode.objects.filter(virtual_product=virtual_product, status=promotion_models.CODE_STATUS_NOT_GET).order_by('id')

				_c = []
				for code in codes:
					if (not code.can_not_use) and len(_c) < count:
						_c.append(code)

				if len(_c) < count:
					can_update_order_status = False
					message = u'发放虚拟商品时库存不足，订单id：%s,商品id：%d,待发放：%d,库存：%d' % (order.order_id, product_id, count, len(_c))
					print message
					ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
					continue
				
				for code in _c:
					print '    deliver code:', code.code
					code.member_id = member.id
					code.get_time = datetime.now()
					code.oid = order.id
					code.order_id = order.order_id
					code.status = promotion_models.CODE_STATUS_GET
					code.save()
			else:
				can_update_order_status = False
				message = u'虚拟商品发货失败，商品没有关联福利卡券活动，订单id：%s,商品id：%d' % (order.order_id, product_id)
				print message
				ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

		if can_update_order_status:
			#更改订单状态，发货
			print u'订单发货：', order.order_id
			module_api.ship_order(order.order_id, '', '', u'系统', '', False, False)

	return 'OK {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class VirtualProducts(resource.Resource):
	app = 'mall2'
	resource = 'duhao'


	@login_required
	def get(request):
		"""
		浏览虚拟商品（福利卡券）列表
		"""
		deliver_virtual_product(None, None)
		c = RequestContext(request, {
			'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_VIRTUAL_PRODUCTS_NAV
		})

		return render_to_response('mall/editor/promotion/duhao.html', c)