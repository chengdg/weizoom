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

CARD_KIND_TEXT2INDEX = {
	"entity": card_models.WEIZOOM_CARD_ENTITY,
	"virtual": card_models.WEIZOOM_CARD_ELECTRONIC,
	"condition": card_models.WEIZOOM_CARD_CONDITION,
	"property": card_models.WEIZOOM_CARD_SPECIAL
}

#卡库列表
def expected_weizoom_cards(context,user,rule_name,card_class):
	expected_table = context.table
	expected_list = []
	if expected_table:
		for row in expected_table:
			order = row.as_dict()
			expected_list.append(order)

	user_id = bdd_util.get_user_id_for(user)
	rule = card_models.WeizoomCardRule.objects.filter(owner_id=user_id, name=rule_name)
	if rule.count() == 0:
		money = int(rule_name[:-2])
		rule = card_models.WeizoomCardRule.objects.filter(owner_id=user_id, name='',money=money)

	response = context.client.get('/card/api/'+card_class+'/',{'weizoom_card_rule_id': rule[0].id})
	actual = json.loads(response.content)['data']['rows']

	card_list = []
	for card in actual:
		card_list.append({
			"card_number": card["weizoom_card_id"],
			"status": card["storage_status_text"],
			"money": card["rule_money"],
			"rest_money": card["money"],
			"comments": card["remark"],
			"apply_per": card["activated_to"],
			"apply_dep": card["department"]
		})
	logging.info(card_list)
	
	bdd_util.assert_list(expected_list, card_list)

@when(u"{user}新建通用卡")
def step_impl(context, user):
	context.rules = json.loads(context.text)
	
	for rule in context.rules:
		rule_dict = {
			"name": rule["name"],
			"weizoom_card_id_prefix": rule["prefix_value"],
			"card_kind": CARD_KIND_TEXT2INDEX[rule["type"]],
			"money": rule["money"],
			"count": rule["num"],
			"remark": rule["comments"]
		}

		response = context.client.put('/card/api/create_ordinary/', rule_dict)
		bdd_util.assert_api_call_success(response)

@then(u"'{user}'能获得通用卡规则列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/card/api/ordinary_rules/')
	actual = json.loads(response.content)['data']['rows']
	rule_list = []
	for rule in actual:
		rule_list.append({
			"name": rule["name"],
			"money": rule["money"],
			"num": str(rule["count"]),
			"stock": str(rule["count"]),
			"type": rule["card_kind"],
			"card_range": rule["card_range"],
			"comments": rule['remark']
		})
	logging.info(rule_list)
	
	bdd_util.assert_list(expected, rule_list)

@then(u"'{user}'能获得通用卡'{rule_name}'的库存列表")
def step_impl(context, user,rule_name):
	expected_weizoom_cards(context,user,rule_name,'ordinary_cards')
	

@when(u"{user}新建限制卡")
def step_impl(context,user):
	context.rules = json.loads(context.text)

	store_name_list = []
	for rule in context.rules:
		if rule.has_key("vip_shop"):
			store_name_list = rule["vip_shop"].split(',')
	
	user_id2username = {user.id: user.username for user in User.objects.using('weapp').filter(username__in=store_name_list)}
	userProfiles = weapp_models.UserProfile.objects.using('weapp').filter(user_id__in=user_id2username.keys())

	if userProfiles.count() > 0:
		for userprofile in userProfiles:
			weapp_models.UserProfile.objects.using('weapp').filter(user_id=userprofile.user_id).update(store_name=user_id2username[userprofile.user_id])

	user_id2store_name = {}
	for user_profile in weapp_models.UserProfile.objects.using('weapp').filter(store_name__in=store_name_list):
		user_id2store_name[user_profile.store_name] = user_profile.user_id
	
	for rule in context.rules:
		use_limit = rule["use_limit"]
		valid_restrictions = -1
		if use_limit["is_limit"] == "on":
			valid_restrictions = use_limit["limit_money"]
		user_ids = []
		if rule.has_key("vip_shop"):
			for shop in rule["vip_shop"].split(','):
				user_ids.append(str(user_id2store_name[user_profile.store_name]))
		if not user_ids:
			user_ids = ['-1']
		is_new_member_special = 0
		if rule.has_key("new_member"):
			if rule["new_member"] == "on":
				is_new_member_special = 1
		rule_dict = {
			"name": rule["name"],
			"weizoom_card_id_prefix": rule["prefix_value"],
			"card_kind": CARD_KIND_TEXT2INDEX[rule["type"]],
			"valid_restrictions": valid_restrictions,
			"shop_limit_list": ",".join(user_ids),
			"is_new_member_special": is_new_member_special,
			"money": rule["money"],
			"count": rule["num"],
			"remark": rule["comments"]
		}

		response = context.client.put('/card/api/create_limit/', rule_dict)
		bdd_util.assert_api_call_success(response)

@then(u"'{user}'能获得限制卡规则列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/card/api/limit_rules/')
	actual = json.loads(response.content)['data']['rows']
	rule_list = []
	for rule in actual:
		rule_list.append({
			"name": rule["name"],
			"money": rule["money"],
			"num": str(rule["count"]),
			"stock": str(rule["count"]),
			"type": rule["card_kind"],
			"is_limit": rule["valid_restrictions"],
			"vip_shop": ",".join(rule["shop_limit_list"]),
			"new_member": rule["is_new_member_special"],
			"card_range": rule["card_range"],
			"comments": rule['remark']
		})
	logging.info(rule_list)
	
	bdd_util.assert_list(expected, rule_list)

@then(u"'{user}'能获得限制卡'{rule_name}'的库存列表")
def step_impl(context, user,rule_name):
	expected_weizoom_cards(context,user,rule_name,'limit_cards')