# -*- coding: utf-8 -*-

import json

from core.jsonresponse import JsonResponse, create_response
from mall.models import Order, OrderHasProduct, WeizoomMallHasOtherMallProductOrder
from webapp.modules.mall import request_util, request_api_util
from apps.register import mobile_api

from weshop import settings


@mobile_api(resource='result_notify', action='pay')
def pay_result_notify(request, webapp_id):
	return request_api_util.pay_result_notify(request, webapp_id)


########################################################################
#save_order: 保存订单
########################################################################
@mobile_api(resource='order', action='save')
def save_order(request):
	request.integral_not_limit = True
	response = request_api_util.save_order(request)
	new_response = json.loads(response.content)
	data = new_response['data']
	if data.get('id', None):
		order_id = data['id']
		order = Order.objects.get(id=order_id)
		if WeizoomMallHasOtherMallProductOrder.objects.filter(order_id=order.order_id).count():
			product_price = 0
			for product in OrderHasProduct.objects.filter(order_id=order_id):
				product.price = round(product.price * settings.WEIZOOM_PRICE, 0)
				product.total_price = product.price * product.number
				product_price += product.total_price
				product.save()

			order.product_price = product_price
			# 微众商城没有会员折扣
			order.member_grade_discounted_money = product_price
			order.final_price = product_price + order.postage - order.coupon_money - order.integral_money
			if order.final_price > 0:
				order.status = 0
			order.save()

			data['final_price'] = order.final_price
			response = create_response(200)
			response.data = data
			response = response.get_response()
	return response


########################################################################
# save_address: 保存订单详情
########################################################################
@mobile_api(resource='address', action='save')
def save_address(request):
	return request_api_util.save_address(request)