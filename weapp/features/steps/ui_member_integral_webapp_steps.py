# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from webapp.modules.mall.models import *
from modules.member.models import * 

from webapp.modules.mall.pageobject.webapp_page.home_page import WAHomePage


@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中拥有{integral_count}会员积分:ui")
def step_impl(context, webapp_user_name, webapp_owner_name, integral_count):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	user_center_page = home_page.enter_user_center_page()
	actual = user_center_page.get_integral()

	expected = integral_count

	context.tc.assertEquals(expected, actual)


@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中的积分日志为:ui")
def step_impl(context, webapp_user_name, webapp_owner_name):
	home_page = WAHomePage(context.webapp_driver)
	home_page.load()

	user_center_page = home_page.enter_user_center_page()
	integral_log_page = user_center_page.enter_integral_log_page()
	actual = integral_log_page.get_logs()

	expected = json.loads(context.text)

	context.tc.assertEquals(expected, actual)