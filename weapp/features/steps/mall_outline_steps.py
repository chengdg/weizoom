# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *


# @then(u"{user}能获取商铺首页的代发货订单列表")
# def step_impl(context, user):
# 	stock_infos = json.loads(context.text)
#
# 	url = '/mall2/outline/'
# 	response = context.client.get(url)
# 	actual = response.context['order_info']
#
# 	expected = json.loads(context.text)
# 	for orders in expected['orders_list']:
# 		orders['date'] = bdd_util.get_date(orders['date']).strftime('%Y-%m-%d')
# 		for order in orders['items']:
# 			order['final_price'] = order['order_money']
# 			del order['order_money']
#
# 	bdd_util.assert_dict(expected, actual)


@then(u"{user}能获取商铺首页的数量信息")
def step_impl(context, user):
	stock_infos = json.loads(context.text)

	url = '/mall2/outline/'
	response = context.client.get(url)
	actual = {
		"order_count_for_yesterday": response.context['order_count'],
		"order_money_for_yesterday": response.context['order_money'],
		"new_member_count": response.context['new_member_count'],
		"subscribed_member_count": response.context['subscribed_member_count'],
		"unread_message_count": response.context['unread_message_count']
	}

	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)

@then(u'{user}能获取店铺提醒信息')
def step_impl(context, user):
	url = '/mall2/outline/'
	response = context.client.get(url)
	shop_hint_data = response.context['shop_hint_data']
	actual = {
		'onshelf_product_count': shop_hint_data['onshelf_product_count'],
        'sellout_product_count': shop_hint_data['sellout_product_count'],
        'to_be_shipped_order_count': shop_hint_data['to_be_shipped_order_count'],
        'refunding_order_count': shop_hint_data['refunding_order_count'],
        'flash_sale_count': shop_hint_data['flash_sale_count'],
        'premium_sale_count': shop_hint_data['premium_sale_count'],
        'integral_sale_count': shop_hint_data['integral_sale_count'],
        'coupon_count': shop_hint_data['coupon_count'],
        'red_envelope_count': shop_hint_data['red_envelope_count']
	}

	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)