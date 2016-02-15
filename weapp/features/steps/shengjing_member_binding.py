# -*- coding: utf-8 -*-

import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from apps.customerized_apps.shengjing.models import *

from utils.string_util import byte_to_hex

def __get_user(user_name):
	return User.objects.get(username=user_name)
@Given(u"{user}配置绑定成功后给好友增加积分")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	client = context.client
	content = json.loads(context.text)
	user_profile = __get_user(user).get_profile()

	sttings,created = ShengjingIntegralStrategySttings.objects.get_or_create(webapp_id=user_profile.webapp_id)
	sttings.binding_for_father = int(content['interal'])
	sttings.save()

@Given(u"手机号{phone_a}是胜景会员，手机号{phone_b}不是胜景会员")
def step_impl(context, phone_a, phone_b):
	pass

@Given(u"{user}拥有会员{member_A}和{member_B},并且A是B的上级节点")
def step_impl(context, user, member_A, member_B):
	context.client = bdd_util.login(user)
	client = context.client

	user_profile = __get_user(user).get_profile()

	try:
		member_nickname_str_a = member_A.encode('utf-8')
		member_nickname_str_b = member_B.encode('utf-8')
	except:
		member_nickname_str_a = member_A
		member_nickname_str_b = member_B

	username_hexstr_a = byte_to_hex(member_nickname_str_a)
	username_hexstr_b = byte_to_hex(member_nickname_str_b)
	context.tc.assertEquals(1,  Member.objects.filter(username_hexstr=username_hexstr_a, webapp_id=user_profile.webapp_id).count())
	context.tc.assertEquals(1,  Member.objects.filter(username_hexstr=username_hexstr_b, webapp_id=user_profile.webapp_id).count())
	member_A = Member.objects.filter(username_hexstr=username_hexstr_a, webapp_id=user_profile.webapp_id)[0]
	member_B = Member.objects.filter(username_hexstr=username_hexstr_b, webapp_id=user_profile.webapp_id)[0]
	if MemberFollowRelation.objects.filter(member_id=member_A.id, follower_member_id=member_B.id, is_fans=True).count() == 0:
		MemberFollowRelation.objects.create(member_id=member_A.id, follower_member_id=member_B.id, is_fans=True)


@When(u"{user}的会员{member_A}和{member_B}访问绑定信息页面时输入以下内容")
def step_impl(context, user, member_A, member_B):
	user =  __get_user(user)
	user_profile = user.get_profile()

	try:
		member_nickname_str_a = member_A.encode('utf-8')
		member_nickname_str_b = member_B.encode('utf-8')
	except:
		member_nickname_str_a = member_A
		member_nickname_str_b = member_B

	username_hexstr_a = byte_to_hex(member_nickname_str_a)
	username_hexstr_b = byte_to_hex(member_nickname_str_b)

	member_a = Member.objects.filter(username_hexstr=username_hexstr_a, webapp_id=user_profile.webapp_id)[0]
	account_a  = MemberHasSocialAccount.objects.filter(member=member_a)[0].account

	member_b = Member.objects.filter(username_hexstr=username_hexstr_b, webapp_id=user_profile.webapp_id)[0]
	account_b  = MemberHasSocialAccount.objects.filter(member=member_b)[0].account

	content = json.loads(context.text)

	data_a = content['member_a']
	data_b = content['member_b']

	post_data_a = {
		'number': data_a['number'],
		'captcha': data_a['captcha'],
		'member_id': member_a.id
	}

	post_data_b = {
		'number': data_b['number'],
		'captcha': data_b['captcha'],
		'member_id': member_b.id
	}

	response = context.client.post('/apps/shengjing/user_center/api/record_binding_phone/', post_data_a)
	context.tc.assertEquals(1, ShengjingBindingMember.objects.filter(member_id=member_a.id, phone_number=post_data_a['number'], captcha=post_data_a['captcha'], webapp_id=user_profile.webapp_id).count())
	if ShengjingBindingMember.objects.filter(member_id=member_a.id, phone_number=post_data_a['number'], captcha=post_data_a['captcha'], webapp_id=user_profile.webapp_id).count() > 0:
		binding_memnber = ShengjingBindingMember.objects.filter(member_id=member_a.id, phone_number=post_data_a['number'], captcha=post_data_a['captcha'], webapp_id=user_profile.webapp_id)[0]
		ShengjingBindingMemberInfo.objects.create(binding=binding_memnber,name=member_a.username_hexstr,status=1)

	context.client.post('/apps/shengjing/user_center/api/record_binding_phone/', post_data_b)
	context.tc.assertEquals(1, ShengjingBindingMember.objects.filter(member_id=member_b.id, phone_number=post_data_b['number'], captcha=post_data_b['captcha'], webapp_id=user_profile.webapp_id).count())

