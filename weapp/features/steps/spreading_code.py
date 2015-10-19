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
from market_tools.tools.member_qrcode.models import *
from django.db.models import Q
from core import dev_util
from mall.promotion.models import Promotion, Coupon, CouponRule
"""
detail	

prize_source|0	 100
prize_type|0	3
reward	1
timestamp	
1444301019345


无
prize_source|0	 0
prize_type|0	0
reward	 1


有优惠券
prize_source|0	2605
prize_type|0	1
reward	1
"""

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

@when(u"{user}创建推广扫码")
def step_impl(context, user):
	if hasattr(context, 'client') and (context.client.user.username != user):
		context.client.logout()

	data = json.loads(context.text)
	post_data = {}
	post_data['reward'] = 1
	if data['prize_type'] == u'无':
		post_data['prize_source|0'] = 0
		post_data['prize_type|0'] = 0
		post_data['detail'] = data['page_description']
	elif data['prize_type'] == u'积分':
		post_data['prize_source|0'] = data['integral']
		post_data['prize_type|0'] = 3
		post_data['detail'] = data['page_description']
	elif data['prize_type'] == u'优惠券':
		coupon_name = data['coupon']
		user_id = bdd_util.get_user_id_for(user)
		coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_name, is_active=True)
		post_data['prize_source|0'] = coupon_rule.id
		post_data['prize_type|0'] = 1
		post_data['detail'] = data['page_description']


	context.client = bdd_util.login(user)
	client = context.client

	url = '/member/api/member_qrcode/'
	

	response = client.post(url, post_data)

	#context.qa_result = json.loads(response.content)


@Then(u"{user}获得推广扫码")
def step_impl(context, user):
	expected_data = json.loads(context.text)
	url = '/member/member_qrcode/'
	
	client = context.client
	response = client.get(url)
	member_qrcode_settings = response.context['member_qrcode_settings']

	award_content = response.context['award_content']

	current_data = {}
	if award_content.award_type == 0:
		current_data['prize_type'] = u'无'
		current_data['page_description'] = member_qrcode_settings.detail
	elif award_content.award_type == 1:
		current_data['prize_type'] = u'优惠券'
		current_data['page_description'] = member_qrcode_settings.detail
		coupon_rule = CouponRule.objects.get(id=award_content.award_content)
		current_data['coupon'] = coupon_rule.name
	elif award_content.award_type == 3:
		current_data['prize_type'] = u'积分'
		current_data['page_description'] = member_qrcode_settings.detail
		current_data['integral'] = int(award_content.award_content)

	bdd_util.assert_dict(expected_data, current_data)
	context.member_qrcode_settings = member_qrcode_settings

@When(u"{user}进入推广扫描链接")
def step_impl(context, user):
	url = "/workbench/jqm/preview/?module=market_tool:member_qrcode&model=settings&action=get&settings_id=%d&webapp_owner_id=%d&project_id=0&workspace_id=market_tool:member_qrcode" % (context.member_qrcode_settings.id,context.webapp_owner_id)

	response = context.client.get(bdd_util.nginx(url), follow=True)

	member_qrcode_settings = response.context['member_qrcode_settings']
	user_id = context.webapp_owner_id
	context.tc.assertEquals(member_qrcode_settings.id, context.member_qrcode_settings.id)
	context.tc.assertEquals(member_qrcode_settings.detail, context.member_qrcode_settings.detail)
	ticket = user
	if MemberQrcode.objects.filter(ticket=ticket).count() == 0:
		MemberQrcode.objects.create(owner_id=user_id, member_id=context.member.id, ticket=ticket, created_time=int(time.time()), expired_second=1800)

	context.ticket = ticket

@When(u"{ticket_user}扫描{user}的推广二维码关注{mp_user_name}公众号")
def step_impl(context, ticket_user, user, mp_user_name):
	old_cookies = context.client.cookies
	if hasattr(context, 'client') and (context.client.user.username != mp_user_name):
		context.client.logout()
	context.client = bdd_util.login(mp_user_name)
	client = context.client
	client.reset()

	mp_user = User.objects.get(username=mp_user_name)
	profile = UserProfile.objects.get(user_id=mp_user.id)
	openid = '%s_%s' % (ticket_user, mp_user_name)

	url = '/simulator/api/mp_user/qr_subscribe/?version=2'
	data = {
		"timestamp": "1402211023857",
		"webapp_id": profile.webapp_id,
		"from_user": openid,
		"ticket": user
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
	__fill_member_info(context, ticket_user, openid)
	#把会员设置为真实用户 add by duhao 2015-07-29
	Member.objects.update(is_for_test=False)
	time.sleep(1)
	