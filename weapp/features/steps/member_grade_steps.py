# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from modules.member.models import MemberGrade


@Then(u"{user}能获取会员等级列表")
def step_impl(context, user):
	# if hasattr(context, 'client'):
	# 	context.client.logout()
	# context.client = bdd_util.login(user)
	client = context.client
	# user = UserFactory(username=user)
	json_data = json.loads(context.text)
	response = context.client.get('/mall2/member_grade_list/')
	member_grades = response.context['member_grades']
	#context.tc.assertEquals(len(member_grades), len(json_data))
	response_data = []
	for grade in member_grades:
		data_dict = {}
		data_dict['name'] = grade.name
		data_dict['discount'] =  grade.shop_discount
		if grade.is_auto_upgrade:
			data_dict['upgrade'] = u"自动升级"
		else:
			data_dict['upgrade'] = u"手动升级"
		response_data.append(data_dict)

	bdd_util.assert_list(json_data, response_data)


@When(u"{user}添加会员等级")
def step_impl(context, user):
	user = context.client.user
	json_data = json.loads(context.text)
	grades = []
	for content in json_data:
		if content['upgrade'] == u'手动升级':
			content['is_auto_upgrade'] = 0
		else:
			content['is_auto_upgrade'] = 1
		db_grade = MemberGrade.objects.filter(name=content['name'], webapp_id=user.get_profile().webapp_id)
		if len(db_grade) > 0:
			content['id'] = str(db_grade[0].id)
		grades.append(content)
	context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(grades)})

@Given(u"{user}添加会员等级")
def step_impl(context, user):
	context.execute_steps(u"when %s添加会员等级" % user)


# @When(u"{user}删除会员等级{name}")
# def step_impl(context, user, name):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)

# 	grade = MemberGrade.objects.get(webapp_id=user.get_profile().webapp_id, name=name)
# 	context.tc.assertEquals(name, grade.name)

# 	response = context.client.get('/webapp/user_center/grade/delete/%d/' % grade.id)