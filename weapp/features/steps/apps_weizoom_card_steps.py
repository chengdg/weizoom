#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cl'

from behave import *
import json
from test import bdd_util

@when(u"{user}进行微众卡余额查询")
def step_impl(context, user):
	args = json.loads(context.text)
	client = context.client
	webapp_owner_id = context.webapp_owner_id
	url = '/webapp/api/project_api/call/'

	# 获取微众卡id
	data = {
		"woid": webapp_owner_id,
		"module": 'mall',
		"target_api": "weizoom_card/check",
		"project_id": "market_tool:weizoom_card:{}".format(webapp_owner_id),
		"name": args.get("id"),
		"password": args.get("password")
	}
	response = context.client.post(url, data)
	response_json = json.loads(response.content)

	if response_json.get('code') == 200:
		context.card_info = response_json.get("data")
	else:
		context.server_error_msg = response_json.get("data").get('msg')

@then(u"{user}获得微众卡余额查询结果")
def step_impl(context, user):
	expected = json.loads(context.text)

	webapp_owner_id = context.webapp_owner_id
	url = '/termite/workbench/jqm/preview/?module=market_tool:weizoom_card&webapp_owner_id=%s&model=weizoom_card_change_money&action=get&workspace_id=market_tool:weizoom_card&project_id=0&card_id=%s&normal=1' % (webapp_owner_id,context.card_info.get('id'))
	response = context.client.get(bdd_util.nginx(url), follow=True)
	weizoom_card = response.context['weizoom_card']
	actual = {}
	actual["card_remaining"] = u'%.2f' % weizoom_card.get('money')

	bdd_util.assert_dict(expected,actual)

@then(u"{user}获得错误信息'{msg}'")
def step_impl(context, user,msg):
	actual = context.server_error_msg
	context.tc.assertEquals(msg, actual)
