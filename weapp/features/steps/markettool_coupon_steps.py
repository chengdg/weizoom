# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.mall.models import *
from account.social_account.models import SocialAccount
from modules.member.models import WebAppUser, Member, MemberHasSocialAccount
from mall.promotion.models import *


def __add_coupon_rule(context, coupon_rule, webapp_owner_name):
	data = {
		"name": coupon_rule['name'],
		"money": coupon_rule['money'],
		"limit_counts": coupon_rule.get('limit_counts', 9999),
		"count": coupon_rule.get("count", 5),
		"member_grade": 0,
		"start_date": '%s 00:00' % bdd_util.get_date_str(coupon_rule['start_date']),
		"end_date": '%s 00:00' % bdd_util.get_date_str(coupon_rule['end_date'])
	}

	if not "using_limit" in coupon_rule:
		data['is_valid_restrictions'] = '0'
	else:
		data['is_valid_restrictions'] = '1'
		using_limit = coupon_rule["using_limit"]
		end = using_limit.find(u'元')
		data['valid_restrictions'] = using_limit[1:end]
	if "coupon_product" in coupon_rule:
		data['limit_product'] = 1
		webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
		data['product_ids'] = Product.objects.get(owner_id=webapp_owner_id, name=coupon_rule['coupon_product']).id

	url = '/mall_promotion/api/coupon_rules/create/'
	response = context.client.post(url, data)
	context.tc.assertEquals(200, response.status_code)

	if 'coupon_id_prefix' in coupon_rule:
		latest_coupon_rule = CouponRule.objects.all().order_by('-id')[0]
		index = 1
		coupon_id_prefix = coupon_rule['coupon_id_prefix']
		for coupon in Coupon.objects.filter(coupon_rule=latest_coupon_rule):
			coupon_id = '%s%d' % (coupon_id_prefix, index)
			Coupon.objects.filter(id=coupon.id).update(coupon_id=coupon_id)
			index += 1


###################################################################################
# __get_member_by_openid: 根据openid获得member
###################################################################################
def __get_member_by_openid(webapp_id, openid):
	social_account = SocialAccount.objects.get(openid=openid)
	relation = MemberHasSocialAccount.objects.get(account_id=social_account.id, webapp_id=webapp_id)
	member = Member.objects.get(id=relation.member_id)
	
	return member


###################################################################################
# __send_coupons: webapp_owner发放优惠券
###################################################################################
def __send_coupons(context, webapp_owner_name, type):
	from market_tools.tools.coupon.api_views import SEND_COUPON_OF_MEMBER, SEND_COUPON_OF_TAG, SEND_COUPON_OF_GRADE
	if type == u'会员':
		type = SEND_COUPON_OF_MEMBER
	else:
		type = -1

	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
	coupon_info = json.loads(context.text)
	coupon_rule_name = coupon_info['coupon_rule']
	coupon_rule = CouponRule.objects.get(owner_id=webapp_owner_id, name=coupon_rule_name, is_active=True)

	count = coupon_info['count']

	member_names = coupon_info['members']
	member_ids = []
	for member_name in member_names:
	 	openid = u'%s_%s' % (member_name, webapp_owner_name)
	 	member = __get_member_by_openid(context.webapp_id, openid)
	 	member_ids.append(str(member.id))

	member_ids = '_'.join(member_ids)

	url = '/market_tools/coupon/api/coupons/send/'
	data = {
		"type": type,
		"count": count,
		"rule_id": coupon_rule.id,
		"ids": member_ids
	}

	response = context.client.post(url, data)
	bdd_util.assert_api_call_success(response)

	#将coupon_id改为指定的coupon_id
	new_created_coupons = Coupon.objects.filter(owner_id=webapp_owner_id).order_by('-id')[:count]
	expected_coupon_ids = coupon_info['coupon_ids']
	expected_coupon_ids.reverse()
	for index, coupon in enumerate(new_created_coupons):
		Coupon.objects.filter(coupon_id=coupon.coupon_id).update(coupon_id=expected_coupon_ids[index])

	#修改发放时间和过期时间
	if 'expire_date' in coupon_info:
		today = datetime.today()
		if coupon_info['expire_date'] == u'昨天':
			expire_date = today - timedelta(1)
		elif coupon_info['expire_date'] == u'前天':
			expire_date = today - timedelta(2)
		else:
			pass

		new_created_coupon_ids = [coupon.id for coupon in new_created_coupons]
		Coupon.objects.filter(id__in=new_created_coupon_ids).update(expired_time=expire_date)


