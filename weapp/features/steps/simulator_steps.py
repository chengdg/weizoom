# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from account.models import UserProfile

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from account.social_account.models import SocialAccount
from modules.member.models import WebAppUser, Member, MemberHasSocialAccount
from django.db.models import Q
from core import dev_util

############################################################################
# __fill_member_info: 在context中放入member, webapp_user, social_account
############################################################################
def __fill_member_info(context, username, openid):
	context.webapp_user = None
	context.member = None
	context.social_account = None

	#获得social_account
	social_account = SocialAccount.objects.get(openid=openid)
	relation = MemberHasSocialAccount.objects.get(account_id=social_account.id, webapp_id=context.webapp_id)

	#获得member
	member = Member.objects.get(id=relation.member_id)
	#由于mode=='develop'或者social account的is_for_test=True，导致member中的username都是'预览'
	#这里要修复username_hexstr
	from utils.string_util import byte_to_hex
	if isinstance(username, unicode):
		member_nickname_str = username.encode('utf-8')
	else:
		member_nickname_str = username
	username_hexstr = byte_to_hex(member_nickname_str)
	if member.username_hexstr != username_hexstr:
		Member.objects.filter(id=member.id).update(username_hexstr=username_hexstr)
		member.username_hexstr = username_hexstr

	#获得webapp_user
	if WebAppUser.objects.filter(member_id=member.id, webapp_id=context.webapp_id).filter(~Q(member_id=0)).count() > 0:
		webapp_user = WebAppUser.objects.filter(member_id=member.id, webapp_id=context.webapp_id).filter(~Q(member_id=0))[0]

	webapp_user = WebAppUser.objects.filter(member_id=member.id, webapp_id=context.webapp_id)[0]

	#填充context
	context.webapp_user = webapp_user
	context.member = member
	context.social_account = social_account


@when(u"{user}在模拟器中发送消息'{message}'")
def step_impl(context, user, message):
	if hasattr(context, 'client') and (context.client.user.username != user):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	url = '/simulator/api/weixin/send/'
	data = {
		"content": message,
		"timestamp": "1402211023857",
		"webapp_id": client.user.profile.webapp_id,
		"weixin_user_fakeid": "	weizoom_default_fakeid",
		"weixin_user_name": "weizoom"
	}
	response = client.post(url, data)
	context.qa_result = json.loads(response.content)


@when(u"{user}在微信中向{mp_user_name}的公众号发送消息'{message}'")
def step_impl(context, user, mp_user_name, message):
	if hasattr(context, 'client') and (context.client.user.username != user):
		context.client.logout()
	# 用user登录是为了在模拟器中辨识user身份
	context.client = bdd_util.login(user)
	client = context.client

	mp_user = User.objects.get(username=mp_user_name)
	profile = UserProfile.objects.get(user_id=mp_user.id)

	url = '/simulator/api/weixin/send/'
	data = {
		"content": message,
		"timestamp": "1402211023857",
		"webapp_id": profile.webapp_id,
		#"weixin_user_fakeid": "weizoom_default_fakeid",
		"weixin_user_fakeid": "weizoom_fakeid_{}".format(user),
		#"weixin_user_name": "weizoom"
		"weixin_user_name": user
	}
	response = client.post(url, data)
	context.qa_result = json.loads(response.content)


@when(u"{user}关注{mp_user_name}的公众号")
def step_impl(context, user, mp_user_name):
	old_cookies = context.client.cookies
	if hasattr(context, 'client') and (context.client.user.username != mp_user_name):
		context.client.logout()
	context.client = bdd_util.login(mp_user_name)
	client = context.client
	client.reset()

	mp_user = User.objects.get(username=mp_user_name)
	profile = UserProfile.objects.get(user_id=mp_user.id)
	openid = '%s_%s' % (user, mp_user_name)

	url = '/simulator/api/mp_user/subscribe/?version=2'
	data = {
		"timestamp": "1402211023857",
		"webapp_id": profile.webapp_id,
		"from_user": openid
	}
	response = client.post(url, data)
	response_data = json.loads(response.content)
	context.qa_result = response_data
	context.tc.assertEquals(200, response_data['code'])

	if getattr(context, 'in_manual_delete_cookie_mode', False):
		context.client.cookies = old_cookies
	else:
		pass

	webapp_owner_id = bdd_util.get_user_id_for(mp_user_name)
	context.webapp_owner_id = webapp_owner_id
	context.webapp_id = profile.webapp_id
	__fill_member_info(context, user, openid)
	#把会员设置为真实用户 add by duhao 2015-07-29
	Member.objects.update(is_for_test=False)


@when(u"{user}关注{mp_user_name}的公众号于'{date}'")
def step_impl(context, user, mp_user_name, date):
	context.execute_steps(u"when %s关注%s的公众号" % (user, mp_user_name))
	date = bdd_util.get_date(date).strftime('%Y-%m-%d')
	latest_member = Member.objects.all().order_by('-id')[0]
	latest_member.created_at = '%s 00:00:00' % date
	latest_member.save()


@when(u"{webapp_user_name}访问{webapp_owner_name}的webapp")
def step_impl(context, webapp_user_name, webapp_owner_name):
	client = context.client
	openid = '%s_%s' % (webapp_user_name, webapp_owner_name)

	#获取sct cookie
	sct = SocialAccount.objects.get(openid=openid).token

	#重新获取sct cookie
	if getattr(context, 'in_manual_delete_cookie_mode', False):
		pass
	else:
		client.reset()
	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
	dev_util.print_cookies(context.client, 'cookie1')
	url = '/workbench/jqm/preview/?module=mall&model=products&action=list&category_id=0&workspace_id=mall&webapp_owner_id=%d&sct=%s' % (webapp_owner_id, sct)
	response = client.get(bdd_util.nginx(url))
	has_sct = False
	for cookie_value in client.cookies.values():
		if 'sct' == cookie_value.key:
			has_sct = True
			break
	if not has_sct:
		assert False, '获取sct cookie失败'
	if response.status_code == 302:
		print("[info]: redirect by replace sct by fmt in url")
		dev_util.print_cookies(context.client, 'cookie2')
		redirect_url = response['Location']
		response = client.get(bdd_util.nginx(response['Location']))
		if response.status_code == 302:
			redirect_url = response['Location']
			response = client.get(bdd_util.nginx(response['Location']))
		assert response.status_code == 200
		context.last_url = redirect_url
	else:
		context.last_url = url

	profile = UserProfile.objects.get(user_id=webapp_owner_id)
	context.webapp_owner_id = webapp_owner_id
	context.sct_cookie = sct
	context.webapp_id = profile.webapp_id
	__fill_member_info(context, webapp_user_name, openid)


@given(u"{user}关注{mp_user_name}的公众号")
def step_impl(context, user, mp_user_name):
	context.execute_steps(u"when %s关注%s的公众号" % (user, mp_user_name))


@then(u"{user}收到自动回复'{answer}'")
def step_impl(context, user, answer):
	result = context.qa_result["data"]
	beg = result.find('<div class="content">') + len('<div class="content">')
	end = result.find('</div>', beg)
	actual = result[beg:end]

	expected = answer
	if expected == 'None':
		expected = ''
	context.tc.assertEquals(expected, actual)


@then(u"{user}收到自动回复")
def step_impl(context, user):
	print(context.qa_result)
	print(context.text)


@when("清空浏览器")
def step_impl(context):
	context.client.reset()