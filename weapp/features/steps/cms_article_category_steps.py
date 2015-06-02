# -*- coding: utf-8 -*-

import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.cms.models import *


@when(u"{user}添加文章分类")
def step_impl(context, user):
	client = context.client
	context.article_categories = json.loads(context.text)
	for article_category in context.article_categories:
		data = article_category  
		response = client.post('/cms/editor/category/create/', data)
		time.sleep(1)


@when(u"{user}已添加了文章分类")
def step_impl(context, user):
	client = context.client
	context.article_categories = json.loads(context.text)
	for article_category in context.article_categories:
		data = article_category  
		response = client.post('/cms/editor/category/create/', data)


@given(u"{user}已添加了文章分类")
def step_impl(context, user):
	context.execute_steps(u"when %s已添加了文章分类" % user)


# @when(u"{user}更新文章分类'{category_name}'为")
# def step_impl(context, user, category_name):
# 	client = context.client
# 	existed_product_category = ProductCategoryFactory(name=category_name)
# 	new_product_category = json.loads(context.text)
# 	data = {
# 		'name': new_product_category['name']
# 	}
# 	response = client.post('/mall/editor/productcategory/update/%d/' % existed_product_category.id, data)


# @when(u"{user}删除文章分类'{category_name}'")
# def step_impl(context, user, category_name):
# 	existed_product_category = ProductCategoryFactory(name=category_name)
# 	res = context.client.get('/mall/editor/productcategory/delete/%d/' % existed_product_category.id)


@then(u"{user}能获取文章分类列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/cms/api/categories/get/?version=1&sort_attr=-created_at&count_per_page=15&page=1')					
	data = json.loads(response.content)['data']
	expected = json.loads(context.text)
	actual = data['items']
	bdd_util.assert_list(expected, actual)


# @then(u"{user}能获取文章分类信息")
# def step_impl(context, user):
# 	actual = []
# 	for category in ProductCategory.objects.all().order_by('id'):
# 		actual.append({
# 			"name": category.name,
# 			"product_count": category.product_count
# 		})

# 	expected = json.loads(context.text)
# 	bdd_util.assert_list(expected, actual)
