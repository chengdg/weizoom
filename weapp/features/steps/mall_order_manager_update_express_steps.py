# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from tools.express import util as express_util
from modules.member.models import WebAppUser

# @given(u"{user}已有的订单")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	profile = context.client.user.profile
# 	webapp_id = context.client.user.profile.webapp_id
#
# 	context.orders = json.loads(context.text)
# 	for order in context.orders:
# 		_set_order_dict(order, profile)
#
# def _set_order_dict(order, profile):
# 	"""
# 	order -> {
# 		'status':
# 		'logistics':
# 		'type':
# 		'methods_of_payment':
# 		'member':
# 		'order_no':
# 		'number':
# 		'integral':
# 		'ship_name':
# 		'ship_tel':
# 		'order_time':
# 		'products':
#
# 	}
# 	"""
# 	status = _get_status_by_name(order.get('status'))
# 	express_value = express_util.get_value_by_name(order.get('logistics'))
# 	type = _get_type_by_name(order.get('type'))
# 	pay_interface_type = _get_paytype_by_name(order.get('methods_of_payment'))
#
# 	webapp_user_id = 1
# 	if order.get('member'):
# 		webapp_user_name = order.get('member')
# 		member = bdd_util.get_member_for(webapp_user_name, profile.webapp_id)
# 		try:
# 			webapp_user_id = WebAppUser.objects.get(member_id=member.id).id
# 		except:
# 			pass
#
# 	order_model = OrderFactory(
# 		order_id=order.get('order_no'),
# 		express_company_name=express_value,
# 		express_number=order.get('number', ''),
# 		status=status,
# 		webapp_id=profile.webapp_id,
# 		type=type,
# 		pay_interface_type=pay_interface_type,
# 		integral=order.get('integral', 0),
# 		webapp_user_id=webapp_user_id,
# 		ship_name=order.get('ship_name', u'收货人'),
# 		ship_tel=order.get('ship_tel', u'1333333333')
# 	)
# 	order_model.product_price = 0
# 	if order.get('order_time'):
# 		order_model.created_at = order.get('order_time')
# 		order_model.save()
#
# 	if order.get('sources') == u"商城":
# 		order_model.order_source = ORDER_SOURCE_WEISHOP
#
# 	if order.get('products'):
# 		for product_data in order.get('products'):
# 			product = Product.objects.get(name=product_data.get('name'))
# 			product.stocks = product.stocks - product_data.get('count')
# 			product.save()
#
# 			model = product_data.get('model', None)
# 			model_name = None
# 			# TODO wan shan gui ge
# 			if model:
# 				value = ProductModelPropertyValue.objects.get(name=model)
# 				model_name = '%s:%s' % (value.property_id, value.id)
# 			else:
# 				model_name = 'standard'
#
# 			product_model = ProductModel.objects.get(product_id=product.id, name=model_name)
#
# 			count = product_data.get('count', None)
# 			if not count:
# 				count = 1
# 			count = int(count)
#
# 			order_model.product_price += product_model.price * count
#
# 			OrderHasProduct.objects.create(
# 				order=order_model,
# 				product=product,
# 				product_name=product.name,
# 				product_model_name=model_name,
# 				price=product_model.price,
# 				total_price=product_model.price * count,
# 				number= count
# 			)
# 			# else:
# 			# 	OrderHasProduct.objects.create(
# 			# 		order=order_model,
# 			# 		product=product,
# 			# 		product_name=product.name,
# 			# 		product_model_name='standard',
# 			# 		price=product.price,
# 			# 		total_price=product.price,
# 			# 		number=product_data.get('count')
# 			# 	)
# 	order_model.final_price = order_model.product_price
# 	order_model.save()
# 	if order.get('integral'):
# 		member.integral = member.integral - order.get('integral')
# 		member.save()
#
# def _get_paytype_by_name(payment_name):
# 	for i in PAYTYPE2NAME:
# 		if PAYTYPE2NAME[i] == payment_name:
# 			return i
# 	return 0
#
# def _get_type_by_name(type_name):
# 	for i in ORDER_TYPE2TEXT:
# 		if ORDER_TYPE2TEXT[i] == type_name:
# 			return i
# 	return 0
#
# def _get_status_by_name(status_name):
# 	for i in STATUS2TEXT:
# 		if STATUS2TEXT[i] == status_name:
# 			return i
# 	return 0
#
# @When(u"{user}通过后台管理系统对'{order_id}'的物流信息进行修改")
# def step_impl(context, user, order_id):
# 	order = json.loads(context.text)
# 	express_value = express_util.get_value_by_name(order['logistics'])
# 	data_order_id = _get_order_by_order_id(order['order_no']).id
#
# 	url = '/mall/api/order_delivery/update/?order_id={}&express_company_name={}&express_number={}&leader_name=&is_update_express=true&leader_name={}'.format(
# 			data_order_id,
# 			express_value,
# 			order['number'],
# 			'aa'
# 		)
# 	response = context.client.get(bdd_util.nginx(url))
#
# def _get_order_by_order_id(order_id):
# 	try:
# 		return Order.objects.get(order_id=order_id)
# 	except:
# 		return None
#
# @then(u"{webapp_user_name}在webapp查看'{order_id}'的物流信息")
# def step_impl(context, webapp_user_name, order_id):
# 	expected_order = json.loads(context.text)
#
# 	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (context.webapp_owner_id, order_id)
# 	response = context.client.get(bdd_util.nginx(url), follow=True)
# 	actual_order = response.context['order']
# 	actual_order = {
# 		'order_no': actual_order.order_id,
# 		'logistics': express_util.get_name_by_value(actual_order.express_company_name),
# 		'number': actual_order.express_number,
# 		'status': ORDERSTATUS2TEXT[actual_order.status]
# 	}
#
# 	bdd_util.assert_dict(expected_order, actual_order)
#
