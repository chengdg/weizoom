# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.mall.models import *


@then(u"{user}能获取商铺首页的代发货订单列表")
def step_impl(context, user):
	stock_infos = json.loads(context.text)

	url = '/mall/outline/get/'
	response = context.client.get(url)
	actual = response.context['order_info']

	expected = json.loads(context.text)
	for orders in expected['orders_list']:
		orders['date'] = bdd_util.get_date(orders['date']).strftime('%Y-%m-%d')
		for order in orders['items']:
			order['final_price'] = order['order_money']
			del order['order_money']

	bdd_util.assert_dict(expected, actual)


@then(u"{user}能获取商铺首页的数量信息")
def step_impl(context, user):
	stock_infos = json.loads(context.text)

	url = '/mall/outline/get/'
	response = context.client.get(url)
	print 'jz-----', response.context
	outline_counts = response.context['outline_counts']
	actual = {
		"order_count_for_yesterday": outline_counts[0]['count'],
		"order_money_for_yesterday": outline_counts[1]['count'],
		"member_count_for_yesterday": outline_counts[2]['count'],
		"total_member_count": outline_counts[3]['count']
	}

	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)

