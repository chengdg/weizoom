# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util
import string
from card import models as card_models
from weapp import models as weapp_models
from django.contrib.auth.models import User

@Then(u"{user}能获得订单详情列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/order/api/order_detail/')
	actual = json.loads(response.content)['data']['order_item_list']
	actual_list = []
	for order_item in actual:
		actual_list.append({
			'name':	order_item.name,
			'money': order_item.money,
			'num':	order_item.count,
			'total_money':	order_item.total_money,
			'type':	order_item.card_kind,
			"is_limit": order_item.valid_restrictions,
			'card_range': order_item.card_range,
		})
	print actual_list,88888888888
	bdd_util.assert_list(expected, actual_list)


@Then(u"{user}能获得'{rule_name}'微众卡列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/order/api/card_detail/')
	actual = json.loads(response.content)['data']['weizoom_card_list']
	actual_list = []
	for ard_list in actual:
		actual_list.append({
			'card_num':	ard_list.card_num,
			'status': ard_list.card_status,
			'money': ard_list.money,
			'rest_money': ard_list.balance,
			'start_date':	ard_list.activated_at,
			'end_date':	ard_list.activated_at,
			'comments': ard_list.remark,
		})
	print actual_list,7777777777
	bdd_util.assert_list(expected, actual_list)
