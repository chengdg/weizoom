# -*- coding: utf-8 -*-
import json
import time

from behave import *

from django.contrib.auth.models import User

from test import bdd_util
from features.testenv.model_factory import *

from account.pageobject.login_page import LoginPage
from test.pageobject.page_frame import PageFrame

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from test.helper import WAIT_SHORT_TIME
from webapp.models import Project
from features.testenv.model_factory import (
    ProductCategoryFactory, ProductFactory
)

@when(u"清空浏览器")
def step_impl(context):
	context.client.reset()


@given(u"开启手动清除cookie模式")
def step_impl(context):
	context.in_manual_delete_cookie_mode = True


@then(u'浏览器cookie包含"{cookie_keys}"')
def step_impl(context, cookie_keys):
	actual = {}
	for cookie_value in context.client.cookies.values():
		actual[cookie_value.key] = 1

	cookie_keys = cookie_keys[1:-1]
	expecteds = cookie_keys.split(',')
	for expected in expecteds:
		if not expected:
			continue

		is_in_operator = True
		expected = expected.strip()
		if expected[0] == '!':
			is_in_operator = False
			expected = expected[1:]

		if is_in_operator:
			assert expected in actual, 'cookie "%s" is not in %s' % (expected, actual)
		else:
			assert (not expected in actual), 'cookie "%s" CAN NOT be in %s' % (expected, actual)


@then(u'浏览器cookie等于')
def step_impl(context):
	actual = {}
	for cookie_value in context.client.cookies.values():
		actual[cookie_value.key] = cookie_value.value

	cookie_relations = json.loads(context.text)
	for cookie_key, context_key in cookie_relations.items():

		if cookie_key == "uuid":
			continue
		if len(context_key) == 0:
			assert (not cookie_key in actual), '%s CAN NOT be in cookie' % cookie_key
		else:
			actual_value = actual[cookie_key]
			is_equal_operator = True
			if context_key[0] == '!':
				is_equal_operator = False
				context_key = context_key[1:]
			expected_value = getattr(context, context_key)

			if is_equal_operator:
				assert expected_value == actual_value, 'context.%s(%s) != cookie.%s(%s)' % (context_key, expected_value, cookie_key, actual_value)
			else:
				assert expected_value != actual_value, 'NEED context.%s != cookie.%s' % (context_key, cookie_key)


@then(u"{user}获得错误提示'{error}'")
def step_impl(context, user, error):
	context.tc.assertEquals(error, context.server_error_msg)

@then(u"{user}获得'{product_name}'错误提示'{error}'")
def step_impl(context, user, product_name ,error):
	detail = context.response_json['data']['detail']
	context.tc.assertEquals(error, detail[0]['short_msg'])
	pro_id = ProductFactory(name=product_name).id
	context.tc.assertEquals(pro_id, detail[0]['id'])