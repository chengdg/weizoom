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
		# order_id = '' if not order_info["order_id"] else order_info["order_id"]
		order_attributes = WEIZOOM_CARD_ORDER_TEXT2ATTRIBUTE[u'发售卡' if not "order_attribute" in order_info.keys() else order_info["order_attribute"]]
		if order_attributes == card_models.WEIZOOM_CARD_ORDER_ATTRIBUTE_SALE:
			rule_order_info = {
				'order_id': -1 if not "order_id" in order_info.keys() else order_info["order_id"],
				'order_attributes': 0 if not order_attributes else order_attributes,
				'company_info': u'窝夫小子' if not "company" in order_info.keys() else order_info["company"],
				'responsible_person':u'窝夫小子' if not "responsible_person" in order_info.keys() else order_info["responsible_person"],
				'contact':u'7777777' if not "contact" in order_info.keys() else order_info["contact"],
				'sale_name':u'7777777' if not "sale_name" in order_info.keys() else order_info["sale_name"],
				'sale_deparment':u'7777777' if not "sale_deparment" in order_info.keys() else order_info["sale_deparment"],
				'remark':u'备注' if not "comments" in order_info.keys() else order_info["comments"],
				'rule_order':[]
			}
		if order_attributes == card_models.WEIZOOM_CARD_ORDER_ATTRIBUTE_INTERNAL:
			rule_order_info = {
				'order_id': -1 if not "order_id" in order_info.keys() else order_info["order_id"],
				'order_attributes': 1 if not order_attributes else order_attributes,
				'use_departent': u'部门' if not "apply_department" in order_info.keys() else order_info["apply_department"],
				'project_name': u'项目' if not "project_name" in order_info.keys() else order_info["project_name"],
				'appliaction':u'目的' if not "purpose" in order_info.keys() else order_info["purpose"],
				'use_persion':u'领用人' if not "apply_person" in order_info.keys() else order_info["apply_person"],
				'remark':u'备注' if not "comments" in order_info.keys() else order_info["comments"],
				'rule_order':[]
			}
		for rule in info["card_info"]:
			name = rule["name"]
			rule_order_info["rule_order"].append({
				"rule_id": name2rule_id[name],
				"card_rule_num": 1 if not "order_num" in rule.keys() else rule["order_num"],
				"valid_time_from": '2010-02-02 00:00' if not "start_date" in rule.keys() else rule["start_date"],
				"valid_time_to": '2010-02-02 00:00' if not "end_date" in rule.keys() else rule["end_date"],
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
	rule_order = {}
	real_pay = 0.00
	for rules in json.loads(actual):
		order_item_list = json.loads(rules['order_item_list'])
		order_attribute = rules["order_attribute"]
		apply_person = rules["responsible_person"]

		use_departent = rules["use_departent"]
		use_persion = rules["use_persion"]
		order_attribute_num = WEIZOOM_CARD_ORDER_TEXT2ATTRIBUTE[order_attribute]
		company = rules["company"]
		status =u'未激活'
		print rules['is_activation'],88888888888
		if rules['is_activation'] ==1:
			status =u'已激活'
		print rules['status'] ,777777777777777777777777
		if  rules['status'] ==1 and rules['is_activation'] == 0:
			status = u'已取消'
		for order_item in order_item_list:
			real_pay += float(order_item["total_money"])
			weizoom_card_id_first = order_item["weizoom_card_id_first"]
			weizoom_card_id_last = order_item["weizoom_card_id_last"]
			card_range = weizoom_card_id_first + "-" + weizoom_card_id_last

			if order_item["name"]:
				name = order_item["name"]
			else:
				name = order_item["money"].replace('.00',u'元卡')

			rule_list.append({
				"name": name,
				"money": str(order_item["money"]),
				"num": str(order_item["weizoom_card_order_item_num"]),
				"total_money": order_item["total_money"],
				"type": order_item["card_kind"],
				"card_range": card_range,
				"is_limit": order_item["valid_restrictions"],
				"vip_shop": ""
			})
		if order_attribute_num == card_models.WEIZOOM_CARD_ORDER_ATTRIBUTE_SALE:
			rule_order = {
				"order_id": rules["order_number"],
				"card_info" : rule_list,
				"order_attribute": order_attribute,
				"apply_person": apply_person,
				"apply_department": company,
				"real_pay": '%.2f' % real_pay,
				"order_money": '%.2f' % real_pay,
				"status": status,
			}
		if order_attribute_num == card_models.WEIZOOM_CARD_ORDER_ATTRIBUTE_INTERNAL:
			rule_order = {
				"order_id": rules["order_number"],
				"card_info" : rule_list,
				"order_attribute": order_attribute,
				"apply_person": use_persion,
				"apply_department": use_departent,
				"real_pay": '%.2f' % real_pay,
				"order_money": '%.2f' % real_pay,
				"status": status,
			}
		actual_list.append(rule_order)
	print actual_list,"++++++++++++++="
	print expected,"-------------="
	bdd_util.assert_list(expected, actual_list)