# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
#from weixin.message.qa.models import *
from weixin2.models import *

#######################################################################
# __add_rule: 添加一个规则
#######################################################################
def __add_rule(context, rule):
	rule_prototype = {
		"patterns": "",
		"answer": "answer"
	}
	rule_prototype.update(rule)
	context.client.post('/new_weixin/api/keyword_rules/?_method=put', rule_prototype)


@given(u"{user}已添加关键词自动回复规则")
def step_impl(context, user):
	client = context.client
	context.rules = json.loads(context.text)
	for rule in context.rules:
		__add_rule(context, rule)


@when(u"{user}添加关键词自动回复规则")
def step_impl(context, user):
	client = context.client
	context.rules = json.loads(context.text)
	for rule in context.rules:
		__add_rule(context, rule)
		time.sleep(1)


@then(u"{user}能获取关键词自动回复规则'{rule_patterns}'")
def step_impl(context, user, rule_patterns):
	existed_rule = Rule.objects.get(patterns=rule_patterns)

	expected = json.loads(context.text)

	response = context.client.get('/new_weixin/api/keyword_rules/?_method=get&id=%d' % existed_rule.id)
	rule =json.loads(response.content)['data']['items'][0]

	try:
		if len(rule['answer']) > 0:
			rule['answer'] = rule['answer'][0]['content']
	except:
		pass

	try:
		if len(rule['patterns']) > 0:
			rule['patterns'] = rule['patterns'][0]['keyword']
	except Exception, e:
		print e

	actual = {
		"patterns": rule['patterns'],
		"answer": rule['answer'],
		"material_id": rule['material_id'],
		"type": "news" if rule['type'] == NEWS_TYPE else 'text'
	}
	bdd_util.assert_dict(expected, actual)


@then(u"{user}无法获取关键词自动回复规则'{rule_patterns}'")
def step_impl(context, user, rule_patterns):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)

	context.tc.assertEquals(0, Rule.objects.filter(owner=context.client.user, patterns=rule_patterns).count())


@then(u"{user}能获取关键词自动回复规则列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/new_weixin/keyword_rules/')
	rules = response.context['rules']

	actual = []
	for rule in rules:
		answers = rule['answer']
		if len(answers) > 0:
			rule['answer'] = answers[0]['content']

		patterns = rule['patterns']
		if len(patterns) > 0:
			rule['patterns'] = patterns[0]['keyword']

		actual.append({
			"patterns": rule['patterns'],
			"answer": rule['answer'],
			"material_id": rule['material_id'],
			"type": "news" if rule['type'] == NEWS_TYPE else 'text'
		})

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u"{user}更新关键词自动回复规则'{rule_patterns}'")
def step_impl(context, user, rule_patterns):
	existed_rule = Rule.objects.get(patterns=rule_patterns)

	rule = json.loads(context.text)
	rule['id'] = existed_rule.id

	context.client.post('/new_weixin/api/keyword_rules/?_method=post', rule)


@when(u"{user}删除关键词自动回复规则'{rule_patterns}'")
def step_impl(context, user, rule_patterns):
	rule = Rule.objects.get(patterns=rule_patterns)

	url = '/new_weixin/api/keyword_rules/?_method=delete'
	context.client.post(url, data={'id':rule.id}, HTTP_REFERER='/new_weixin/keyword_rules/')


#
# 以下是“关注自动回复规则”step
#
@then(u"{user}能获取关注自动回复规则")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/new_weixin/follow_rules/')
	print response.context['rule']

	rule = response.context['rule']
	if rule == None:
		actual = {
			"answer": '',
			"material_id": 0,
			"type": 'text'
		}
	else:
		try:
			answers = json.loads(rule.answer)
			if len(answers) > 0:
				rule.answer = answers[0]['content']
		except:
			pass

		actual = {
			"answer": rule['answer']['content'],
			"material_id": rule['material_id'],
			"type": "news" if rule['type'] == NEWS_TYPE else 'text'
		}
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{user}添加关注自动回复规则")
def step_impl(context, user):
	client = context.client
	rule = json.loads(context.text)

	data = {
		"material_id": "0",
		"answer": rule['answer']
	}
	print context.client.post('/new_weixin/api/follow_rules/?_method=put', data)


