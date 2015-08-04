# -*- coding: utf-8 -*-
# import json
# import time
# from datetime import datetime, timedelta

# from behave import *

# from test import bdd_util
# from features.testenv.model_factory import *

# from django.test.client import Client
# from mall.models import *


#######################################################################
# __process_product_model_property: 转换一个商品的规格属性数据
#######################################################################
# def __process_product_model_property(model_property, existed_model_property_id=None):
# 	data = {"name": model_property['name']}

# 	#处理类型
# 	type = model_property.get('type', None)
# 	if type == u'文字' or not type:
# 		data['type'] = 'text'
# 	else:
# 		data['type'] = 'image'

# 	#处理property value
# 	value_counter = -1
# 	for value in model_property['values']:
# 		cid = value_counter
# 		if 'original_name' in value:
# 			#是更改已有的property value，调整cid
# 			existed_property_value = ProductModelPropertyValue.objects.get(property_id=existed_model_property_id, name=value['original_name'], is_deleted=False)
# 			cid = existed_property_value.id

# 		if 'name' in value:
# 			key = 'value^name^%d' % cid
# 			data[key] = value['name']
# 		if 'image' in value:
# 			key = 'value^image^%d' % cid
# 			data[key] = value['image']

# 		if cid == value_counter:
# 			value_counter -= 1

# 	return data



#######################################################################
# __add_product_model_property: 添加一个商品规格属性
#######################################################################
# def __add_product_model_property(context, model_property):
# 	#data = __process_product_model_property(model_property)
# 	data = model_property
# 	response = context.client.post('/mall/api/product_model_property/create/', data)
# 	bdd_util.assert_api_call_success(response)
# 	property_id = json.loads(response.content)['data']

# 	#更新name
# 	post_data = {
# 		"id": property_id,
# 		"field": 'name',
# 		"name": data['name']
# 	}
# 	response = context.client.post('/mall/api/product_model_property/update/', post_data)
# 	bdd_util.assert_api_call_success(response)

# 	#更新type
# 	post_data = {
# 		"id": property_id,
# 		"field": 'type',
# 		"type": 'text'
# 	}
# 	type = data.get('type', None)
# 	if type == u'图片':
# 		post_data['type'] = 'image'
# 	response = context.client.post('/mall/api/product_model_property/update/', post_data)
# 	bdd_util.assert_api_call_success(response)

# 	#处理value
# 	for value in data['values']:
# 		if 'image' in value:
# 			value['pic_url'] = value['image']
# 		else:
# 			value['pic_url'] = ''
# 		value['id'] = property_id
# 		response = context.client.post('/mall/api/product_model_property_value/create/', value)
# 		bdd_util.assert_api_call_success(response)


# @given(u"{user}已添加商品规格")
# def step_impl(context, user):
# 	product_model_properties = json.loads(context.text)
# 	for property in product_model_properties:
# 		__add_product_model_property(context, property)


# @when(u"{user}添加商品规格")
# def step_impl(context, user):
# 	product_model_properties = json.loads(context.text)
# 	for property in product_model_properties:
# 		__add_product_model_property(context, property)


###########################################################################################
# __get_model_property_from_web_page: 从网页中获取model property
###########################################################################################
# def __get_model_property_from_web_page(context, property_name):
# 	model_property = ProductModelProperty.objects.get(owner_id=context.webapp_owner_id, name=property_name, is_deleted=False)
# 	url = '/mall/model_properties/get/'
# 	response = context.client.get(url)
# 	actual = {}
# 	model_properties = response.context['model_properties']
# 	model_property = filter(
# 							lambda x: x.id == model_property.id,
# 							model_properties)[0]
# 	# from pprint import pprint
# 	# print("*"*29, "model_property", "*"*29)
# 	# pprint(model_property)
# 	# print("*"*79)
# 	actual['name'] = model_property.name
# 	actual['type'] = u'图片' if model_property.type == PRODUCT_MODEL_PROPERTY_TYPE_IMAGE else u'文字'
# 	actual['values'] = []
# 	property_values = ProductModelPropertyValue.objects.filter(property_id=model_property.id, is_deleted=False)
# 	for property_value in property_values:
# 		actual['values'].append({
# 			"name": property_value.name,
# 			"image": property_value.pic_url
# 		})

