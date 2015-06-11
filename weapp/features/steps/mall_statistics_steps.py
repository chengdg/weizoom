# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *


@then(u"{user}能获取'{days}'购买趋势")
def step_impl(context, user, days):
	if u'天' in days:
		days = days[:-1]

	url = '/mall/api/purchase_trend/get/?days=%s' % days
	response = context.client.get(url)
	data = json.loads(response.content)['data']
	dates = data['xAxis']['data']
	product_counts = data['series'][0]['data']
	money_list = data['series'][1]['data']
	date2info = {}
	for i, date in enumerate(dates):
		date2info[date] = {
			"product_count": product_counts[i],
			"money": money_list[i]
		}
	actual = date2info

	date2info = {}
	for row in context.table:
		date = bdd_util.get_date(row['date']).strftime('%Y-%m-%d')
		date2info[date] = {
			"product_count": int(row['product_count']),
			"money": float(row['money'])
		}
	expected = date2info

	bdd_util.assert_dict(expected, actual)


@then(u"{user}能获取'{days}'页面访问趋势")
def step_impl(context, user, days):
	if u'天' in days:
		days = days[:-1]

	url = '/mall/api/visit_daily_trend/get/?days=%s' % days
	response = context.client.get(url)
	data = json.loads(response.content)['data']
	dates = data['xAxis']['data']
	pvs = data['series'][0]['data']
	uvs = data['series'][1]['data']
	date2info = {}
	for i, date in enumerate(dates):
		date2info[date] = {
			"pv": pvs[i],
			"uv": uvs[i]
		}
	actual = date2info

	date2info = {}
	for row in context.table:
		date = bdd_util.get_date(row['date']).strftime('%Y-%m-%d')
		date2info[date] = {
			"pv": int(row['pv']),
			"uv": int(row['uv'])
		}
	expected = date2info

	bdd_util.assert_dict(expected, actual)