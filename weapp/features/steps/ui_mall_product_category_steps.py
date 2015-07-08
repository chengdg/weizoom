# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from mall.models import *
from webapp.modules.mall.pageobject.category_list_page import CategoryListPage


@when(u"{user}添加商品分类:ui")
def step_impl(context, user):
	category_list_page = CategoryListPage(context.driver)
	category_list_page.load()

	product_categories = json.loads(context.text)
	for product_category in product_categories:
		category_name = product_category['name']
		category_list_page = CategoryListPage(context.driver)
		edit_category_page = category_list_page.click_add_category_button()
		edit_category_page.add_category(category_name)
		edit_category_page.submit()


@when(u"{user}更新商品分类'{category_name}'为:ui")
def step_impl(context, user, category_name):
	client = context.client
	existed_product_category = ProductCategoryFactory(name=category_name)
	new_product_category = json.loads(context.text)
	data = {
		'name': new_product_category['name']
	}
	response = client.post('/mall/editor/productcategory/update/%d/' % existed_product_category.id, data)


@when(u"{user}删除商品分类'{category_name}':ui")
def step_impl(context, user, category_name):
	existed_product_category = ProductCategoryFactory(name=category_name)
	res = context.client.get('/mall/editor/productcategory/delete/%d/' % existed_product_category.id)


@then(u"{user}能获取商品分类列表:ui")
def step_impl(context, user):
	category_list_page = CategoryListPage(context.driver)
	category_list_page.load()
	actual = category_list_page.get_categories()

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


# @then(u"{user}能获取商品分类信息:ui")
# def step_impl(context, user):
# 	actual = []
# 	for category in ProductCategory.objects.all().order_by('id'):
# 		actual.append({
# 			"name": category.name,
# 			"product_count": category.product_count
# 		})

# 	expected = json.loads(context.text)
# 	bdd_util.assert_list(expected, actual)
