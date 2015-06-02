# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from webapp.modules.mall.models import *
from webapp.modules.mall.pageobject.pay_interface_list_page import PayInterfaceListPage


@when(u"{user}添加支付方式:ui")
def step_impl(context, user):
	pay_interface_list_page = PayInterfaceListPage(context.driver)
	pay_interface_list_page.load()
	edit_pay_interface_page = pay_interface_list_page.click_add_pay_interface_button()

	pay_interfaces = json.loads(context.text)
	for pay_interface in pay_interfaces:
		edit_pay_interface_page.add_pay_interface(pay_interface)
		edit_pay_interface_page.submit()
		time.sleep(1)


@when(u"{user}更新支付方式'{pay_interface_description}':ui")
def step_impl(context, user, pay_interface_description):
	pay_interface_list_page = PayInterfaceListPage(context.driver)
	pay_interface_list_page.load()
	edit_pay_interface_page = pay_interface_list_page.enter_edit_pay_interface_page(pay_interface_description)

	pay_interface = json.loads(context.text)
	edit_pay_interface_page.add_pay_interface(pay_interface)
	edit_pay_interface_page.submit()


@then(u"{user}能获得支付方式'{pay_interface_description}':ui")
def step_impl(context, user, pay_interface_description):
	pay_interface_list_page = PayInterfaceListPage(context.driver)
	pay_interface_list_page.load()
	edit_pay_interface_page = pay_interface_list_page.enter_edit_pay_interface_page(pay_interface_description)

	actual = edit_pay_interface_page.get_pay_interface()
	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual)


@when(u"{user}删除支付方式'{pay_interface_description}':ui")
def step_impl(context, user, pay_interface_description):
	pay_interface_list_page = PayInterfaceListPage(context.driver)
	pay_interface_list_page.load()
	edit_pay_interface_page = pay_interface_list_page.enter_edit_pay_interface_page(pay_interface_description)
	edit_pay_interface_page.inactive_pay_interface()

	pay_interface_list_page = PayInterfaceListPage(context.driver)
	edit_pay_interface_page = pay_interface_list_page.enter_edit_pay_interface_page(pay_interface_description)
	edit_pay_interface_page.delete()


@then(u"{user}能获得支付方式列表:ui")
def step_impl(context, user):
	pay_interface_list_page = PayInterfaceListPage(context.driver)
	pay_interface_list_page.load()

	expected = json.loads(context.text)
	actual = pay_interface_list_page.get_pay_interfaces()

	bdd_util.assert_list(expected, actual)


@then(u'{user}"{add_ability}"添加其他支付方式:ui')
def step_impl(context, user, add_ability):
	pay_interface_list_page = PayInterfaceListPage(context.driver)
	pay_interface_list_page.load()
	can_add_pay_interface = pay_interface_list_page.can_add_pay_interface()

	if add_ability == u'还能':
		context.tc.assertTrue(can_add_pay_interface)
	elif add_ability == u'不能':
		context.tc.assertFalse(can_add_pay_interface)
	else:
		assert False
