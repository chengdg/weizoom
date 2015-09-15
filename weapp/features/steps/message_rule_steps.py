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
	rule_name = rule['rules_name']
	posted = True
	patterns = '['
	for pattern in rule['keyword']:
		if pattern['type'] == 'equal':
			pattern_type = 0
		else:
			pattern_type = 1

		if pattern['keyword'].strip() == '':
			posted = False

		patterns = patterns + '{"keyword":"%s","type":"%s"},' % (pattern['keyword'], pattern_type)
	patterns = patterns[:-1] + ']'
	answers = '['
	for answer in rule['keyword_reply']:
		content = answer['reply_content']
		if answer['reply_type'] == 'text':
			type = 'text'
		else:
			type = 'news'
			news = News.objects.filter(material__owner_id=context.client.user.id, title=answer['reply_content'])[0]
			material_id = news.material_id
			content = material_id
		if str(content).strip() == '':
			posted = False
		answers = answers + '{"content":"%s","type":"%s"},' % (content, type)
	answers = answers[:-1] + ']'

	rule_prototype = {
		"patterns": str(patterns),
		"answer": str(answers),
		"id": "new",
		"rule_name": rule_name
	}
	#rule_prototype.update(rule)
	if posted:
		context.client.post('/new_weixin/api/keyword_rules/?_method=put', rule_prototype)

def __update_rule(context, rule, id):
	rule_name = rule['rules_name']
	posted = True
	patterns = '['
	for pattern in rule['keyword']:
		if pattern['type'] == 'equal':
			pattern_type = 0
		else:
			pattern_type = 1
		if pattern['keyword'].strip() == '':
			posted = False
		patterns = patterns + '{"keyword":"%s","type":"%s"},' % (pattern['keyword'], pattern_type)
	patterns = patterns[:-1] + ']'
	answers = '['
	for answer in rule['keyword_reply']:
		content = answer['reply_content']
		if answer['reply_type'] == 'text':
			type = 'text'
		else:
			type = 'news'
			try:
				news = News.objects.filter(material__owner_id=context.client.user.id, title=answer['reply_content'])[0]
				material_id = news.material_id
				content = material_id
			except:
				content = ''

		answers = answers + '{"content":"%s","type":"%s"},' % (content, type)
		if str(content).strip() == '':
			posted = False
	answers = answers[:-1] + ']'

	rule_prototype = {
		"patterns": str(patterns),
		"answer": str(answers),
		"id": id,
		"rule_name": rule_name
	}
	#rule_prototype.update(rule)
	if posted:
		context.client.post('/new_weixin/api/keyword_rules/?_method=post', rule_prototype)


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
		print(e)

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


