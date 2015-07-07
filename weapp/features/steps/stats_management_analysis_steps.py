#coding: utf8
"""
数据统计(BI)之管理分析的BDD steps

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


@when(u'{user}查看微品牌页面')
def step_impl(context, user):
	# 获取EChart展示的数据
	context.response = context.client.get("/stats/api/brand_value/?id=1")
	#print("content: {}".format(context.response.content))
	results = json.loads(context.response.content)
	assert results.has_key('data')
	context.data = results['data']
	print("data: {}".format(context.data))


@then(u'微品牌的数据为')
def step_impl(context):
	expected_data = json.loads(context.text)
	expected = [e['value'] for e in expected_data]
	print("expected: {}".format(expected))
	real = context.data['series'][0]['data']
	print("real: {}".format(real))
	bdd_util.assert_list(expected, real)
