# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.mall.models import *


@given(u"{user}已添加商品分类")
def step_impl(context, user):
	# user = UserFactory(username=user)
	# context.product_categories = json.loads(context.text)
	# for product_category in context.product_categories:
	# 	ProductCategoryFactory(name=product_category['name'], owner=user)
	client = context.client
	context.product_categories = json.loads(context.text)
	for product_category in context.product_categories:
		data = product_category
		response = client.post('/mall/api/product_category/create/', data)


@when(u"{user}添加商品分类")
def step_impl(context, user):
	client = context.client
	product_categories = json.loads(context.text)
	for product_category in product_categories:
		data = product_category
		response = client.post('/mall/api/product_category/create/', data)
		time.sleep(1)


@when(u"{user}更新商品分类'{category_name}'为")
def step_impl(context, user, category_name):
	client = context.client
	existed_product_category = ProductCategoryFactory(name=category_name)
	new_product_category = json.loads(context.text)
	data = {
		'id': existed_product_category.id,
		'name': new_product_category['name']
	}
	response = client.post('/mall/api/product_category/update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品分类'{category_name}'")
def step_impl(context, user, category_name):
	existed_product_category = ProductCategoryFactory(name=category_name)
	data = {
		'id': existed_product_category.id
	}
	response = context.client.post('/mall/api/product_category/delete/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}从商品分类'{category_name}'中删除商品'{product_name}'")
def step_impl(context, user, category_name, product_name):
	existed_product_category = ProductCategoryFactory(name=category_name)
	existed_product = Product.objects.get(name=product_name)
	data = {
		'category_id': existed_product_category.id,
		'product_id': existed_product.id
	}
	response = context.client.post('/mall/api/product_in_category/delete/', data)
	bdd_util.assert_api_call_success(response)


@then(u"{user}能获得商品分类'{category_name}'的可选商品集合为")
def step_impl(context, user, category_name):
	existed_product_category = ProductCategoryFactory(name=category_name)
	response = context.client.get('/mall/api/category_products/get/?id={}'.format(existed_product_category.id))

	actual = json.loads(response.content)['data']['items']
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u"{user}向商品分类'{category_name}'中添加商品")
def step_impl(context, user, category_name):
	existed_product_category = ProductCategoryFactory(name=category_name)

	product_names = json.loads(context.text)
	products = Product.objects.filter(name__in=product_names)
	product_ids = [product.id for product in products]

	data = {
		"id": existed_product_category.id,
		"name": existed_product_category.name,
		"product_ids[]": product_ids
	}

	response = context.client.post('/mall/api/product_category/update/', data)


@then(u"{user}能获取商品分类列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/mall/product_categories/get/')
	actual = response.context['product_categories']
	#data = json.loads(response.content)['data']
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@then(u"{user}能获取商品分类信息")
def step_impl(context, user):
	actual = []
	for category in ProductCategory.objects.all().order_by('id'):
		actual.append({
			"name": category.name,
			"product_count": category.product_count
		})

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)