@Then(u"{user}可以得到的绑定信息")
def step_impl(context, user):
	user =  __get_user(user)
	user_profile = user.get_profile()
	content = json.loads(context.text)
	data_a = content['a']
	data_b = content['b']
	data_a_dict = {
		'number': data_a['number'],
		'captcha': data_a['captcha'],
		'status': 1 if data_a['is_student'] == '1' else 0
	}

	data_b_dict = {
		'number': data_b['number'],
		'captcha': data_b['captcha'],
		'status': 1 if data_b['is_student'] == '1' else 0
	}
	binding_memnbe_a = ShengjingBindingMember.objects.filter(phone_number=data_a_dict['number'], captcha=data_a_dict['captcha'], webapp_id=user_profile.webapp_id)
	binding_memnbe_b = ShengjingBindingMember.objects.filter(phone_number=data_b_dict['number'], captcha=data_b_dict['captcha'], webapp_id=user_profile.webapp_id)
	context.tc.assertEquals(1, binding_memnbe_a.count())
	context.tc.assertEquals(1, ShengjingBindingMemberInfo.objects.filter(binding=binding_memnbe_a[0], status=data_a_dict['status']).count())
	context.tc.assertEquals(1, binding_memnbe_b.count())
	context.tc.assertEquals(1, ShengjingBindingMemberInfo.objects.filter(binding=binding_memnbe_a[0]).count())

@When(u"{user}会员{member_B}进入绑定个人信息页面,输入以下信息")
def step_impl(context, user,member_B):
	user =  __get_user(user)
	user_profile = user.get_profile()
	content = json.loads(context.text)
	member_A = 'A'
	try:
		member_nickname_str_a = member_A.encode('utf-8')
		member_nickname_str_b = member_B.encode('utf-8')
	except:
		member_nickname_str_a = member_A
		member_nickname_str_b = member_B

	username_hexstr_a = byte_to_hex(member_nickname_str_a)
	username_hexstr_b = byte_to_hex(member_nickname_str_b)

	member_a = Member.objects.filter(username_hexstr=username_hexstr_a, webapp_id=user_profile.webapp_id)[0]
	account_a  = MemberHasSocialAccount.objects.filter(member=member_a)[0].account

	member_b = Member.objects.filter(username_hexstr=username_hexstr_b, webapp_id=user_profile.webapp_id)[0]
	account_b  = MemberHasSocialAccount.objects.filter(member=member_b)[0].account

	member_b = Member.objects.filter(username_hexstr=username_hexstr_b, webapp_id=user_profile.webapp_id)[0]
	account_b  = MemberHasSocialAccount.objects.filter(member=member_b)[0].account
	binding_member = ShengjingBindingMember.objects.filter(member_id=member_b.id)[0]

	name = content['name']
	position = content['position']
	company = content['company']
	post_data = {
		'name': name,
		'position': position,
		'company': company,
		'binding_member_id': binding_member.id
	}

	url = '/workbench/jqm/preview/?module=customerized_apps:shengjing:user_center&model=bingding_info&action=get&workspace_id=mall&webapp_owner_id=%s&sct=%s' % (user.id, account_b.token)
	response =  context.client.post(bdd_util.nginx(url), post_data)
	# print('-----------------------')
	# print(response)
	# print('------------------------aa')

	# context.tc.assertEquals(1, ShengjingBindingMemberInfo.objects.filter(binding=binding_member).count())
	# context.tc.assertEquals(10, member_a.interal)

