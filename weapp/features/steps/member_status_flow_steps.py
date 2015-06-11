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
import urlparse


@when(u"{webapp_user_name}获得db中在{webapp_owner_name}公众号中的{attr}为'{variable_name}'")
def step_impl(context, webapp_user_name, webapp_owner_name, attr, variable_name):
	openid = '%s_%s' % (webapp_user_name, webapp_owner_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	social_account = SocialAccount.objects.get(openid=openid, webapp_id=webapp_id)
	if attr == 'sct':
		value = social_account.token
	elif attr == 'uuid':
		value = social_account.uuid
	elif attr == 'mt':
		member = MemberHasSocialAccount.objects.get(account=social_account, webapp_id=webapp_id).member
		value = member.token
	setattr(context, variable_name, value)	


@then(u"{webapp_user_name}在{webapp_owner_name}中的social_account与member已关联")
def step_impl(context, webapp_user_name, webapp_owner_name):
	sct = context.client.cookies['sct'].value
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	social_account = SocialAccount.objects.get(token=sct, webapp_id=webapp_id)
	member = MemberHasSocialAccount.objects.get(account=social_account, webapp_id=webapp_id).member
	bdd_util.tc.assertEquals(webapp_id, member.webapp_id)
	bdd_util.tc.assertEquals(webapp_user_name, member.username)


@then(u"{webapp_user_name}已是{webapp_owner_name}的会员")
def step_impl(context, webapp_user_name, webapp_owner_name):
	username = byte_to_hex(webapp_user_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member_count = Member.objects.filter(username_hexstr=username, webapp_id=webapp_id).count()
	bdd_util.tc.assertEquals(1, member_count)

	member = Member.objects.get(username_hexstr=username, webapp_id=webapp_id)
	webapp_user_count = WebAppUser.objects.filter(member_id=member.id).count()
	bdd_util.tc.assertEquals(1, webapp_user_count)


@then(u"{webapp_user_name}不是{webapp_owner_name}的会员")
def step_impl(context, webapp_user_name, webapp_owner_name):
	username = byte_to_hex(webapp_user_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member_count = Member.objects.filter(username_hexstr=username, webapp_id=webapp_id).count()
	bdd_util.tc.assertEquals(0, member_count)


@then(u"{webapp_user_name}分享的链接中的fmt为{webapp_user_name_2}在{webapp_owner_name}中的mt")
def step_impl(context, webapp_user_name, webapp_user_name_2, webapp_owner_name):
	openid = '%s_%s' % (webapp_user_name_2, webapp_owner_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	social_account = SocialAccount.objects.get(openid=openid, webapp_id=webapp_id)
	member = MemberHasSocialAccount.objects.get(account=social_account, webapp_id=webapp_id).member
	mt = member.token	

	query_strings = dict(urlparse.parse_qsl(urlparse.urlparse(context.shared_url).query))
	fmt = query_strings['fmt']

	bdd_util.tc.assertEquals(mt, fmt)


@then(u"{webapp_user_name}当前链接中的fmt为{webapp_user_name_2}在{webapp_owner_name}中的mt")
def step_impl(context, webapp_user_name, webapp_user_name_2, webapp_owner_name):
	openid = '%s_%s' % (webapp_user_name_2, webapp_owner_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	social_account = SocialAccount.objects.get(openid=openid, webapp_id=webapp_id)
	member = MemberHasSocialAccount.objects.get(account=social_account, webapp_id=webapp_id).member
	mt = member.token	

	query_strings = dict(urlparse.parse_qsl(urlparse.urlparse(context.last_url).query))
	fmt = query_strings['fmt']

	bdd_util.tc.assertEquals(mt, fmt)


@then(u"{webapp_user_name}分享的链接中的fmt为空")
def step_impl(context, webapp_user_name):
	query_strings = dict(urlparse.parse_qsl(urlparse.urlparse(context.shared_url).query))
	assert (not 'fmt' in query_strings), 'fmt CAN NOT be in query_strings'

@then(u"{webapp_user_name}当前链接中的fmt为空")
def step_impl(context, webapp_user_name):
	query_strings = dict(urlparse.parse_qsl(urlparse.urlparse(context.last_url).query))
	assert (not 'fmt' in query_strings), 'fmt CAN NOT be in query_strings'

@then(u"{webapp_user_name}在{webapp_owner_name}公众号中有{token}对应的webapp_user")
def step_impl(context, webapp_user_name, webapp_owner_name, token):
	if token == 'uuid':
		uuid = context.client.cookies['uuid'].value
		webapp_user_count = WebAppUser.objects.filter(token=uuid).count()
	elif token == 'mt':
		username = byte_to_hex(webapp_user_name)
		webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
		member = Member.objects.get(username_hexstr=username, webapp_id=webapp_id)
		webapp_user_count = WebAppUser.objects.filter(token=member.token).count()

	bdd_util.tc.assertEquals(1, webapp_user_count)


@then(u"{webapp_user_name}在{webapp_owner_name}公众号中有{count}个webapp_user")
def step_impl(context, webapp_user_name, webapp_owner_name, count):
	username = byte_to_hex(webapp_user_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member = Member.objects.get(username_hexstr=username, webapp_id=webapp_id)
	webapp_user_count = WebAppUser.objects.filter(member_id=member.id).count()

	bdd_util.tc.assertEquals(int(count), webapp_user_count)