@when(u'{user_name}添加优惠券规则')
def step_impl(context, user_name):
	coupon_rules = json.loads(context.text)
	if type(coupon_rules) == dict:
		coupon_rules = [coupon_rules]

	for coupon_rule in coupon_rules:
		__add_coupon_rule(context, coupon_rule, user_name)
		time.sleep(1)


@given(u'{user_name}已添加了优惠券')
def step_impl(context, user_name):
	coupon_rules = json.loads(context.text)
	if type(coupon_rules) == dict:
		coupon_rules = [coupon_rules]

	for coupon_rule in coupon_rules:
		__add_coupon_rule(context, coupon_rule, user_name)


@then(u"{user_name}能获得优惠券规则'{coupon_rule_name}'")
def step_impl(context, user_name, coupon_rule_name):
	user_id = bdd_util.get_user_id_for(user_name)
	coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
	url = '/market_tools/coupon/coupon_rule/update/?rule_id=%d' % coupon_rule.id
	response = context.client.get(url)

	coupon_rule = response.context['coupon_rule']
	coupon_rule.expire_days = coupon_rule.valid_days
	coupon_rule.using_limit = u'无限制' if coupon_rule.valid_restrictions == -1 else (u'满%d元可以使用' % coupon_rule.valid_restrictions)
	#coupon_rule.can_delete = u'是' if coupon_rule.can_delete else u'否'

	expected = json.loads(context.text)
	actual = coupon_rule
	bdd_util.assert_dict(expected, actual)


@then(u'{user_name}能获得优惠券规则列表')
def step_impl(context, user_name):
	url = '/market_tools/coupon/'
	response = context.client.get(url)
	coupon_rules = response.context['coupon_rules']

	for coupon_rule in coupon_rules:
		coupon_rule.expire_days = coupon_rule.valid_days
		coupon_rule.using_limit = u'无限制' if coupon_rule.valid_restrictions == -1 else (u'满%d元可以使用' % coupon_rule.valid_restrictions)

	expected = json.loads(context.text)
	actual = coupon_rules
	bdd_util.assert_list(expected, actual)


@when(u"{user_name}更新优惠券规则'{coupon_rule_name}'为")
def step_impl(context, user_name, coupon_rule_name):
	user_id = bdd_util.get_user_id_for(user_name)
	coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
	url = '/market_tools/coupon/coupon_rule/update/?rule_id=%d' % coupon_rule.id

	name = json.loads(context.text)['name']
	data = {
		"name": name
	}

	response = context.client.post(url, data)


@when(u"{user_name}删除优惠券规则'{coupon_rule_name}'")
def step_impl(context, user_name, coupon_rule_name):
	user_id = bdd_util.get_user_id_for(user_name)
	coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
	url = '/market_tools/coupon/coupon_rule/delete/?rule_id=%d' % coupon_rule.id

	response = context.client.get(url)


@when(u"{user_name}手工为优惠券规则生成优惠券")
def step_impl(context, user_name):
	user_id = bdd_util.get_user_id_for(user_name)
	info = json.loads(context.text)
	coupon_rule_name = info['coupon_rule']
	count = info['count']

	coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
	url = '/market_tools/coupon/api/manual_coupons/create/'
	data = {
		"rule_id": coupon_rule.id,
		"count": count
	}

	response = context.client.post(url, data)

	provided_time = None
	if 'provided_time' in info:
		today = datetime.today()
		if info['provided_time'] == u'前天':
			provided_time = today - timedelta(2)

	if 'coupon_ids' in info:
		#将coupon_id改为指定的coupon_id
		new_created_coupons = Coupon.objects.filter(owner_id=user_id).order_by('-id')[:count]
		expected_coupon_ids = info['coupon_ids']
		expected_coupon_ids.reverse()
		for index, coupon in enumerate(new_created_coupons):
			if provided_time:
				expired_time = provided_time + timedelta(coupon_rule.valid_days)
				Coupon.objects.filter(coupon_id=coupon.coupon_id).update(coupon_id=expected_coupon_ids[index], provided_time=provided_time, expired_time=expired_time)
			else:
				Coupon.objects.filter(coupon_id=coupon.coupon_id).update(coupon_id=expected_coupon_ids[index])


