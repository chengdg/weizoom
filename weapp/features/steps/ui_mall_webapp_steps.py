# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import WebAppUser, ShipInfo

from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage
from webapp.modules.mall.pageobject.webapp_page.edit_order_page import WAEditOrderPage
from webapp.modules.mall.pageobject.webapp_page.edit_ship_address_page import WAEditShipAddressPage


@then(u"webapp页面标题为'{page_title}':ui")
def step_impl(context, page_title):
	page = context.page
	actual = page.get_title()
	expected = page_title

	context.tc.assertEquals(expected, actual)
	

@when(u"{webapp_user_name}浏览{webapp_owner_name}的webapp的'{category_name}'商品列表页:ui")
def step_impl(context, webapp_user_name, webapp_owner_name, category_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	product_list_page = home_page.enter_product_list_page()
	if category_name != u'全部':
		product_list_page.switch_category(category_name)
	context.page = product_list_page



@then(u"{webapp_user_name}获得webapp商品列表:ui")
def step_impl(context, webapp_user_name):
	product_list_page = context.page
	actual = product_list_page.get_products()
	
	expected = json.loads(context.text)
	
	bdd_util.assert_list(expected, actual)


@then(u"webapp页面上'{capability}'选择商品分类:ui")
def step_impl(context, capability):
	product_list_page = context.page

	if capability == u'能':
		context.tc.assertTrue(product_list_page.can_switch_category())
	else:
		context.tc.assertFalse(product_list_page.can_switch_category())


@when(u"{webapp_user_name}浏览{webapp_owner_name}的webapp的'{product_name}'商品页:ui")
def step_impl(context, webapp_user_name, webapp_owner_name, product_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	product_list_page = home_page.enter_product_list_page()
	product_detail_page = product_list_page.enter_product_detail_page(product_name)

	context.page = product_detail_page


@then(u"{webapp_user_name}获得webapp商品:ui")
def step_impl(context, webapp_user_name):
	product_detail_page = context.page

	product_detail_page.show_purchase_panel()
	actual = product_detail_page.get_product_info()
	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)


@then(u"{webapp_user_name}获得webapp商品的购买数量为'{purchase_count}':ui")
def step_impl(context, webapp_user_name, purchase_count):
	product_detail_page = context.page
	actual = product_detail_page.get_purchase_count()

	expected = int(purchase_count)

	context.tc.assertEquals(expected, actual)


@then(u"{webapp_user_name}获得webapp商品的购买信息为:ui")
def step_impl(context, webapp_user_name):
	product_detail_page = context.page

	product_detail_page.show_purchase_panel()
	actual = product_detail_page.get_product_info()
	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)


# @when(u"{webapp_user_name}增加购买'{count}'个webapp商品:ui")
# def step_impl(context, webapp_user_name, count):
# 	product_detail_page = context.page
# 	product_detail_page.increase_purchase_count(int(count))


# @when(u"{webapp_user_name}减少购买'{count}'个webapp商品:ui")
# def step_impl(context, webapp_user_name, count):
# 	product_detail_page = context.page
# 	product_detail_page.decrease_purchase_count(int(count))
	

@then(u"{webapp_user_name}获得待编辑订单:ui")
def step_impl(context, webapp_user_name):
	edit_order_page = context.page
	expected = json.loads(context.text)
	actual = {}
	if 'product_groups' in expected:
		actual['product_groups'] = edit_order_page.get_product_groups()

	if 'ship_info' in expected:
		actual['ship_info'] = edit_order_page.get_ship_info()

	if 'price_info' in expected:
		actual['price_info'] = edit_order_page.get_price_info(expected['price_info'])

	bdd_util.print_json(actual)
	
	bdd_util.assert_dict(expected, actual)


def __has_ship_info(webapp_user_name, webapp_owner_name):
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	webapp_user = WebAppUser.objects.get(member_id=member.id)
	if ShipInfo.objects.filter(webapp_user_id=webapp_user.id).count() > 0:
		return True
	else:
		return False

def __create_default_ship_info(webapp_user_name, webapp_owner_name):
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	webapp_user = WebAppUser.objects.get(member_id=member.id)
	ShipInfo.objects.create(
		webapp_user_id = webapp_user.id,
		ship_name = 'bill',
		ship_tel = '13811223344',
		ship_address = u'泰兴大厦',
		area = '1_1_8',
		is_selected = True
	)