@when(u"{user}更新关注自动回复规则为")
def step_impl(context, user):
	rule = Rule.objects.get(owner=context.client.user, type=FOLLOW_TYPE)
	rule_json = json.loads(context.text)

	data = {
		"material_id": "0",
		"answer": rule_json['answer'],
		"id": rule.id
	}
	context.client.post('/new_weixin/api/follow_rules/?_method=post', data)


#
# 以下是“自动回复规则”step
#
def __process_unmatch_rule(data):
	if data['active_type'] == u'全天启用':
		data['active_type'] = RULE_ACTIVE_TYPE_ACTIVE
	elif data['active_type'] == u'禁用':
		data['active_type'] = RULE_ACTIVE_TYPE_INACTIVE
	elif data['active_type'] == u'定时启用':
		data['active_type'] = RULE_ACTIVE_TYPE_TIMED_ACTIVE
	else:
		pass

@then(u"{user}能获取自动回复规则")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/new_weixin/unmatch_rules/')

	rule = response.context['rule']
	actual = []

	if rule == None:
		actual.append({
			"answer": '',
			"material_id": 0,
			"type": 'text',
			"active_type": RULE_ACTIVE_TYPE_ACTIVE,
			"start_hour": 0,
			"end_hour": 24,
		})
	else:
		try:
			answers = rule['answer']
			if len(answers) > 0:
				rule['answer'] = answers[0]['content']
		except:
			pass


		actual.append({
			"answer": rule['answer'],
			"material_id": rule['material_id'],
			"type": "news" if rule['type'] == NEWS_TYPE else 'text',
			"active_type": rule['active_type'],
			"start_hour": rule['start_hour'],
			"end_hour": rule['end_hour']
		})

	expected = json.loads(context.text)
	__process_unmatch_rule(expected)

	bdd_util.assert_dict(expected, actual[0])


@when(u"{user}添加自动回复规则")
def step_impl(context, user):
	rule = json.loads(context.text)

	data = {
		"material_id": 0,
		"answer": rule['answer'],
		"active_type": rule['active_type']
	}
	__process_unmatch_rule(data)
	context.client.post('/new_weixin/api/unmatch_rules/?_method=put', data)


@when(u"{user}更新自动回复规则为")
def step_impl(context, user):
	rule = Rule.objects.get(owner=context.client.user, type=UNMATCH_TYPE)
	rule_json = json.loads(context.text)

	data = {
		"material_id": 0,
		"answer": rule_json['answer'],
		"id": rule.id,
		"active_type": rule_json['active_type'],
		"start_hour": rule_json.get('start_hour', 0),
		"end_hour": rule_json.get('end_hour', 24)
	}
	__process_unmatch_rule(data)
	context.client.post('/new_weixin/api/unmatch_rules/?_method=post', data)


def __parse_hour(str):
	now = datetime.now()
	if str == u'现在':
		delta = 0
		direction = 1
	else:
		delta, direction = str.split(u'小时')
		delta = int(delta)
		if direction == u'前':
			direction = -1
		else:
			direction = 1

	delta = delta * direction
	return (now + timedelta(hours=delta)).hour


@when(u"{user}更新自动回复规则启用策略为'{active_type}'")
def step_impl(context, user, active_type):
	rule = Rule.objects.get(owner=context.client.user, type=UNMATCH_TYPE)

	start_hour = 0
	end_hour = 24
	if active_type == u'禁用' or active_type == u'全天启用':
		pass
	else:
		start, end = active_type.split('-')
		active_type = u'定时启用'
		start_hour = __parse_hour(start)
		end_hour = __parse_hour(end)

	print 'start_hour: %d, end_hour: %d' % (start_hour, end_hour)
	data = {
		"material_id": 0,
		"answer": rule.answer,
		"id": rule.id,
		"active_type": active_type,
		"start_hour": start_hour,
		"end_hour": end_hour
	}
	__process_unmatch_rule(data)
	context.client.post('/new_weixin/api/unmatch_rules/?_method=post', data)
