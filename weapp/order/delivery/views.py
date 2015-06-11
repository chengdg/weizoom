# -*- coding: utf-8 -*-

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from order.account.order_decorators import project_freight_required

from mall.models import *
from tools.regional.views import get_str_value_by_string_ids
from mall.promotion.models import Coupon
from mall import module_api as mall_api

FREIGHT_NAV_NAME = 'freight-waybill'

@project_freight_required
def get_orders(request):
	c = RequestContext(request, {
		'nav_name': FREIGHT_NAV_NAME,
		'freight_user': request.freight_user
	})
	return render_to_response('waybill_list.html', c)


@project_freight_required
def show_order(request):
	order_id = request.GET.get('order_id', None)
	order = None
	coupon = None
	if order_id is not None:
		order = Order.objects.get(order_id=order_id)
		order_has_products = OrderHasProduct.objects.filter(order=order)

		# 商品总数量
		order_product_total_number = 0
		for order_has_product in order_has_products:
			order_product_total_number += order_has_product.number
		order.number = order_product_total_number

		#处理订单关联的优惠券
		coupon =  None
		coupons = Coupon.objects.filter(id=order.coupon_id)
		if coupons.count() > 0:
			coupon =  coupons[0]

		#获得订单关联的商品集合
		# product_ids = []
		# product_infos = []
		# order_product_relations = list(OrderHasProduct.objects.filter(order_id=order.id))
		# for relation in order_product_relations:
		# 	product_ids.append(relation.product_id)
		# 	product_infos.append({
		# 		'count': relation.number, #商品数量
		# 		'id': relation.product_id, #商品id
		# 		'total_price': relation.total_price #商品总价
		# 	})
		# id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

		# product_items = []
		# for product_info in product_infos:
		# 	product_id = product_info['id']
		# 	product = id2product[product_id]
		# 	product_items.append({
		# 		'name': product.name,
		# 		'thumbnails_url': product.thumbnails_url,
		# 		'count': product_info['count'],
		# 		'total_price': '%.2f' % product_info['total_price']
		# 	})
		order.products = mall_api.get_order_products(order.id)

		order.area = get_str_value_by_string_ids(order.area)

	c = RequestContext(request, {
		'nav_name': FREIGHT_NAV_NAME,
		'order': order,
		'is_order_not_payed': (order.status == ORDER_STATUS_NOT),
		'coupon': coupon,
		'freight_user': request.freight_user
	})
	return render_to_response('detail_waybill.html', c)