@when(u"{webapp_user_name}使用'{pay_interface_type}'购买{webapp_owner_name}的商品:ui")
def step_impl(context, webapp_user_name, pay_interface_type, webapp_owner_name):
	if context.text:
		args = json.loads(context.text)
	else:
		args = {}

	if webapp_owner_name == u'订单中':
		edit_order_page = context.page
	else:
		home_page = WAHomePage(context.webapp_driver)
		home_page.load()

		product = args['products'][0]
		product_list_page = home_page.enter_product_list_page()
		product_detail_page = product_list_page.enter_product_detail_page(product['name'])
		product_detail_page.show_purchase_panel()
		product_detail_page.increase_purchase_count_to(product['count'])
		has_ship_info = __has_ship_info(webapp_user_name, webapp_owner_name)
		if (not has_ship_info) and (not 'ship_name' in args):
			#数据库中无ship info，且购买参数中也无ship info，创建默认ship info
			__create_default_ship_info(webapp_user_name, webapp_owner_name)
			has_ship_info = True
		product_detail_page.do_purchase()

		#判断是否有收货地址
		if has_ship_info:
			edit_order_page = WAEditOrderPage(context.webapp_driver)
		else:
			edit_ship_address_page = WAEditShipAddressPage(context.webapp_driver)
			edit_ship_address_page.input_ship_info(args)
			edit_ship_address_page.click_submit_button()
			edit_order_page = WAEditOrderPage(context.webapp_driver)

	#使用积分
	if args.get('use_integral', False):
		edit_order_page.use_integral()

	#使用优惠券
	if 'coupon' in args:
		if args['coupon_type'] == u'选择':
			edit_order_page.use_coupon(args['coupon'])
		else:
			edit_order_page.input_coupon(args['coupon'])

	#输入商家留言
	if 'customer_message' in args:
		edit_order_page.input_customer_message(args['customer_message'].strip())

	if edit_order_page.is_encounter_error():
		#编辑订单过程中出错
		context.error_message = edit_order_page.get_error_message()
	else:
		edit_order_page.select_pay_interface(pay_interface_type)
		page = edit_order_page.submit_order()
		if page.is_webapp_pay_interface_list_page():
			#进入订单支付
			if pay_interface_type == u'不支付':
				context.page = page
				pay_result_page = None
			else:
				pay_interface_list_page = page
				pay_result_page = pay_interface_list_page.select_pay_interface(pay_interface_type)
		elif page.is_webapp_pay_result_page():
			#订单直接支付完成
			pay_result_page = page
		else:
			#提交订单出错
			pay_result_page = None
			context.error_message = page.err_message
		context.pay_result_page = pay_result_page


@when(u"{webapp_user_name}从商品详情页发起购买操作:ui")
def step_impl(context, webapp_user_name):
	if context.text:
		args = json.loads(context.text)
	else:
		args = {}


	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	product = args['products'][0]
	product_list_page = home_page.enter_product_list_page()
	product_detail_page = product_list_page.enter_product_detail_page(product['name'])
	product_detail_page.show_purchase_panel()
	product_detail_page.increase_purchase_count_to(product['count'])
	product_detail_page.do_purchase()

	edit_order_page = WAEditOrderPage(context.webapp_driver)
	context.page = edit_order_page


@when(u"{webapp_user_name}对商品'{product_name}'使用积分:ui")
def step_impl(context, webapp_user_name, product_name):
	edit_order_page = context.page
	edit_order_page.use_integral(product_name, "")

@when(u"{webapp_user_name}对规格为'{product_model}'的商品'{product_name}'使用积分:ui")
def step_impl(context, webapp_user_name, product_model, product_name):
	edit_order_page = context.page
	edit_order_page.use_integral(product_name, product_model)

@when(u"{webapp_user_name}对商品'{product_name}'取消使用积分:ui")
def step_impl(context, webapp_user_name, product_name):
	edit_order_page = context.page
	edit_order_page.unuse_integral(product_name, "")

@when(u"{webapp_user_name}对规格为'{product_model}'的商品'{product_name}'取消使用积分:ui")
def step_impl(context, webapp_user_name, product_model, product_name):
	edit_order_page = context.page
	edit_order_page.unuse_integral(product_name, product_model)


