# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from account.models import *

@when(u"{user}添加第一个员工账号")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	context.employees = json.loads(context.text)
	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 0)
	context.client.get('/account/sub_user/create/')
	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 1)
	sub_user = UserHasSubUser.objects.filter(user=user)[0]
	context.tc.assertEquals(sub_user.is_active, False)
	context.tc.assertEquals(sub_user.sub_user.username, '001@%s' % user.username)
	
	employee = context.employees[0]
	employee['id'] = sub_user.sub_user.id
	response = client.post('/account/sub_user/create/', employee)

@then(u"{user}能获取添加的员工账号")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)

	context.employees = json.loads(context.text)

	response = context.client.get('/account/sub_users/')
	response_datas = response.context['user_has_sub_users']
	print '--------------'
	print context.employees
	print '======'
	print response_datas
	for employee in context.employees:
		print ']]]]]]]]]]]]]]]]]'
		print employee['employees_account']
		print employee['remark']
		print response_datas.filter(sub_user__username=employee['employees_account'], remark=employee['remark']).count()
		context.tc.assertEquals(response_datas.filter(sub_user__username=employee['employees_account'], remark=employee['remark']).count() , 1)


	
@when(u"{user}添加第二个员工账号")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	context.employees = json.loads(context.text)
	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 1)
	context.client.get('/account/sub_user/create/')
	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 2)
	sub_users = UserHasSubUser.objects.filter(sub_user__username='002@%s' % user.username)
	context.tc.assertEquals(sub_users.count(), 1)
	context.tc.assertEquals(sub_users[0].is_active, False)
	
	employee = context.employees[0]
	employee['id'] = sub_users[0].sub_user.id
	response = client.post('/account/sub_user/create/', employee)


@when(u"{user}添加第三个员工账号")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	context.employees = json.loads(context.text)
	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 2)
	context.client.get('/account/sub_user/create/')
	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 3)
	sub_users = UserHasSubUser.objects.filter(sub_user__username='003@%s' % user.username)
	context.tc.assertEquals(sub_users.count(), 1)
	context.tc.assertEquals(sub_users[0].is_active, False)
	
	employee = context.employees[0]
	employee['id'] = sub_users[0].sub_user.id
	response = client.post('/account/sub_user/create/', employee)

@given(u"{user}已有的员工账号")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)

	context.employees = json.loads(context.text)

	response = context.client.get('/account/sub_users/')
	response_datas = response.context['user_has_sub_users']
	print '--------------'
	print context.employees
	print '======'
	print response_datas
	for employee in context.employees:
		print ']]]]]]]]]]]]]]]]]'
		print employee['employees_account']
		print employee['remark']
		print response_datas.filter(sub_user__username=employee['employees_account'], remark=employee['remark']).count()
		context.tc.assertEquals(response_datas.filter(sub_user__username=employee['employees_account'], remark=employee['remark']).count() , 1)


@when(u"{user}删除员工账号003@jobs")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	context.employees = json.loads(context.text)

	context.tc.assertEquals(UserHasSubUser.objects.filter(user=user).count(), 3)
	sub_users = UserHasSubUser.objects.filter(sub_user__username=context.employees[0]['employees_account'])
	
	id = sub_users[0].sub_user.id
	
	response = client.get('/account/sub_user/delete/?user_id=%d' % id)

