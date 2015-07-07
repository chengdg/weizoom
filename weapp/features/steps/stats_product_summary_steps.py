# -*- coding: utf-8 -*-
"""
数据统计(BI)之商品概况分析的BDD steps

"""

__author__ = 'duhao'

from test import bdd_util
from behave import *
from django.test.client import Client

import json
from core import dateutil

@then(u"{user}获得商品概况数据")
def step_impl(context, user):
	start_date = bdd_util.get_date_str(context.date_dict['start_date'])
	end_date = bdd_util.get_date_str(context.date_dict['end_date'])

	url = '/stats/api/product_summary/?start_date=%s&end_date=%s' % (start_date, end_date)
	response = context.client.get(url)
	results = json.loads(response.content)
	actual = results['data']['item']

	expected_dict = {}
	for row in context.table:
		expected_dict[row['item']] = int(row['quantity'])

	expected = {}
	expected['buyer_count'] = expected_dict[u'购买总人数']
	expected['order_count'] = expected_dict[u'下单单量']
	expected['deal_product_count'] = expected_dict[u'总成交件数']

	bdd_util.assert_dict(expected, actual)
