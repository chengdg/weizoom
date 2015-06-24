# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta


from behave import given, then, when
from test import bdd_util
# from features.testenv.model_factory import *

from mall.models import Product
from account.social_account.models import SocialAccount
from modules.member.models import Member, MemberHasSocialAccount
from mall.promotion.models import Promotion, Coupon, CouponRule


def __add_coupon_rule(context, webapp_owner_name):
	coupon_rules = json.loads(context.text)
	if type(coupon_rules) == dict:
		coupon_rules = [coupon_rules]

	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
	for coupon_rule in coupon_rules:
		# __add_coupon_rule(context, coupon_rule, user_name)
		cr_name = coupon_rule['name']
		cr_money = coupon_rule['money']
		cr_count = coupon_rule.get('count', 4)
		cr_limit_counts = coupon_rule.get('limit_counts', 9999)
		cr_start_date = coupon_rule['start_date']
		start_date = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))
		cr_end_date = coupon_rule['end_date']
		end_date = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))
		post_data = {
			'name': cr_name,
			'money': cr_money,
			'count': cr_count,
			'limit_counts': cr_limit_counts,
			'start_date': start_date,
			'end_date': end_date
		}
		if not "using_limit" in coupon_rule:
			post_data['is_valid_restrictions'] = '0'
		else:
			post_data['is_valid_restrictions'] = '1'
			using_limit = coupon_rule['using_limit']
			end = using_limit.find(u"元")
			if end == -1:
				post_data['valid_restrictions'] = -1
			else:
				post_data['valid_restrictions'] = int(using_limit[1:end])
		if "coupon_product" in coupon_rule:
			post_data['limit_product'] = 1
			post_data['product_ids'] = Product.objects.get(
											owner_id=webapp_owner_id,
											name=coupon_rule['coupon_product']).id
		url = '/mall_promotion/api/coupon_rules/create/'
		response = context.client.post(url, post_data)
		context.tc.assertEquals(200, response.status_code)
		if "coupon_id_prefix" in coupon_rule:
			latest_coupon_rule = CouponRule.objects.all().order_by('-id')[0]
			index = 1
			coupon_id_prefix = coupon_rule['coupon_id_prefix']
			for coupon in Coupon.objects.filter(coupon_rule=latest_coupon_rule):
				coupon_id = "%s%d" % (coupon_id_prefix, index)
				Coupon.objects.filter(id=coupon.id).update(coupon_id=coupon_id)
				index +=1
		time.sleep(0.002)



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

	new_created_coupons = Coupon.objects.filter(owner_id=webapp_owner_id).order_by('-id')[:count]
	expected_coupon_ids = coupon_info['coupon_ids']
	expected_coupon_ids.reverse()
	for index, coupon in enumerate(new_created_coupons):
		# 将coupon_id改为指定的coupon_id，特殊情况允许更新操作
		Coupon.objects.filter(coupon_id=coupon.coupon_id).update(coupon_id=expected_coupon_ids[index])

	if 'expire_date' in coupon_info:
		# 修改发放时间和过期时间，特殊情况允许更新操作
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
	__add_coupon_rule(context, user_name)


@given(u'{user_name}已添加了优惠券规则')
def step_impl(context, user_name):
	__add_coupon_rule(context, user_name)


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
	response = context.client.get('/mall_promotion/api/promotions/get/?design_mode=0&version=1&type=coupon&count_per_page=10&page=1')
	coupon_rules = json.loads(response.content)['data']['items']

	actual = []
	for coupon_rule in coupon_rules:
		rule = {}
		rule["name"] = coupon_rule["name"]
		rule["type"] = "单品券" if coupon_rule["detail"]["limit_product"] else "全店通用券"
		rule["money"] = coupon_rule["detail"]["money"]
		rule["remained_count"] = coupon_rule["detail"]["remained_count"]
		rule["limit_counts"] = coupon_rule["detail"]["limit_counts"]
		rule["use_count"] = coupon_rule["detail"]["use_count"]
		rule["start_date"] = coupon_rule["start_date"]
		rule["end_date"] = coupon_rule["end_date"]
		actual.append(rule)

	expected = json.loads(context.text)
	for item in expected:
		item["start_date"] = "{} 00:00".format(bdd_util.get_date_str(item["start_date"]))
		item["end_date"] = "{} 00:00".format(bdd_util.get_date_str(item["end_date"]))
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


