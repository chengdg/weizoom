# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *
from mall.promotion.models import CouponRule
from utils.string_util import byte_to_hex

@when(u"{user}选择会员")
def step_impl(context, user):
    context.member_ids = []
    for raw in context.table:
        query_hex = byte_to_hex(raw['member_name'])
        member = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex)
        context.member_ids.append(str(member.id))

@when(u"{user}批量修改等级")
def step_impl(context, user):
    member_ids = context.member_ids
    data = json.loads(context.text)[0]
    grade_name = data['member_rank']
    grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=grade_name).id
    args = {}
    if data['modification_method'] == '给选中的人修改等级':
        if not member_ids:
            return
        args['update_status'] = 'selected'
        args['ids'] = '-'.join(member_ids)
    elif data['modification_method'] == '给筛选出来的所有人修改等级':
        args['update_status'] = 'all'
        if hasattr(context, 'filter_str'):
            args['filter_value'] = context.filter_str


    args['grade_id'] = grade_id
    response = context.client.post('/member/api/grade/batch_update/', args)
    bdd_util.assert_api_call_success(response)

@when(u"{user}批量添加分组")
def step_impl(context, user):
    member_ids = context.member_ids
    data = json.loads(context.text)[0]
    tag_name = data['grouping']
    tag_id = MemberTag.objects.get(webapp_id=context.webapp_id, name=tag_name).id
    args = {}
    if data['modification_method'] == '给选中的人添加分组':
        if not member_ids:
            return
        args['update_status'] = 'selected'
        args['ids'] = '-'.join(member_ids)
    elif data['modification_method'] == '给筛选出来的所有人添加分组':
        args['update_status'] = 'all'
        if hasattr(context, 'filter_str'):
            args['filter_value'] = context.filter_str


    args['tag_id'] = tag_id
    response = context.client.post('/member/api/tag/batch_update/', args)
    bdd_util.assert_api_call_success(response)

@when(u'{webapp_user}给"{member}"调分组')
def step_impl(context, webapp_user, member):
    url = '/member/api/tag/update/'
    query_hex = byte_to_hex(member)
    member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
    tag_ids = []
    data = json.loads(context.text)
    for tag_name in data:
        tag_ids.append(str(MemberTag.objects.get(webapp_id=context.webapp_id, name=tag_name).id))
    args = {
        'type': 'tag',
        'checked_ids': '_'.join(tag_ids),
        'member_id': member_id
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

@when(u'{webapp_user}给"{member}"设等级')
def step_impl(context, webapp_user, member):
    url = '/member/api/tag/update/'
    query_hex = byte_to_hex(member)
    member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
    data = json.loads(context.text)
    grade_name = data['member_rank']
    grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=grade_name).id

    args = {
        'type': 'grade',
        'checked_ids': grade_id,
        'member_id': member_id
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)


@when(u'{webapp_user}给"{member}"发优惠券')
def step_impl(context, webapp_user, member):
    query_hex = byte_to_hex(member)
    member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
    data = json.loads(context.text)[0]
    coupon_rule_name = data['name']
    count = data['count']
    coupon_rule_id = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=coupon_rule_name).id

    args = {
        'coupon_rule_id': coupon_rule_id,
        'pre_person_count': count,
        'member_id': json.dumps([member_id])
    }

    url = '/mall2/api/issuing_coupons_record/?_method=put'
    response = context.client.post(url, args)
    try:
        bdd_util.assert_api_call_success(response)
    except:
        #用来判断出错的提示信息
        context.response = response

