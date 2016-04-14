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

@Then(u"{user}能获得'{rule_name}'订单详情列表")
def step_impl(context, user, rule_name):
	card_rule = card_models.WeizoomCardRule.objects.filter(name=rule_name)
	order_id = 0 
	if card_rule:
		rule_id = card_rule[0].id
		order_item = card_models.WeizoomCardOrderItem.objects.filter(weizoom_card_rule_id=rule_id)
		order_id = order_item[0].weizoom_card_order_id if order_item else 0
	expected = json.loads(context.text)
	response = context.client.get('/order/api/order_detail/?order_id={}'.format(order_id))
	actual = json.loads(response.content)['data']['order_item_list']
	actual_list = []
	print type(json.loads(actual))
	print actual,888888888
	for order_item in json.loads(actual):
		actual_list.append({
			'name':	order_item.get('name'),
			'money': "%.2f"%(float(order_item.get('money'))),
			'num':	u"%d"%int(order_item.get('count')),
			'total_money':	"%.2f"%(float(order_item.get('total_money'))),
			'type':	order_item.get('card_kind'),
			"is_limit": order_item.get('valid_restrictions'),
			'card_range': order_item.get('card_range'),
		})
	print actual_list,7777777777
	bdd_util.assert_list(expected, actual_list)


@Then(u"{user}能获得'{rule_name}'微众卡列表")
def step_impl(context, user, rule_name):
	print "+++++++++++++++++++++===================="
	card_rule = card_models.WeizoomCardRule.objects.filter(name=rule_name)
	order_item_id = 0 
	rule_id = 0
	if card_rule:
		rule_id = card_rule[0].id
		order_item = card_models.WeizoomCardOrderItem.objects.filter(weizoom_card_rule_id=rule_id)
		order_item_id = order_item[0].id if order_item else 0
	expected = json.loads(context.text)
	response = context.client.get('/order/api/card_detail/?rule_id={}&order_item_id={}'.format(rule_id,order_item_id))
	actual = json.loads(response.content)['data']['weizoom_card_list']
	actual_list = []
	for ard_list in json.loads(actual):
		actual_list.append({
			'card_num':	ard_list.card_num,
			'status': ard_list.card_status,
			'money': ard_list.money,
			'rest_money': ard_list.balance,
			'start_date':	ard_list.validate_from,
			'end_date':	ard_list.validate_to,
			'comments': ard_list.remark,
		})
	print actual_list,7777777777
	bdd_util.assert_list(expected, actual_list)
