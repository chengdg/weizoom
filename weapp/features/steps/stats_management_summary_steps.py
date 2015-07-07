#coding: utf8
"""
数据统计(BI)之销售订单分析的BDD steps

"""

__author__ = 'victor'

import json
#import time
from test import bdd_util
from market_tools.tools.activity.models import *

from behave import *
#from features.testenv.model_factory import *
from django.test.client import Client
#from market_tools.tools.delivery_plan.models import *

from core import dateutil
from utils import dateutil as util_dateutil


@when(u"浏览'经营概况'页面")
def step_impl(context):
	client = context.client
	context.response = client.get("/stats/management_summary/")
	#bdd_util.assert_api_call_success(context.response)
	#data = context.response.context['jsons'] # 与render_to_response的Response对应
	#print("data: {}".format(data))

@when(u"查询'店铺经营概况'")
def step_impl(context):
	client = context.client
	date_dict = context.date_dict[0]
	begin_date = bdd_util.get_date(date_dict['begin_date'])
	end_date = bdd_util.get_date(date_dict['end_date'])

	url = u'/stats/api/manage_summary/?design_mode=0&version=1&start_date={}&end_date={}&count_per_page=10&page=1&enable_paginate=1'.format(util_dateutil.date2string(begin_date), util_dateutil.date2string(end_date))
	context.response = client.get(url)
	bdd_util.assert_api_call_success(context.response)
	context.data = json.loads(context.response.content)['data']
	#print("json: {}".format(context.data))


@then(u'获得店铺经营概况数据')
def step_impl(context):
	print("json: {}".format(context.data))
	real = context.data['result']
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, real)
