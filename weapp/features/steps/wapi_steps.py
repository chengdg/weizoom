# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import re
from behave import given, then, when
#from features.testenv.model_factory import ProductFactory, ProductCategoryFactory

from test import bdd_util
from mall import models as mall_models
#from utils import mall_api
import wapi as wapi_resource
from utils import dateutil as utils_dateutil

PATTERN_VARIABLE = re.compile(r'^\$([A-Za-z_]+)\((.*?)\)\$$')

# 定义scenario中处理子函数

def _profunc_owner_id(param):
	# 将用户名转成owner_id
	return bdd_util.get_user_id_for(param)

def _profunc_category_id(param):
	# 将类名转成ID
	return mall_models.ProductCategory.objects.get(name=param).id

def _profunc_today_date(param):
	# 返回今天日期YYYY-MM-DD
	return utils_dateutil.date2string(utils_dateutil.now())


_PROCESS_FUNC_DICT = {
	'owner_id': _profunc_owner_id,
	'category_id': _profunc_category_id,
	'today_date': _profunc_today_date
}


def _process_param(params):
	"""
	将params中的参数做处理
	"""
	for key in params.keys():
		value = params[key]
		if isinstance(value, basestring):
			m = re.match(PATTERN_VARIABLE, value)
			if m:
				#print(m.group(1))
				func_name = m.group(1)
				param = m.group(2)
				func = _PROCESS_FUNC_DICT[func_name]
				new_value = func(param)
				params[key] = new_value
	return params


@when(u"访问WAPI:{app}/{resource}")
def step_add_category(context, app, resource):
	#client = context.client
	#uid = client.user.id

	params = json.loads(context.text)
	# 需要处理params
	params = _process_param(params)
	print("params: {}".format(params))
	
	context.data = wapi_resource.get(app, resource, params)
	print("context.data: {}".format(context.data))


@then(u"获得WAPI结果")
def step_impl(context):
	#client = context.client
	#uid = client.user.id
	data = context.data
	expected = _process_param(json.loads(context.text))
	bdd_util.assert_dict(expected, data)	
	#assert False

@then(u"获得WAPI列表结果")
def step_impl(context):
	#client = context.client
	#uid = client.user.id
	data = context.data
	expected = json.loads(context.text)
	for i in range(0, len(expected)):
		expected[i] = _process_param(expected[i])
	bdd_util.assert_list(expected, data)