@when(u"{webapp_user_name}立即购买{webapp_owner_name}的商品:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	if context.text:
		args = json.loads(context.text)
	else:
		args = {}


	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	product = args['product']
	product_list_page = home_page.enter_product_list_page()
	product_detail_page = product_list_page.enter_product_detail_page(product['name'])
	product_detail_page.show_purchase_panel()
	product_detail_page.increase_purchase_count_to(product['count'])
	product_detail_page.do_purchase()

	edit_order_page = WAEditOrderPage(context.webapp_driver)
	context.page = edit_order_page
		

@then(u"{webapp_user_name}获得支付结果:ui")
def step_impl(context, webapp_user_name):
	expected = json.loads(context.text)

	actual = context.pay_result_page.get_pay_result()
	bdd_util.assert_dict(expected, actual)


@then(u"{webapp_user_name}成功创建订单:ui")
def step_impl(context, webapp_user_name):
	context.tc.assertTrue(context.page.is_webapp_pay_interface_list_page())


@then(u"{webapp_user_name}获得创建订单失败的信息'{error_message}':ui")
def step_impl(context, webapp_user_name, error_message):
	expected = error_message
	actual = context.error_message
	context.tc.assertEquals(expected, actual)	


@when(u"{webapp_user_name}加入{webapp_owner_name}的商品到购物车:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	products = json.loads(context.text)

	for product in products:
		home_page = WAHomePage(context.webapp_driver)
		home_page.load()

		product_list_page = home_page.enter_product_list_page()
		product_detail_page = product_list_page.enter_product_detail_page(product['name'])
		product_detail_page.show_purchase_panel()
		#这里必须先选择规格，再调整数量
		if product.get('model', None):
			product_detail_page.select_model(product['model'])
		if product.get('count', None):
			product_detail_page.increase_purchase_count_to(product['count'])
		product_detail_page.add_to_shopping_cart()


@then(u"{webapp_user_name}能获得购物车:ui")
def step_impl(context, webapp_user_name):
	page = getattr(context, 'page', None)
	if page and page.is_shopping_cart_page():
		#在购物车页面再次获取信息时，不需要重新进入
		shopping_cart_page = page
	else:
		home_page = WAHomePage(context.webapp_driver)
		home_page.load()
		product_list_page = home_page.enter_product_list_page()
		shopping_cart_page = product_list_page.enter_shopping_cart_page()
		context.page = shopping_cart_page
	actual = {
		"product_groups": shopping_cart_page.get_product_groups(),
		"total_product_count": shopping_cart_page.get_total_product_count(),
		"total_price": shopping_cart_page.get_total_price()
	}

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{webapp_user_name}增加'{count}'个购物车中'{product_name}'的数量:ui")
def step_impl(context, webapp_user_name, count, product_name):
	shopping_cart_page = context.page
	shopping_cart_page.increase_purchase_count(product_name, int(count))


@when(u"{webapp_user_name}减少'{count}'个购物车中'{product_name}'的数量:ui")
def step_impl(context, webapp_user_name, count, product_name):
	shopping_cart_page = context.page
	shopping_cart_page.decrease_purchase_count(product_name, int(count))


@when(u"{webapp_user_name}选中购物车中商品'{product_name}':ui")
def step_impl(context, webapp_user_name, product_name):
	shopping_cart_page = context.page
	shopping_cart_page.select_product(product_name)


@when(u"{webapp_user_name}取消对购物车中商品'{product_name}'的选中:ui")
def step_impl(context, webapp_user_name, product_name):
	shopping_cart_page = context.page
	shopping_cart_page.select_product(product_name)


@when(u"{webapp_user_name}从购物车中删除商品'{product_name}':ui")
def step_impl(context, webapp_user_name, product_name):
	page = getattr(context, 'page', None)
	if page and page.is_shopping_cart_page():
		#在购物车页面再次获取信息时，不需要重新进入
		shopping_cart_page = page
	else:
		home_page = WAHomePage(context.webapp_driver)
		home_page.load()

		product_list_page = home_page.enter_product_list_page()
		shopping_cart_page = user_center_page.enter_shopping_cart_page()
	shopping_cart_page.delete_product(product_name)


@when(u"{webapp_user_name}从购物车发起购买操作:ui")
def step_impl(context, webapp_user_name):
	page = getattr(context, 'page', None)
	if page and page.is_shopping_cart_page():
		#在购物车页面再次获取信息时，不需要重新进入
		shopping_cart_page = page
	else:
		home_page = WAHomePage(context.webapp_driver)
		home_page.load()
		product_list_page = home_page.enter_product_list_page()
		shopping_cart_page = product_list_page.enter_shopping_cart_page()
	# if getattr(context, 'text', None):
	# 	args = json.loads(context.text)
	# 	products = args['products']
	# 	if products == 'all':
	# 		shopping_cart_page.select_products('all')
	# 	else:
	# 		for product in products:
	# 			shopping_cart_page.select_products(product['name'])
	# 			shopping_cart_page.increase_purchase_count_to(product['name'], product['count'])
	# else:
	# 	args = {}

	#判断是否需要填充默认的收货地址
	has_ship_info = __has_ship_info(webapp_user_name, context.webapp_owner_name)
	# if (not has_ship_info) and (not 'ship_info' in args):
	# 	#数据库中无ship info，且购买参数中也无ship info，创建默认ship info
	# 	__create_default_ship_info(webapp_user_name, context.webapp_owner_name)
	# 	has_ship_info = True

	#获得提交后的page，可能情况：
	#1. 购物车page
	#2. 编辑收货地址page
	#3. 编辑订单page
	page = shopping_cart_page.submit_order()

	if page.is_shopping_cart_page():
		context.page = page
	else:
		if not has_ship_info:
			edit_ship_address_page = WAEditShipAddressPage(context.webapp_driver)
			edit_ship_address_page.input_ship_info(args['ship_info'])
			edit_ship_address_page.click_submit_button()
			edit_order_page = WAEditOrderPage(context.webapp_driver)
			context.page = edit_order_page
		else:
			edit_order_page = WAEditOrderPage(context.webapp_driver)
			context.page = edit_order_page
