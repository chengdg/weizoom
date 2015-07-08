# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *

from webapp.modules.mall.pageobject.product_model_list_page import ProductModelListPage


#######################################################################
# __process_product_model_property: 转换一个商品的规格属性数据
#######################################################################
def __process_product_model_property(model_property, existed_model_property_id=None):
	data = {"name": model_property['name']}

	#处理类型
	type = model_property.get('type', None)
	if type == u'文字' or not type:
		data['type'] = PRODUCT_MODEL_PROPERTY_TYPE_TEXT
	else:
		data['type'] = PRODUCT_MODEL_PROPERTY_TYPE_IMAGE

	#处理property value
	value_counter = -1
	for value in model_property['values']:
		cid = value_counter
		if 'original_name' in value:
			#是更改已有的property value，调整cid
			existed_property_value = ProductModelPropertyValue.objects.get(property_id=existed_model_property_id, name=value['original_name'], is_deleted=False)
			cid = existed_property_value.id

		if 'name' in value:
			key = 'value^name^%d' % cid
			data[key] = value['name']
		if 'image' in value:
			key = 'value^image^%d' % cid
			data[key] = value['image']

		if cid == value_counter:
			value_counter -= 1

	return data



#######################################################################
# __add_product_model_property: 添加一个商品规格属性
#######################################################################
def __add_product_model_property(context, model_property):
	data = __process_product_model_property(model_property)
	response = context.client.post('/mall/editor/product_model_property/create/', data)



@when(u"{user}添加商品规格:ui")
def step_impl(context, user):
	product_model_list_page = ProductModelListPage(context.driver)
	product_model_list_page.load()

	product_model_properties = json.loads(context.text)
	for property in product_model_properties:
		edit_product_model_page = product_model_list_page.click_add_product_model_button()
		edit_product_model_page.edit_product_model(property)
		edit_product_model_page.submit()


@then(u"{user}能获取商品规格'{product_model_property_name}':ui")
def step_impl(context, user, product_model_property_name):
	product_model_list_page = ProductModelListPage(context.driver)
	product_model_list_page.load()

	edit_product_model_page = product_model_list_page.enter_edit_product_model_page(product_model_property_name)
	actual = edit_product_model_page.get_product_model()

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@then(u"{user}能获取商品规格列表:ui")
def step_impl(context, user):
	product_model_list_page = ProductModelListPage(context.driver)
	product_model_list_page.load()
	actual = product_model_list_page.get_product_models()

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual)



@when(u"{user}更新商品规格'{product_model_property_name}'为:ui")
def step_impl(context, user, product_model_property_name):
	product_model_list_page = ProductModelListPage(context.driver)
	product_model_list_page.load()

	property = json.loads(context.text)
	edit_product_model_page = product_model_list_page.enter_edit_product_model_page(product_model_property_name)
	edit_product_model_page.update_product_model(property)
	edit_product_model_page.submit()


@when(u"{user}删除商品规格'{product_model_property_name}'的值'{property_value}':ui")
def step_impl(context, user, product_model_property_name, property_value):
	product_model_list_page = ProductModelListPage(context.driver)
	product_model_list_page.load()

	edit_product_model_page = product_model_list_page.enter_edit_product_model_page(product_model_property_name)
	edit_product_model_page.delete_model_property(property_value)


@when(u"{user}删除商品规格'{product_model_property_name}':ui")
def step_impl(context, user, product_model_property_name):
	product_model_list_page = ProductModelListPage(context.driver)
	product_model_list_page.load()

	edit_product_model_page = product_model_list_page.enter_edit_product_model_page(product_model_property_name)
	edit_product_model_page.delete()