@when(u'{webapp_user}给"{member}"加积分')
def step_impl(context, webapp_user, member):
    url = '/member/api/integral/update/'
    query_hex = byte_to_hex(member)
    member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
    data = json.loads(context.text)

    args = {
        'integral': data['integral'],
        'reason': data['reason'],
        'member_id': member_id
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

@when(u"{user}批量发优惠券")
def step_impl(context, user):
    data = json.loads(context.text)[0]
    coupon_rule_name = data.get('coupon_name', '')
    count = data.get('count', 0)
    if not coupon_rule_name:
        return
    coupon_rule_id = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=coupon_rule_name).id
    args = {}
    args['coupon_rule_id'] = coupon_rule_id
    args['pre_person_count'] = count

    url = "/mall2/api/issuing_coupons_record/?_method=put"
    if data['modification_method'] == '给选中的人发优惠券(已取消关注的除外)':
        args['member_id'] = json.dumps(context.member_ids)
    elif data['modification_method'] == '给筛选出来的所有人发优惠券(已取消关注的除外)':
        get_all_member_args = {}
        get_all_member_args['filter_value'] = context.filter_str
        get_all_member_args['count_per_page'] = 999999999999
        response = context.client.get('/member/api/members/get/', get_all_member_args)
        member_ids = []
        for item in json.dumps(response)['items']:
            member_ids.append(item["id"])

        args['member_id'] = member_ids

    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

# @Then(u"{user}能获取会员等级列表")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)
# 	response = context.client.get('/webapp/user_center/grades/')
# 	member_grades = response.context['member_grades']
# 	#context.tc.assertEquals(len(member_grades), len(json_data))
# 	response_data = []
# 	for grade in member_grades:
# 		data_dict = {}
# 		data_dict['name'] = grade.name
# 		data_dict['shop_discount'] =  str(grade.shop_discount)+"%"
# 		if grade.is_auto_upgrade:
# 			data_dict['upgrade'] = u"自动升级"
# 		else:
# 			data_dict['upgrade'] = u"不自动升级"
# 		response_data.append(data_dict)

# 	bdd_util.assert_list(response_data, json_data)

# def _add_member_grade(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)
# 	for content in json_data:
# 		if content['upgrade'] == u'不自动升级':
# 			content['is_auto_upgrade'] = 0
# 		else:
# 			content['is_auto_upgrade'] = 1
# 			content['upgrade_lower_bound'] = int(content['shop_discount'].replace('%',''))
# 		content['shop_discount'] = content['shop_discount'].replace('%','')
# 		if MemberGrade.objects.filter(name=content['name'], webapp_id=user.get_profile().webapp_id).count() == 0:
# 			response = context.client.post('/webapp/user_center/grade/create/', content)

# @When(u"{user}添加会员等级")
# def step_impl(context, user):
# 	_add_member_grade(context, user)

# @Given(u"{user}添加会员等级")
# def step_impl(context, user):
# 	_add_member_grade(context, user)

# @When(u"{user}更新会员等级{name}")
# def step_impl(context, user, name):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)
# 	if name.startswith("'") and name.endswith("'"):
# 		name = name.replace("'","")
# 	grade = MemberGrade.objects.get(webapp_id=user.get_profile().webapp_id, name=name)
# 	context.tc.assertEquals(name, grade.name)
# 	for content in json_data:
# 		if content['upgrade'] == u'不自动升级':
# 			content['is_auto_upgrade'] = 0
# 		else:
# 			content['is_auto_upgrade'] = 1
# 			content['upgrade_lower_bound'] = int(content['shop_discount'].replace('%',''))
# 		if content.has_key('integral'):
# 			integral = content['integral']
# 			if integral.find('%') > 0:
# 				integral = integral.replace('%','')
# 			content['usable_integral_percentage_in_order'] = integral
# 		content['shop_discount'] = content['shop_discount'].replace('%','')
# 		response = context.client.post('/webapp/user_center/grade/update/%d/' % grade.id, content)


# @When(u"{user}删除会员等级{name}")
# def step_impl(context, user, name):
# 	if hasattr(context, 'client'):
# 		context.client.logout()
# 	context.client = bdd_util.login(user)
# 	client = context.client
# 	user = UserFactory(username=user)
# 	json_data = json.loads(context.text)

# 	grade = MemberGrade.objects.get(webapp_id=user.get_profile().webapp_id, name=name)
# 	context.tc.assertEquals(name, grade.name)

# 	response = context.client.get('/webapp/user_center/grade/delete/%d/' % grade.id)