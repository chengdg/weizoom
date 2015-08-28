# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *
from utils.string_util import byte_to_hex

@when(u"{user}选择会员")
def step_impl(context, user):
    context.member_ids = []
    for raw in context.table:
        query_hex = byte_to_hex(raw['member_name'])
        member = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex)
        context.member_ids.append(str(member.id))

@when(u"{user}批量修改等级")
def step_impl(context, user):
    member_ids = context.member_ids
    data = json.loads(context.text)[0]
    grade_name = data['member_rank']
    grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=grade_name).id
    args = {}
    if data['modification_method'] == '给选中的人修改等级':
        if not member_ids:
            return
        args['update_status'] = 'selected'
        args['ids'] = '-'.join(member_ids)
    elif data['modification_method'] == '给筛选出来的所有人修改等级':
        args['update_status'] = 'all'

    args['grade_id'] = grade_id
    response = context.client.post('/member/api/grade/batch_update/', args)
    bdd_util.assert_api_call_success(response)
# @Then(u"{user}能获取会员等级列表")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)
# 	response = context.client.get('/webapp/user_center/grades/')
# 	member_grades = response.context['member_grades']
# 	#context.tc.assertEquals(len(member_grades), len(json_data))
# 	response_data = []
# 	for grade in member_grades:
# 		data_dict = {}
# 		data_dict['name'] = grade.name
# 		data_dict['shop_discount'] =  str(grade.shop_discount)+"%"
# 		if grade.is_auto_upgrade:
# 			data_dict['upgrade'] = u"自动升级"
# 		else:
# 			data_dict['upgrade'] = u"不自动升级"
# 		response_data.append(data_dict)

# 	bdd_util.assert_list(response_data, json_data)

# def _add_member_grade(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)
# 	for content in json_data:
# 		if content['upgrade'] == u'不自动升级':
# 			content['is_auto_upgrade'] = 0
# 		else:
# 			content['is_auto_upgrade'] = 1
# 			content['upgrade_lower_bound'] = int(content['shop_discount'].replace('%',''))
# 		content['shop_discount'] = content['shop_discount'].replace('%','')
# 		if MemberGrade.objects.filter(name=content['name'], webapp_id=user.get_profile().webapp_id).count() == 0:
# 			response = context.client.post('/webapp/user_center/grade/create/', content)

# @When(u"{user}添加会员等级")
# def step_impl(context, user):
# 	_add_member_grade(context, user)

# @Given(u"{user}添加会员等级")
# def step_impl(context, user):
# 	_add_member_grade(context, user)

# @When(u"{user}更新会员等级{name}")
# def step_impl(context, user, name):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)
# 	if name.startswith("'") and name.endswith("'"):
# 		name = name.replace("'","")
# 	grade = MemberGrade.objects.get(webapp_id=user.get_profile().webapp_id, name=name)
# 	context.tc.assertEquals(name, grade.name)
# 	for content in json_data:
# 		if content['upgrade'] == u'不自动升级':
# 			content['is_auto_upgrade'] = 0
# 		else:
# 			content['is_auto_upgrade'] = 1
# 			content['upgrade_lower_bound'] = int(content['shop_discount'].replace('%',''))
# 		if content.has_key('integral'):
# 			integral = content['integral']
# 			if integral.find('%') > 0:
# 				integral = integral.replace('%','')
# 			content['usable_integral_percentage_in_order'] = integral
# 		content['shop_discount'] = content['shop_discount'].replace('%','')
# 		response = context.client.post('/webapp/user_center/grade/update/%d/' % grade.id, content)


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