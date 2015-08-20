# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *

@given(u"{user}登录系统")
def step_impl(context, user):
	context.client = bdd_util.login(user, password=None, context=context)

@when(u"{user}添加会员分组")
def step_impl(context, user):
	MemberTag.objects.all().delete()
	client = context.client
	context.member_tags = json.loads(context.text)
	for member_tag in context.member_tags:
		data = member_tag
		response = client.post('/member/member_tags/get/', data)
	#response = client.post('/member/member_tags/get/', context.member_tags)

@then(u"{user}能获取会员分组列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/webapp/user_center/tags/')
	member_tags =response.context['member_tags']
	tag_list = []
	for tag in member_tags:
		tag_list.append({"name":tag.name})
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, tag_list)

# @given(u"{user}添加会员分组")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client

# 	response = client.get('/webapp/user_center/tags/')
# 	member_tags =response.context['member_tags']
# 	tag_list = []
# 	for tag in member_tags:
# 		tag_list.append({"name":tag.name})
# 	expected = json.loads(context.text)
# 	bdd_util.assert_list(expected, tag_list)

@when(u"{user}更新会员分组'{tag_name}'")
def step_impl(context, user, tag_name):
	client = context.client
	existed_member_tag = MemberTagFactory(name=tag_name)
	new_member_tag = json.loads(context.text)
	data = {
		'name': new_member_tag['name']
	}
	response = client.post('/webapp/user_center/tag/update/%d/' % existed_member_tag.id, data)

@when(u"{user}删除会员分组'{tag_name}'")
def step_impl(context, user, tag_name):
	existed_member_tag = MemberTagFactory(name=tag_name)
	res = context.client.get('/webapp/user_center/tag/delete/%d/' % existed_member_tag.id)



