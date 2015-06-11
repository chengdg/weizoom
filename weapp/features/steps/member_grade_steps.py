# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import * 


@Then(u"{user}能获取会员等级列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	json_data = json.loads(context.text)
	response = context.client.get('/webapp/user_center/grades/')
	member_grades = response.context['member_grades']
	#context.tc.assertEquals(len(member_grades), len(json_data))
	response_data = []
	for grade in member_grades:
		data_dict = {}
		data_dict['name'] = grade.name
		data_dict['shop_discount'] =  str(grade.shop_discount)+"%"
		if grade.is_auto_upgrade:
			data_dict['upgrade'] = u"自动升级"
		else:
			data_dict['upgrade'] = u"不自动升级"
		response_data.append(data_dict)

	bdd_util.assert_list(response_data, json_data)

@When(u"{user}添加会员等级")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	json_data = json.loads(context.text)
	for content in json_data:
		if content['upgrade'] == u'不自动升级':
			content['is_auto_upgrade'] = 0
		else:
			content['is_auto_upgrade'] = 1
			content['upgrade_lower_bound'] = int(content['shop_discount'].replace('%',''))
		content['shop_discount'] = content['shop_discount'].replace('%','')
		if MemberGrade.objects.filter(name=content['name'], webapp_id=user.get_profile().webapp_id).count() == 0:
			response = context.client.post('/webapp/user_center/grade/create/', content)

@Given(u"{user}添加会员等级")
def step_impl(context, user):
	context.execute_steps(u"when %s添加会员等级" % user)

@When(u"{user}更新会员等级{name}")
def step_impl(context, user, name):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	json_data = json.loads(context.text)
	if name.startswith("'") and name.endswith("'"):
		name = name.replace("'","")
	grade = MemberGrade.objects.get(webapp_id=user.get_profile().webapp_id, name=name)
	context.tc.assertEquals(name, grade.name)
	for content in json_data:
		if content['upgrade'] == u'不自动升级':
			content['is_auto_upgrade'] = 0
		else:
			content['is_auto_upgrade'] = 1
			content['upgrade_lower_bound'] = int(content['shop_discount'].replace('%',''))
		if content.has_key('integral'):
			integral = content['integral']
			if integral.find('%') > 0:
				integral = integral.replace('%','')
			content['usable_integral_percentage_in_order'] = integral
		content['shop_discount'] = content['shop_discount'].replace('%','')
		response = context.client.post('/webapp/user_center/grade/update/%d/' % grade.id, content)


@When(u"{user}删除会员等级{name}")
def step_impl(context, user, name):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	json_data = json.loads(context.text)

	grade = MemberGrade.objects.get(webapp_id=user.get_profile().webapp_id, name=name)
	context.tc.assertEquals(name, grade.name)

	response = context.client.get('/webapp/user_center/grade/delete/%d/' % grade.id)