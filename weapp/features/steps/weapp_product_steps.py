# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from product.models import Product
from market_tools import ToolModule

@When(u"{user}添加产品")
def step_impl(context, user):
	product = json.loads(context.text)

	data = {}
	data['product_id'] = '-1'
	data['name'] = product['name']
	data['price'] = product['price']
	data['footer'] = product['footer']
	data['remark'] = product['remark']
	data['max_mall_product_count'] = '10000'

	market_tools = product['market_tools']
	for tool_module in ToolModule.all_tool_modules():
		if tool_module.settings.TOOL_NAME in market_tools:
			model_value = 'market_tool_%s' %(tool_module.module_name)
			data[model_value] = tool_module.module_name
	data['webapp_1'] = "1"
	data['webapp_2'] = "2"
	data['webapp_3'] = "3"
	data['webapp_4'] = "4"

	url = '/product/product/add/'
	context.client.post(url, data)


@Then(u"{user}可以获取产品{product_name}")
def step_impl(context, user, product_name):
	expected = json.loads(context.text)

	product = Product.objects.get(name=product_name)
	actual = {}
	actual['name'] = product.name
	actual['price'] = product.price
	actual['footer'] = product.footer

	market_tool_modules = product.market_tool_modules.split(',')
	market_tool_module_values = []
	for tool_module in ToolModule.all_tool_modules():
		if tool_module.module_name in market_tool_modules:
			market_tool_module_values.append(tool_module.settings.TOOL_NAME)
	actual['market_tools'] = market_tool_module_values
	actual['remark'] = product.remark
	bdd_util.assert_dict(expected, actual)


@When(u"{user}编辑产品{product_name}")
def step_impl(context, user, product_name):
	p = Product.objects.get(name=product_name)

	product = json.loads(context.text)

	data = {}
	data['product_id'] = p.id
	data['name'] = product['name']
	data['price'] = product['price']
	data['footer'] = product['footer']
	data['remark'] = product['remark']
	data['max_mall_product_count'] = '10000'

	market_tools = product['market_tools']
	for tool_module in ToolModule.all_tool_modules():
		if tool_module.settings.TOOL_NAME in market_tools:
			model_value = 'market_tool_%s' %(tool_module.module_name)
			data[model_value] = tool_module.module_name
	data['webapp_1'] = "1"
	data['webapp_2'] = "2"
	data['webapp_3'] = "3"
	data['webapp_4'] = "4"

	url = '/product/product/add/'
	context.client.post(url, data)