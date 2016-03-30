# -*- coding: utf-8 -*-

from behave import *

from test import bdd_util

from mall.models import *
from modules.member.models import *


@then(u'{user}能获得weapp系统{member}拥有优惠券')
def step_impl(context, user, member):
	member_id = bdd_util.get_member_by_username(member, context.webapp_id).id
	if context.coupon_status is None:
		url = '/member/api/member_coupon/?id='+str(member_id)
	elif context.coupon_status == '全部':
		url = '/member/api/member_coupon/?id='+str(member_id)+'&filter_attr=status&filter_value=-1'
	elif context.coupon_status == '未使用':
		url = '/member/api/member_coupon/?id='+str(member_id)+'&filter_attr=status&filter_value=0'
	elif context.coupon_status == '已使用':
		url = '/member/api/member_coupon/?id='+str(member_id)+'&filter_attr=status&filter_value=1'
	elif context.coupon_status == '已过期':
		url = '/member/api/member_coupon/?id='+str(member_id)+'&filter_attr=status&filter_value=2'
	response = context.client.get(bdd_util.nginx(url))
	items = json.loads(response.content)['data']['items']
	expected = json.loads(context.text)

	actual = []
	for record in items:
		detail = record['coupon_detail'].split()[0]
		actual.append(dict(
			coupon_id=record['coupon_id'],
			name=record['coupon_name'],
			type=record['coupon_detail'].split()[1],
			get_time=record['provided_time'],
			money=detail[1:],
			status=record['coupon_state']
		))

	bdd_util.assert_list(actual, expected)


@then(u'{user}能获得weapp系统{member}拥有优惠券默认查询条件')
def step_impl(context, user, member):
	expected = json.loads(context.text)
	actual = []
	item = ()
	item['status'] = '全部'
	actual.append(item)
	bdd_util.assert_list(actual, expected)


@when(u'{user}设置优惠券状态查询条件')
def step_impl(context, user):
	expected = json.loads(context.text)
	context.coupon_status = expected['status']

