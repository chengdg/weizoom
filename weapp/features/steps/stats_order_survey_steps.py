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
#from util import dateutil as util_dateutil


@when(u"浏览'销售分析-订单概况'页面")
def step_impl(context):
	client = context.client
	context.response = client.get("/stats/order_summary/")
	data = context.response.context['jsons'] # 与render_to_response的Response对应
	print("data: {}".format(data))


@then(u"页面上的'筛选日期'")
def step_impl(context):
	print("text: {}".format(context.text))
	expected = json.loads(context.text)
	real = context.response.context['jsons'][0]['content'] # 实际数据

	expected['begin_time'] = bdd_util.escape_date_string(expected['begin_time'])
	context.tc.assertEquals(expected['begin_time'], real['start_time'])

	expected['end_time'] = bdd_util.escape_date_string(expected['end_time'])
	context.tc.assertEquals(expected['end_time'], real['end_time'])
