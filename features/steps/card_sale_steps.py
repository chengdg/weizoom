# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util

from card import models as card_models
from weapp import models as weapp_models
from django.contrib.auth.models import User

WEIZOOM_CARD_ORDER_TEXT2ATTRIBUTE = {
	u'发售卡':0,
	u'内部领用卡':1,
	u'返点卡':2
}

@when(u"{user}下订单")
def step_impl(context, user):
	context.infos = json.loads(context.text)
	name2rule_id = {}
	for rule in card_models.WeizoomCardRule.objects.all():
		if rule.name:
			name = rule.name
		else:
			name = u'%.f元卡' % rule.money
		name2rule_id[name] = rule.id
	for info in context.infos:
		order_info = info["order_info"]
		order_attributes = WEIZOOM_CARD_ORDER_TEXT2ATTRIBUTE[order_info["order_attribute"]]
		rule_order_info = {
			'order_attributes':order_attributes,
			'company_info':order_info["company"],
			'responsible_person':order_info["responsible_person"],
			'contact':order_info["contact"],
			'sale_name':order_info["sale_name"],
			'sale_deparment':order_info["sale_deparment"],
			'remark':order_info["comments"],
			'rule_order':[]
		}
		for rule in info["card_info"]:
			name = rule["name"]
			rule_order_info["rule_order"].append({
				"rule_id": name2rule_id[name],
				"card_rule_num": rule["order_num"],
				"valid_time_from": rule["start_date"],
				"valid_time_to": rule["end_date"],
			})
		rule_order_info["rule_order"] = json.dumps(rule_order_info["rule_order"])
		response = context.client.post('/order/api/order_data/', rule_order_info)
		bdd_util.assert_api_call_success(response)

@then(u"{user}能获得订单列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/order/api/rule_order/')
	actual = json.loads(response.content)['data']['card_order_list']
	actual_list = []
	rule_list = []
	order_money = 0
	for rule in actual:
		order_money += int(rule["total_money"])
		order_attribute = rule["order_attribute"]
		apply_person = rule["apply_person"]
		company = rule["company"]
		rule_list.append({
			"name": rule["name"],
			"money": rule["money"],
			"num": str(rule["weizoom_card_order_item_num"]),
			"total_money": rule["total_money"],
			"type": rule["card_kind"],
		})
	rule_order = {
		"card_info" : rule_list,
		"order_attribute": order_attribute,
		"apply_person": apply_person,
		"apply_department": company
	}
	actual_list.append(rule_order)
	
	bdd_util.assert_list(expected, actual_list)