@then(u"{user_name}能获得优惠券列表")
def step_impl(context, user_name):
	url = '/market_tools/coupon/api/records/get/'
	response = context.client.get(url)
	coupons = json.loads(response.content)['data']['items']

	for coupon in coupons:
		coupon['coupon_rule'] = coupon['rule_name']
		coupon['create_date'] = coupon['provided_time']
		coupon['expire_date'] = coupon['expired_time']
		if coupon['status'] == COUPON_STATUS_UNUSED:
			coupon['status'] = u'未使用'
		elif coupon['status'] == COUPON_STATUS_USED:
			coupon['status'] = u'已使用'
		elif coupon['status'] == COUPON_STATUS_EXPIRED:
			coupon['status'] = u'已过期'
		else:
			coupon['status'] = u'unknown'

		if coupon['is_manual_generated']:
			coupon['target'] = u'手工'
		else:
			coupon['target'] = coupon['member']['username_for_html']

		coupon['consumer'] = coupon['consumer']['username_for_html']
		coupon['money'] = float(coupon['money'])

	#处理expected中的参数
	today = datetime.now()
	tomorrow = today + timedelta(1)
	day_after_tomorrow = tomorrow + timedelta(1)
	yesterday = today - timedelta(1)
	day_before_yesterday = yesterday - timedelta(1)
	today = today.strftime('%m月%d日').decode('utf-8')
	tomorrow = tomorrow.strftime('%m月%d日').decode('utf-8')
	day_after_tomorrow = day_after_tomorrow.strftime('%m月%d日').decode('utf-8')
	yesterday = yesterday.strftime('%m月%d日').decode('utf-8')
	day_before_yesterday = day_before_yesterday.strftime('%m月%d日').decode('utf-8')
	name2date = {
		u'今天': today,
		u'明天': tomorrow,
		u'后天': day_after_tomorrow,
		u'昨天': yesterday,
		u'前天': day_before_yesterday
	}

	expected_coupons = json.loads(context.text)
	for expected_coupon in expected_coupons:
		if 'create_date' in expected_coupon:
			expected_coupon['create_date'] = name2date[expected_coupon['create_date']]
		if 'expire_date' in expected_coupon:
			expected_coupon['expire_date'] = name2date[expected_coupon['expire_date']]

	bdd_util.assert_list(expected_coupons, coupons)


@then(u"{user_name}能获得优惠券'{coupon_rule_name}'的码库")
def step_impl(context, user_name, coupon_rule_name):
	db_coupon_rule = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=coupon_rule_name)
	url = '/mall_promotion/api/coupons/get/?id=%d' % db_coupon_rule.id
	response = context.client.get(url)
	
	bdd_util.assert_api_call_success(response)
	
	actual = {}
	coupons = json.loads(response.content)['data']['items']
	for coupon in coupons:
		coupon['target'] = coupon['member']['username_for_html']
		coupon['consumer'] = coupon['consumer']['username_for_html']
		coupon['money'] = float(coupon['money'])
		actual[coupon['coupon_id']] = coupon

	expected_coupons = json.loads(context.text)
	bdd_util.assert_dict(expected_coupons, actual)


@when(u"{user_name}为会员发放优惠券")
def step_impl(context, user_name):
	__send_coupons(context, user_name, u'会员')
	
	
@when(u"{user}更新优惠券排行榜时间")
def step_impl(context, user):
	coupon_saller_data = json.loads(context.text)
	url = '/market_tools/coupon/api/coupon_saller_data/update/'
	response = context.client.post(url, coupon_saller_data[0])

 
@then(u"{user}能获得优惠券排行榜时间")
def step_impl(context, user):
	url = '/market_tools/coupon/'
	response = context.client.get(url)
	actual = response.context['coupon_saller_data']
	actual_data = []
	actual_data.append({
		"start_date": actual.start_date.strftime('%Y-%m-%d'),
		"end_date": actual.end_date.strftime('%Y-%m-%d')
	})

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual_data)


@when(u"{webapp_user_name}领取{webapp_owner_name}的优惠券")
def step_impl(context, webapp_user_name, webapp_owner_name):
	infos = json.loads(context.text)
	
	for info in infos:
		coupon_rule = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=info['name'])
		for coupon_id in info['coupon_ids']:
			# url = '/termite/workbench/jqm/preview/?module=market_tool:coupon&model=coupon&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%s&project_id=0&rule_id=%d&coupon_id=%s' % (context.webapp_owner_id, coupon_rule.id, coupon_id)
			url = '/webapp/api/project_api/call/?design_mode=0&project_id=market_tool:coupon:0'
			response = context.client.post(bdd_util.nginx(url), {'target_api': 'coupon/consume', 'rule_id': coupon_rule.id, 'webapp_owner_id':context.webapp_owner_id}, follow=True)
			# response = context.client.post(bdd_util.nginx(url), {'target_api': 'coupon/consume', }, follow=True)
			#bdd_util.assert_api_call_success(response)
			#coupon = response.context['coupons'][0]
			#Coupon.objects.filter(id=coupon.id).update(coupon_id=coupon_id)
	