# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from webapp.modules.mall.models import *
from webapp.modules.mall.pageobject.postage_list_page import PostageListPage


@when(u"{user}添加邮费配置:ui")
def step_impl(context, user):
	postage_list_page = PostageListPage(context.driver)
	postage_list_page.load()

	postage_configs = json.loads(context.text)
	for postage_config in postage_configs:
		edit_postage_page = postage_list_page.click_add_postage_config_button()
		edit_postage_page.add_postage_config(postage_config)
		edit_postage_page.submit()
		time.sleep(1)


@then(u"{user}能获取添加的邮费配置:ui")
def step_impl(context, user):
	postage_list_page = PostageListPage(context.driver)
	postage_list_page.load()

	actual = postage_list_page.get_postage_configs()
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)

