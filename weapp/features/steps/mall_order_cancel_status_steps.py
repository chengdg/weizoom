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
from mall.promotion.models import *
from core import dateutil

@given(u"{user}已有的会员")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()

	context.client = bdd_util.login(user)
	profile = context.client.user.profile
	webapp_id = context.client.user.profile.webapp_id

	context.members = json.loads(context.text)
	for member in context.members:
		_update_member_by_name(webapp_id, member)

def _update_member_by_name(webapp_id, member_data):
	webapp_user_name = member_data.get('name')
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	member.integral = member_data['integral']
	member.save()

@given(u"{user}添加优惠券")
def step_impl(context, user):
	user = context.client.user
	profile = context.client.user.profile
	webapp_id = context.client.user.profile.webapp_id

	context.coupons = json.loads(context.text)
	for coupon in context.coupons:
		_save_coupon(user, coupon)

def _save_coupon(user, coupon_data):
	coupon_price = coupon_data.get('coupon_price')
	rule = CouponRule.objects.create(
		owner=user,
		name=coupon_price,
		valid_days=120,
		money=coupon_price,
		count=1,
		remained_count=1,
		start_date=datetime.now(),
		end_date=datetime.now(),
	)
	Coupon.objects.create(
		owner=user,
		coupon_rule=rule,
		provided_time=datetime.now(),
		start_time=datetime.now(),
		expired_time=datetime.now() + timedelta(10),
		coupon_id=coupon_data.get('coupon_code'),
		money=coupon_price
	)

# @when(u"{webapp_user_name}取消订单'{order_id}'")
# def step_impl(context, webapp_user_name, order_id):
# 	id =  _get_order_by_order_id(order_id).id
# 	post_data = dict()
# 	post_data["woid"] = context.webapp_owner_id
# 	post_data["module"] = 'mall'
# 	post_data["target_api"] = 'order_status/update'
# 	post_data["order_id"] = id
# 	post_data["action"] = u'cancel-custom'
#
# 	url = '/webapp/api/project_api/call/'
# 	response = context.client.post(url, post_data)
# 	response_json = json.loads(response.content)
#
# 	if response_json['code'] == 200:
# 		context.created_order_id = id
# 	else:
# 		context.created_order_id = -1

def _get_order_by_order_id(order_id):
	try:
		return Order.objects.get(order_id=order_id)
	except:
		return None

# @then(u"{webapp_user_name}手机端获取订单'{order_id}'状态")
# def step_impl(context, webapp_user_name, order_id):
# 	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (context.webapp_owner_id, order_id)
# 	response = context.client.get(bdd_util.nginx(url), follow=True)
#
# 	actual_order = response.context['order']
# 	actual_order.order_no = actual_order.order_id
# 	actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
#
# 	expected = json.loads(context.text)
#
# 	bdd_util.assert_dict(expected, actual_order)
#
# @then(u"{user}后端订单状态改变为")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
#
# 	context.client = bdd_util.login(user)
# 	profile = context.client.user.profile
# 	webapp_id = context.client.user.profile.webapp_id
#
# 	expected = json.loads(context.text)
#
# 	order_id = _get_order_by_order_id(expected['order_no']).id
# 	response = context.client.get('/mall/order_detail/get/?order_id=%d' % order_id)
#
# 	order = response.context['order']
# 	actual_order = dict()
# 	actual_order['order_no'] = order.order_id
# 	actual_order['status'] = ORDERSTATUS2TEXT[order.status]
#
# 	bdd_util.assert_dict(expected, actual_order)

# @then(u"{user}后端获取商品库存")
# def step_impl(context, user):
# 	profile = context.client.user.profile
# 	webapp_id = context.client.user.profile.webapp_id

# 	expected = json.loads(context.text)

# 	product_id = _get_product_by_name(expected['name']).id
# 	response = context.client.get('/mall/product/update/?id=%s' % product_id)

# 	product = response.context['product']
# 	actual_product = dict()
# 	actual_product['name'] = product.name
# 	actual_product['stocks'] = product.stocks

# 	bdd_util.assert_dict(expected, actual_product)

def _get_product_by_name(name):
	try:
		return Product.objects.get(name=name)
	except:
		return None

@then(u"{user}获取优惠券'{coupon_id}'状态")
def step_impl(context, user, coupon_id):
	expected = json.loads(context.text)

	coupon = _get_coupon_by_coupon_id(coupon_id)
	actual_product = dict()
	actual_product['coupon_code'] = coupon.coupon_id
	actual_product['coupon_status'] = _get_coupon_status_by(coupon)

	bdd_util.assert_dict(expected, actual_product)

def _get_coupon_by_coupon_id(coupon_id):
	try:
		return Coupon.objects.get(coupon_id=coupon_id)
	except:
		return None

def _get_coupon_status_by(coupon):
	STATUS = {
		COUPON_STATUS_UNUSED: u'未使用',
		COUPON_STATUS_USED: u'已使用',
		COUPON_STATUS_EXPIRED: u'已过期',
		COUPON_STATUS_DISCARD: u'作废'
	}
	return STATUS[coupon.status]

@then(u"{webapp_user_name}获取积分数值")
def step_impl(context, webapp_user_name):
	expected = json.loads(context.text)

	profile = context.client.user.profile
	member = bdd_util.get_member_for(webapp_user_name, profile.webapp_id)
	actual_data = dict()
	actual_data['integral'] = str(member.integral)

	bdd_util.assert_dict(expected, actual_data)
