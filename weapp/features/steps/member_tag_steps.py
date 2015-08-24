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
	response = client.post('/member/member_tags/get/',
		context.member_tags)

@given(u"{user}添加会员分组")
def step_impl(context, user):
	MemberTag.objects.all().delete()
	client = context.client
	context.member_tags = json.loads(context.text)
	response = client.post('/member/member_tags/get/',
		context.member_tags)

@then(u"{user}能获取会员分组列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/member/member_tags/get/')
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
	response = client.post('/member/member_tags/get/' ,new_member_tag)


@when(u"{user}删除会员分组")
def step_impl(context, user):
	client = context.client
	new_member_tag = json.loads(context.text)
	response = client.post('/member/member_tags/get/' ,new_member_tag)




