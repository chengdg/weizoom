# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.mall.models import *

from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage
from webapp.modules.user_center.pageobject.webapp_page.user_center_page import WAUserCenterPage

@when(u"{webapp_user_name}设置{webapp_owner_name}的webapp的默认收货地址:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	data = {
		'area': '1_1_8',
		'ship_address': '泰兴大厦',
		'ship_name': webapp_user_name,
		'ship_tel': '13811223344'
	}

	#from modules.member.models import ShipInfo
	#ship_info = ShipInfo.objects.get(webapp_user_id=context.webapp_user.id)
	url = '/workbench/jqm/preview/?woid=%s&module=user_center&model=ship_info&action=save' % (context.webapp_owner_id)
	response = context.client.post(bdd_util.nginx(url), data)


@when(u"{webapp_user_name}在{webapp_owner_name}的webapp中添加收货地址:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	ship_info = json.loads(context.text)

	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	user_center_page = home_page.enter_user_center_page()
	ship_info_page = user_center_page.enter_ship_info_page()
	edit_ship_address_page = ship_info_page.enter_edit_ship_info_page()
	edit_ship_address_page.input_ship_info(ship_info)
	edit_ship_address_page.click_submit_button()


@when(u"{webapp_user_name}在{webapp_owner_name}的webapp中更新收货人'{ship_name}'的收货地址:ui")
def step_impl(context, webapp_user_name, webapp_owner_name, ship_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	ship_info = json.loads(context.text)

	user_center_page = home_page.enter_user_center_page()
	ship_info_page = user_center_page.enter_ship_info_page()
	edit_ship_address_page = ship_info_page.enter_edit_ship_info_page(ship_name)
	edit_ship_address_page.input_ship_info(ship_info, force=True)
	edit_ship_address_page.click_submit_button()


@when(u"{webapp_user_name}在订单中切换收货地址:ui")
def step_impl(context, webapp_user_name):
	ship_info = json.loads(context.text)

	edit_order_page = context.page
	edit_order_page.switch_ship_info(ship_info)
	# home_page = WAHomePage(context.webapp_driver)
	# home_page.load()

	# ship_info = json.loads(context.text)

	# user_center_page = home_page.enter_user_center_page()
	# ship_info_page = user_center_page.enter_ship_info_page()
	# edit_ship_address_page = ship_info_page.enter_edit_ship_info_page(ship_name)
	# edit_ship_address_page.input_ship_info(ship_info, force=True)
	# edit_ship_address_page.click_submit_button()


@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中查看收货人'{ship_name}'的收货地址:ui")
def step_impl(context, webapp_user_name, webapp_owner_name, ship_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	user_center_page = home_page.enter_user_center_page()
	ship_info_page = user_center_page.enter_ship_info_page()
	edit_ship_address_page = ship_info_page.enter_edit_ship_info_page(ship_name)
	actual = edit_ship_address_page.get_ship_info()

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中拥有收货地址:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	user_center_page = home_page.enter_user_center_page()
	ship_info_page = user_center_page.enter_ship_info_page()
	actual = ship_info_page.get_ship_infos()

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中拥有优惠券:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	user_center_page = home_page.enter_user_center_page()
	user_coupon_page = user_center_page.enter_user_coupon_page()
	actual = user_coupon_page.get_coupons()

	expected = json.loads(context.text)

	context.tc.assertEquals(expected, actual)