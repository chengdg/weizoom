# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from behave import given, then, when
#from features.testenv.model_factory import ProductFactory, ProductCategoryFactory

from test import bdd_util
from mall import models as mall_models
#from utils import mall_api
import wapi as wapi_resource
import re


PATTERN_VARIABLE = re.compile(r'^\$(.+?)\$$')

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
				variable = m.group(1)
				if key == 'oid':
					value = bdd_util.get_user_id_for(variable)
				elif key == 'category_id':
					obj = mall_models.ProductCategory.objects.get(name=variable)
					value = obj.id
				params[key] = value
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
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, data)	
	#assert False


@then(u"获得WAPI列表结果")
def step_impl(context):
	#client = context.client
	#uid = client.user.id
	data = context.data
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, data)
