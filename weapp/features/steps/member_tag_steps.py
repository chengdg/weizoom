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
	__add_member_tag(context, user)

@given(u"{user}添加会员分组")
def step_impl(context, user):
	__add_member_tag(context, user)

def __add_member_tag(context, user):
	MemberTag.objects.all().delete()
	client = context.client
	context.member_tags = {}
	for tag_id, tag_name in json.loads(context.text).items():
		if tag_name != '未分组':
			tag_id = 'tag_id_{}'.format(int(tag_id.split('_')[2]) + 1)
		context.member_tags[tag_id] = tag_name
	response = client.post('/member/api/member_tags/',
		context.member_tags)

@then(u"{user}能获取会员分组列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/member/member_tags/')
	member_tags =response.context['member_tags']
	tag_list = []
	for tag in member_tags:
		tag_list.append({"name":tag.name,"group_membership":tag.count})
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, tag_list)


@when(u"{user}更新会员分组")
def step_impl(context, user):
	client = context.client
	new_member_tag = json.loads(context.text)
	response = client.post('/member/api/member_tags/' ,new_member_tag)


@when(u"{user}删除会员分组")
def step_impl(context, user):
	client = context.client
	new_member_tag = json.loads(context.text)
	response = client.post('/member/api/member_tags/' ,new_member_tag)