@when(u"{user_name}删除优惠券'{coupon_rule_name}'")
def step_impl(context, user_name, coupon_rule_name):
	user_id = bdd_util.get_user_id_for(user_name)
	coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
	promotion = Promotion.objects.get(detail_id=coupon_rule.id)
	url = '/mall_promotion/api/promotions/delete/'

	response = context.client.post(url, {'ids[]': [promotion.id], 'type': 'coupon'})


@when(u"{user_name}删除优惠券'{coupon_rule_name}'的码库")
def step_coupon_delete(context, user_name, coupon_rule_name):
	from django.db.models import Q
	coupon_rule = CouponRule.objects.get(name=coupon_rule_name)
	# Coupon.objects.filter(Q(coupon_rule_id=coupon_rule.id) and
	#                       ~Q(status=0)
	#                       ).delete()


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


@then(u"{user_name}获得优惠券规则列表")
def step_impl(context, user_name):
	"""

	e.g.:
		[{
			"coupon_rule": "过期优惠券规则",
			"money": "1.00",
			"create_date": "前天",
			"expire_date": "昨天",
			"status": "已结束"
		},{
			"coupon_rule": "优惠券规则3",
			"money": "10.00",
			"create_date": "前天",
			"expire_date": "后天",
			"status": "进行中"
		}]

	"""
	url = '/mall_promotion/api/promotions/get/'
	the_kwargs = {
		"type": "coupon",
	}
	response = context.client.get(url, the_kwargs)
	coupons = json.loads(response.content)['data']['items']

	for coupon in coupons:
		coupon['coupon_rule'] = coupon['detail']['name']
		coupon['create_date'] = coupon['start_date']
		coupon['expire_date'] = coupon['end_date']

		# if coupon['is_manual_generated']:
		# 	coupon['target'] = u'手工'
		# else:
		# 	coupon['target'] = coupon['member']['username_for_html']

		# coupon['consumer'] = coupon['consumer']['username_for_html']
		coupon['money'] = coupon['detail']["money"]

	#处理expected中的参数
	today = datetime.today()
	today = today.replace(hour=0, minute=0, second=0, microsecond=0)

	tomorrow = today + timedelta(1)
	day_after_tomorrow = tomorrow + timedelta(1)
	yesterday = today - timedelta(1)
	day_before_yesterday = yesterday - timedelta(1)
	t_format = "%Y-%m-%d %H:%M"
	today = today.strftime(t_format).decode('utf-8')
	tomorrow = tomorrow.strftime(t_format).decode('utf-8')
	day_after_tomorrow = day_after_tomorrow.strftime(t_format).decode('utf-8')
	yesterday = yesterday.strftime(t_format).decode('utf-8')
	day_before_yesterday = day_before_yesterday.strftime(t_format).decode('utf-8')
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


# @when(u"{user}更新优惠券排行榜时间")
# def step_impl(context, user):
# 	coupon_saller_data = json.loads(context.text)
# 	url = '/market_tools/coupon/api/coupon_saller_data/update/'
# 	response = context.client.post(url, coupon_saller_data[0])


# @then(u"{user}能获得优惠券排行榜时间")
# def step_impl(context, user):
# 	url = '/market_tools/coupon/'
# 	response = context.client.get(url)
# 	actual = response.context['coupon_saller_data']
# 	actual_data = []
# 	actual_data.append({
# 		"start_date": actual.start_date.strftime('%Y-%m-%d'),
# 		"end_date": actual.end_date.strftime('%Y-%m-%d')
# 	})

# 	expected = json.loads(context.text)

# 	bdd_util.assert_list(expected, actual_data)


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


@when(u"{webapp_owner}失效优惠券'{coupon_rule_name}'")
def step_disable_coupon_rule(context, webapp_owner, coupon_rule_name):
	promotion = Promotion.objects.get(name=coupon_rule_name)
	args = {
		'ids[]': [promotion.id,],
		'type': 'coupon'
	}
	url = '/mall_promotion/api/promotions/finish/'
	context.client.post(url, args)
