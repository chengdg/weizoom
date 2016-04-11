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


@when(u"{user}下订单")
def step_impl(context, user):
	context.infos = json.loads(context.text)
	order_info = context.infos.order_info
	rule_order_info = {
		'order_attribute':order_info["name"],
		'company':order_info["company"],
		'responsible_person':order_info["responsible_person"],
		'contact':order_info["contact"],
		'sale_name':order_info["sale_name"],
		'sale_deparment':order_info["sale_deparment"],
		'comments':order_info["comments"],
		'card_info':[]
	}
	for rule in context.infos.card_info:
		rule_order_info['card_info'].append({
			"name": rule["name"],
			"order_num": rule["order_num"],
			"start_date": rule["start_date"],
			"end_date": rule["end_date"],
		})
	rule_order_list.append(rule_order_info)
	response = context.client.put('/order/api/create_rule_order/', rule_order_info)
	bdd_util.assert_api_call_success(response)