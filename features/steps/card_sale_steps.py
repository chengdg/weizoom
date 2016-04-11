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
			print name,"gggggggggggggg"
		name2rule_id[name] = rule.id
	print name2rule_id,"dddddddddddddd"
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
		print rule_order_info,99999999999999999999999999999
		for rule in info["card_info"]:
			name = rule["name"]
			print name,666666666666666666666666666666
			rule_order_info["rule_order"].append({
				"rule_id": name2rule_id[name],
				"card_rule_num": rule["order_num"],
				"valid_time_from": rule["start_date"],
				"valid_time_to": rule["end_date"],
			})
		rule_order_info["rule_order"] = json.dumps(rule_order_info["rule_order"])
		print rule_order_info,"hhhhhhhhh"
		response = context.client.post('/order/api/create_rule_order/', rule_order_info)
		bdd_util.assert_api_call_success(response)