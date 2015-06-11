# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util

from mall.models import *
from webapp.modules.mall.pageobject.product_list_page import ProductListPage
from webapp.modules.mall.pageobject.order_list_page import OrderListPage


@when(u"{user}添加商品:ui")
def step_impl(context, user):
	products = json.loads(context.text)
	url2uploaded_url = {}
	for product in products:
		product_list_page = ProductListPage(context.driver)
		product_list_page.load()
		edit_product_page = product_list_page.click_add_product_button()
		edit_product_page.submit_product(product, url2uploaded_url)


@when(u"{user}更新商品'{product_name}':ui")
def step_impl(context, user, product_name):
	product = json.loads(context.text)
	product_list_page = ProductListPage(context.driver)
	product_list_page.load()
	edit_product_page = product_list_page.enter_edit_product_page(product_name)
	edit_product_page.update_product(product)


@when(u"{user}删除后台商品'{product_name}':ui")
def step_impl(context, user, product_name):
	product_list_page = ProductListPage(context.driver)
	product_list_page.load()
	edit_product_page = product_list_page.enter_edit_product_page(product_name)
	edit_product_page.delete()



# ############################################################################################
# # __get_product_from_web_page: 通过web page获取一个用户的特定商品
# ############################################################################################
# def __get_product_from_web_page(context, product_name):
# 	existed_product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)

# 	response = context.client.get('/mall/editor/product/update/%d/' % existed_product.id)
# 	product = response.context['product']

# 	#处理category	
# 	categories = response.context['categories']
# 	category_name = ''
# 	for category in categories:
# 		if hasattr(category, 'selected') and category.selected:
# 			category_name = category.name
# 			break

# 	actual = {
# 		"name": product.name,
# 		"physical_unit": product.physical_unit,
# 		"thumbnails_url": product.thumbnails_url,
# 		"pic_url": product.pic_url,
# 		"introduction": product.introduction,
# 		"detail": product.detail,
# 		"remark": product.remark,
# 		"stock_type": u'无限' if product.stock_type == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
# 		"shelve_type": u'上架' if product.shelve_type == PRODUCT_SHELVE_TYPE_ON else u'下架',
# 		'stocks': product.stocks,
# 		'category': category_name,
# 		'swipe_images': json.loads(product.swipe_images_json),
# 		'is_use_custom_model': u'是' if product.is_use_custom_model else u'否',
# 		'is_enable_model': u'启用规格' if product.is_use_custom_model else u'不启用规格',
# 		'model':{}
# 	}

# 	#填充model信息
# 	if product.is_use_custom_model:
# 		product_models = json.loads(product.models_json_str)
# 		models = {}
# 		for product_model in product_models:
# 			if product_model['name'] == 'standard':
# 				continue
# 			else:
# 				display_name = __get_custom_model_name_from_id(context.webapp_owner_id, product_model['name'])
# 				models[display_name] = {
# 					"price": product_model['price'],
# 					"weight": product_model['weight'],
# 					"stock_type": u'无限' if product_model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
# 					"stocks": product_model['stocks']
# 				}
# 		actual['model']['models'] = models
# 	else:
# 		product_models = json.loads(product.models_json_str)
# 		models = {}
# 		for product_model in product_models:
# 			if product_model['name'] == 'standard':		
# 				models['standard'] = {
# 					"price": product_model['price'],
# 					"weight": product_model['weight'],
# 					"stock_type": u'无限' if product_model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
# 					"stocks": product_model['stocks']
# 				}
# 		actual['model']['models'] = models

# 	return actual


@then(u"{user}能获取商品'{product_name}':ui")
def step_impl(context, user, product_name):
	product_list_page = ProductListPage(context.driver)
	product_list_page.load()
	edit_product_page = product_list_page.enter_edit_product_page(product_name)
	actual = edit_product_page.get_product_content()

	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)
	if 'model' in expected:
		context.tc.assertEquals(len(expected['model']['models']), len(actual['model']['models']))
	

@then(u"{user}找不到商品'{product_name}':ui")
def step_impl(context, user, product_name):
	context.tc.assertEquals(0, Product.objects.filter(name=product_name).count())
	

@then(u"{user}能获取商品列表:ui")
def step_impl(context, user):
	product_list_page = ProductListPage(context.driver)
	product_list_page.load()
	actual = product_list_page.get_products()

	if hasattr(context, 'caller_step_text'):
		expected = json.loads(context.caller_step_text)
		delattr(context, 'caller_step_text')
	else:
		expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual)


@then(u"{user}能获取商品列表'{product_list}':ui")
def step_impl(context, user, product_list):
	context.caller_step_text = product_list
	context.execute_steps(u"then %s能获取商品列表:ui" % user)


@when(u"{user}'{direction}'调整'{product_name}':ui")
def step_impl(context, user, direction, product_name):
	product_list_page = ProductListPage(context.driver)
	product_list_page.load()
	product_list_page.sort_product(product_name, direction)
	context.driver.refresh()


@when(u"{user}置顶商品'{product_name}':ui")
def step_impl(context, user, product_name):
	product_list_page = ProductListPage(context.driver)
	product_list_page.load()
	product_list_page.set_product_to_top(product_name)
	context.driver.refresh()


# @when(u"{user}更新商品'{product_name}'")
# def step_impl(context, user, product_name):
# 	existed_product = ProductFactory(name=product_name)

# 	if hasattr(context, 'caller_step_json'):
# 		product = context.caller_step_json
# 		delattr(context, 'caller_step_json')
# 	else:
# 		product = json.loads(context.text)
# 	if not 'name' in product:
# 		product['name'] = existed_product.name
# 	__process_product_data(product)
# 	product = __supplement_product(context, product)

# 	url = '/mall/editor/product/update/%d/' % existed_product.id
# 	context.client.post(url, product)


# @when(u"{user}删除商品'{product_name}'的商品规格'{product_model_name}'")
# def step_impl(context, user, product_name, product_model_name):
# 	product = __get_product_from_web_page(context, product_name)
# 	del product['model']['models'][product_model_name]
# 	context.caller_step_json = product
# 	context.execute_steps(u"when %s更新商品'%s'" % (user, product_name))



@then(u"{webapp_owner_name}能获取最新的订单:ui")
def step_impl(context, webapp_owner_name):
	order_list_page = OrderListPage(context.driver)
	order_list_page.load()
	order_detail_page = order_list_page.enter_latest_order_detail_page()
	order_detail = order_detail_page.get_order_detail()
	actual = order_detail

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)