# 	return actual


# @then(u"{user}能获取商品规格'{product_model_property_name}'")
# def step_impl(context, user, product_model_property_name):
# 	expected = json.loads(context.text)
# 	actual = __get_model_property_from_web_page(context, product_model_property_name)

# 	bdd_util.assert_dict(expected, actual)


# @then(u"{user}能获取商品规格列表")
# def step_impl(context, user):
# 	response = context.client.get('/mall/model_properties/get/')

# 	expected = json.loads(context.text)

# 	actual = []
# 	model_properties = response.context['model_properties']
# 	for model_property in model_properties:
# 		data = {
# 			"name": model_property.name,
# 			"type": u'图片' if model_property.type == PRODUCT_MODEL_PROPERTY_TYPE_IMAGE else u'文字'
# 		}
# 		data['values'] = []
# 		property_values = ProductModelPropertyValue.objects.filter(property_id=model_property.id, is_deleted=False)
# 		for property_value in property_values:
# 			data['values'].append({
# 				"name": property_value.name,
# 				"image": property_value.pic_url
# 			})
# 		actual.append(data)

# 	bdd_util.assert_list(expected, actual)



# @when(u"{user}更新商品规格'{product_model_property_name}'为")
# def step_impl(context, user, product_model_property_name):
# 	user_id = bdd_util.get_user_id_for(user)
# 	db_model_property = ProductModelProperty.objects.get(owner_id=user_id, name=product_model_property_name, is_deleted=False)
# 	property_id = db_model_property.id

# 	model_property = json.loads(context.text)

# 	#更新name
# 	data = {
# 		"id": property_id,
# 		"field": 'name',
# 		"name": model_property['name']
# 	}
# 	response = context.client.post('/mall/api/product_model_property/update/', data)
# 	bdd_util.assert_api_call_success(response)

# 	#更新type
# 	data = {
# 		"id": property_id,
# 		"field": 'type',
# 		"type": 'text'
# 	}
# 	type = model_property.get('type', None)
# 	if type == u'图片':
# 		data['type'] = 'image'
# 	response = context.client.post('/mall/api/product_model_property/update/', data)
# 	bdd_util.assert_api_call_success(response)

# 	#处理add_values
# 	for value in model_property.get('add_values', []):
# 		if 'image' in value:
# 			value['pic_url'] = value['image']
# 		else:
# 			value['pic_url'] = ''
# 		value['id'] = property_id
# 		response = context.client.post('/mall/api/product_model_property_value/create/', value)
# 		bdd_util.assert_api_call_success(response)

# 	#处理delete_values
# 	for value in model_property.get('delete_values', []):
# 		db_model_property_value = ProductModelPropertyValue.objects.get(property=db_model_property, name=value['name'], is_deleted=False)
# 		response = context.client.post('/mall/api/product_model_property_value/delete/', {'id': db_model_property_value.id})
# 		bdd_util.assert_api_call_success(response)


# @when(u"{user}删除商品规格'{product_model_property_name}'的值'{property_value}'")
# def step_impl(context, user, product_model_property_name, property_value):
# 	user_id = bdd_util.get_user_id_for(user)
# 	db_model_property = ProductModelProperty.objects.get(owner_id=user_id, name=product_model_property_name, is_deleted=False)
# 	db_model_property_value = ProductModelPropertyValue.objects.get(property=db_model_property, name=property_value, is_deleted=False)

# 	response = context.client.post('/mall/api/product_model_property_value/delete/', {'id': db_model_property_value.id})
# 	bdd_util.assert_api_call_success(response)


# @when(u"{user}删除商品规格'{product_model_property_name}'")
# def step_impl(context, user, product_model_property_name):
# 	user_id = bdd_util.get_user_id_for(user)
# 	db_model_property = ProductModelProperty.objects.get(owner_id=user_id, name=product_model_property_name, is_deleted=False)

# 	response = context.client.post('/mall/api/product_model_property/delete/', {'id': db_model_property.id})
# 	bdd_util.assert_api_call_success(response)