@then(u"{user}获得关键词自动回复列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	url = '/new_weixin/api/keyword_rules/?'
	if hasattr(context, 'count_per_page') and hasattr(context, 'cur_page'):
		url += ('count_per_page=%s' % (str(context.count_per_page) + '&')) + 'page=%s' % context.cur_page
	elif hasattr(context, 'keyword'):
		url += 'count_per_page=100&query=%s' % context.keyword
	else:
		url += 'count_per_page=100&page=1'
	response = context.client.get(bdd_util.nginx(url))
	response_json = json.loads(response.content)
	rules = response_json['data']['items']
	actual = []
	for rule in rules:
		try:
			current_dict = {}
			current_dict['rules_name'] = rule['rule_name']

			patterns = []
			for pattern in eval(rule['patterns'][0]['keyword']):
				if pattern['type'] == '0':
					type = 'equal'
				else:
					type = 'like'
				patterns.append({
					'type':type,
					'keyword': pattern['keyword']
					})
			current_dict['keyword'] = patterns

			answers = []
			for answer in eval(rule['answer'][0]['content']):
				if answer['type'] != 'text':
					material_id = answer['content']
					#material = Material.objects.get(id=material_id)
					new =  News.objects.filter(material_id=material_id)[0]
					reply_content = new.title
					reply_type = 'text_picture'
				else:
					reply_type = 'text'
					reply_content = answer['content']
				answers.append({
					"reply_content":reply_content,
					"reply_type":reply_type
					})
			current_dict['keyword_reply'] = answers

			actual.append(current_dict)
		except:
			current_dict = {}
			current_dict['rules_name'] = rule['rule_name']

			patterns = []
			for pattern in rule['patterns']:
				if pattern['type'] == '0':
					type = 'equal'
				else:
					type = 'like'
				patterns.append({
					'type':type,
					'keyword': pattern['keyword']
					})
			current_dict['keyword'] = patterns

			answers = []
			for answer in rule['answer']:
				if answer['type'] != 'text':
					material_id = answer['content']
					#material = Material.objects.get(id=material_id)
					new =  News.objects.filter(material_id=material_id)[0]
					reply_content = new.title
					reply_type = 'text_picture'
				else:
					reply_type = 'text'
					reply_content = answer['content']
				answers.append({
					"reply_content":reply_content,
					"reply_type":reply_type
					})
			current_dict['keyword_reply'] = answers

			actual.append(current_dict)


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
	rule = Rule.objects.get(rule_name=rule_patterns)

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
	print(response.context['rule'])

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
	rule = json.loads(context.text)[0]
	if rule == 'text_picture':
		new_title = rule['reply_content']
		news = News.objects.filter(material__owner_id=context.client.user.id, title=new_title)[0]
		material_id = news.id
		reply_content = rule['reply_content']
	else:
		material_id = 0
		reply_content = rule['reply_content']

	data = {
		"material_id": material_id,
		"answer": reply_content
	}
	print(context.client.post('/new_weixin/api/follow_rules/?_method=put', data))


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

	print('start_hour: %d, end_hour: %d' % (start_hour, end_hour))
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

@when(u"{user}添加小尾巴")
def step_impl(context, user):
	data_json = json.loads(context.text)[0]
	if data_json['is_open'] == 'true':
		is_active = 1
	else:
		is_active = 0

	data = {
		"tail": data_json['reply_content'],
		"is_active": is_active
	}
	context.client.post('/new_weixin/api/message_tails/?_method=put', data)

@when(u"{user}已添加消息托管")
def step_impl(context, user):
	#rule = Rule.objects.get(owner=context.client.user, type=UNMATCH_TYPE)
	data_json = json.loads(context.text)[0]
	start_hour = data_json['time_start']
	end_hour = data_json['time_end']
	answers = []
	for answer in data_json['reply']:
		answer_dict = {}
		if answer['reply_type'] == 'text':
			answer_dict['content']  = answer['reply_content']
			answer_dict['type']  = 'text'
		else:
			new_title = answer['reply_content']
			print '>>>>>>',context.client.user.id, new_title
			news = News.objects.filter(material__owner_id=context.client.user.id, title=new_title)[0]
			answer_dict['content']  = "%s" % news.id
			answer_dict['type']  = 'news'
		answers.append(answer_dict)

	if data_json['is_open'] == 'true':
		active_type = 1
	else:
		active_type = 0
	date = {"Mon":False,"Tue":False,"Wed":False,"Thu":False,"Fri":False,"Sat":False,"Sun":False}
	if data_json['Weeks'] == "Mon":
		date['Mon'] = True
	if data_json['Weeks'] == "Tue":
		date['Mon'] = True
	if data_json['Weeks'] == "Wed":
		date['Mon'] = True
	if data_json['Weeks'] == "Thu":
		date['Mon'] = True
	if data_json['Weeks'] == "Fri":
		date['Mon'] = True
	if data_json['Weeks'] == "Sat":
		date['Mon'] = True
	if data_json['Weeks'] == "Sun":
		date['Mon'] = True

	data = {
		"material_id": 0,
		"active_days":str(date),
		"answer": str(answers),
		"active_type": active_type,
		"start_hour": start_hour,
		"end_hour": end_hour
	}
	__process_unmatch_rule(data)
	context.client.post('/new_weixin/api/unmatch_rules/?_method=post', data)

<<<<<<< HEAD
@when(u'{user}访问关键词自动回复规则列表')
def step_impl(context, user):
	url = "/new_weixin/api/keyword_rules/?count_per_page=%s" % context.count_per_page
	print "context.count_per_page"
	response = context.client.get(url)
	context.response = response

@then(u'{user}获得关键词自动回复规则列表显示共{page_count}页')
def step_impl(context, user, page_count):
	content = context.response.content
	print json.loads(content)
	max_page = json.loads(content)['data']['pageinfo']['max_page']
	if int(page_count) != max_page:
		raise

@when(u'{user}访问关键词自动回复规则列表第{cur_page}页')
def step_impl(context, user, cur_page):
	context.cur_page = cur_page

@when(u"{user}浏览'下一页'")
def step_impl(context, user):
	cur_page = int(context.cur_page)
	context.cur_page = cur_page + 1

@when(u"{user}浏览'上一页'")
def step_impl(context, user):
	cur_page = int(context.cur_page)
	context.cur_page = cur_page - 1

@when(u"{user}设置关键词搜索条件")
def step_impl(context, user):
	data = json.loads(context.text)
	context.keyword = data['keyword']

@when(u"{user}编辑关键词自动回复规则'{rule_name}'")
def step_impl(context, user, rule_name):
	current_rule = Rule.objects.get(rule_name=rule_name)
	client = context.client
	context.rules = json.loads(context.text)
	#for rule in context.rules:
	__update_rule(context, context.rules , current_rule.id)
