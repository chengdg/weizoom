# -*- coding: utf-8 -*-

import time
import json
import random
from behave import *
from mall.promotion.models import CouponRule
from modules.member.models import MemberGrade, MemberTag, Member
from test import bdd_util
import logging
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings
from utils.string_util import byte_to_hex


def __create_random_ticket():
    ticket = time.strftime("%Y%m%d%H%M%S", time.localtime())
    ticket = '%s%03d' % (ticket, random.randint(1, 999))
    if ChannelDistributionQrcodeSettings.objects.filter(ticket=ticket).count() > 0:
        return __create_random_ticket()
    else:
        return ticket

@When(u"{user}新建渠道分销二维码")
def step_impl(context, user):
	expecteds = json.loads(context.text)
	for expected in expecteds:
		
		params = {} 
		distribution_rewards_type = {u'无':0, u'佣金':1}

		name = expected['relation_member']
		name = byte_to_hex(name)
		bing_member_id = Member.objects.filter(username_hexstr__contains=name)[0].id

		group_id = MemberTag.objects.get(webapp_id=context.webapp_id, name=expected['tags']).id

		if expected['prize_type'] == u"无":
			prize_info = '{"id":-1,"name":"non-prize","type":"无奖励"}'
		elif expected['prize_type'] == u'优惠券':
			coupon_rule_id = CouponRule.objects.filter(name=expected['coupon']).order_by('-id')[0].id
			prize_info = '{"id":%s,"name":"%s","type":"优惠券"}'%(coupon_rule_id, expected['coupon'])
		elif expected['prize_type'] == u'积分':
			prize_info = '{"id":%s,"name":"_score-prize_","type":"积分"}'%expected['integral']

		reply_type_type = {u'文字':1 ,u'图文': 2}

		# 图文
		reply_detail = ''
		reply_material_id = 0
		if reply_type_type[expected['reply_type']] == 1:
			reply_detail = expected['scan_code_reply']
		elif reply_type_type[expected['reply_type']] == 2:
			reply_material_id = 1

		# 格式化数据
		params['bing_member_title'] = expected['code_name']
		params['bing_member_id'] = bing_member_id
		params['distribution_rewards'] = distribution_rewards_type[expected['distribution_prize_type']]
		params['commission_rate'] = expected['commission_return_rate']
		params['minimun_return_rate'] = expected['minimum_cash_discount']
		params['commission_return_standard'] = expected['commission_return_standard']
		params['return_standard'] = expected['settlement_time']
		params['group_id'] = group_id
		params['prize_info'] = prize_info
		params['reply_type'] = reply_type_type[expected['reply_type']]
		params['reply_material_id'] = reply_material_id
		params['reply_detail'] = reply_detail
		params['create_time'] = expected['create_time']
		params['_method'] = 'put'

		response = context.client.post('/new_weixin/api/channel_distribution/', params)

		# 给二维码ticket添加个随机值
		qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_title=params['bing_member_title'])
		qrcode.ticket = __create_random_ticket()
		qrcode.save()
		# logging.info(response)
		# logging.info('////////////////////')

@Then(u"{user}获得渠道分销二维码列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	params = {}
	if hasattr(context, 'distribution_query_name'):
		params['query_name'] = context.distribution_query_name
	if hasattr(context, 'count_per_page'):
		params['count_per_page'] = context.count_per_page
	if hasattr(context, 'distribution_page'):
		params['page'] = context.distribution_page

	response = context.client.get('/new_weixin/api/channel_distributions/', params)

	datas = json.loads(response.content)['data']['items']
	actual_list = []
	for data in datas:
		data_dict = {}
		data_dict['code_name'] = data['title']
		data_dict['relation_member'] = data['bing_member_name']
		data_dict['attention_number'] = data['bing_member_count']
		data_dict['total_transaction_money'] =float(data['total_transaction_volume'])
		data_dict['cash_back_amount'] = float(data['total_return'])
		data_dict['prize'] = data['award_prize_info']
		data_dict['distribution_prize'] = data['distribution_rewards']
		data_dict['create_time'] = data['created_at']
		actual_list.append(data_dict)

	bdd_util.assert_list(expected, actual_list)


@When(u"{user}设置渠道分销二维码查询条件")
def step_impl(context, user):
	code_name = json.loads(context.text)['code_name']
	context.distribution_query_name = code_name


@When(u"{user}设置分页查询参数")
def set_paginate_args(context, user):
	count_per_page = json.loads(context.text)['count_per_page']
	context.count_per_page = count_per_page


@When(u"{user}访问渠道分销二维码列表第'{num}'页")
def step_impl(context, user, num):
	context.distribution_page = int(num)


@When(u"{user}访问渠道分销二维码列表下一页")
def step_impl(context, user):
	if hasattr(context, 'distribution_page'):
		context.distribution_page += 1
	else:
		context.distribution_page = 2


@When(u"{user}访问渠道分销二维码列表上一页")
def step_impl(context, user):
	if hasattr(context, 'distribution_page'):
		context.distribution_page -= 1


@When(u"{user}更新渠道分销二维码'{qrcode_name}'")
def step_impl(context, user, qrcode_name):
	expected = json.loads(context.text)
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_title=qrcode_name)

	distribution_rewards_type = {u'无': 0, u'佣金': 1}

	name = expected['relation_member']
	name = byte_to_hex(name)
	bing_member_id = Member.objects.filter(username_hexstr__contains=name)[0].id
	group_id = MemberTag.objects.get(webapp_id=context.webapp_id, name=expected['tags']).id
	if expected['prize_type'] == u"无":
		prize_info = '{"id":-1,"name":"non-prize","type":"无奖励"}'
	elif expected['prize_type'] == u'优惠券':
		coupon_rule_id = CouponRule.objects.filter(name=expected['coupon']).order_by('-id')[0].id
		prize_info = '{"id":%s,"name":"%s","type":"优惠券"}' % (coupon_rule_id, expected['coupon'])
	elif expected['prize_type'] == u'积分':
		prize_info = '{"id":%s,"name":"_score-prize_","type":"积分"}' % expected['integral']

	reply_type_type = {u'文字': 1, u'图文': 2}
	# 图文
	reply_detail = ''
	reply_material_id = 0
	if reply_type_type[expected['reply_type']] == 1:
		reply_detail = expected['scan_code_reply']
	elif reply_type_type[expected['reply_type']] == 2:
		reply_material_id = 1

	params = {}
	params['qrcode_id'] = qrcode.id
	params['bing_member_title'] = expected['code_name']
	params['bing_member_id'] = bing_member_id
	params['distribution_rewards'] = distribution_rewards_type[expected['distribution_prize_type']]
	params['commission_rate'] = expected['commission_return_rate']
	params['minimun_return_rate'] = expected['minimum_cash_discount']
	params['commission_return_standard'] = expected['commission_return_standard']
	params['return_standard'] = expected['setlement_time']
	params['group_id'] = group_id
	params['prize_info'] = prize_info
	params['reply_type'] = reply_type_type[expected['reply_type']]
	params['reply_material_id'] = reply_material_id
	params['reply_detail'] = reply_detail
	params['create_time'] = expected['create_time']


	response = context.client.post('/new_weixin/api/channel_distribution/', params)
	# logging.info('11111111111')
	# logging.info(response)



# @When(u"{qrcode_name}访问'{user}'的webapp")
# def step_impl(context, user, qrcode_name):
# 	if not expected['order'] and not expected['extraction_money']
	
# Scenario:1 没有订单,没有佣金
@Then(u"{user}获得推广分销详情")
def step_impl(context,user):
	expected = json.loads(context.text)
	name = byte_to_hex(user)
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_title=name)

	params = {}
	params['already_extracted'] = qrcode.total_return
	params['income'] = qrcode.will_return_reward
	params['commission_return_standard'] = qrcode.commission_return_standard
	params['already_reward'] = qrcode.total_return
	params['difference_value'] = qrcode.will_return_reward

	actual_list = []
	for param in params:
		param_dict = {}
		param_dict['already_extracted'] = params['already_extracted']
		param_dict['income'] = params['income']
		param_dict['commission_return_standard'] =float(param['commission_return_standard'])
		param_dict['already_reward'] = param['already_reward']
		param_dict['difference_value'] = float(param['difference_value'])
		actual_list.append(param_dict)

	bdd_util.assert_list(expected, actual_list)


# @Then(u"{user}获得分销会员结算列表")
# def step_impl(context,user):
# 	expected = json.loads(context.text)

# 	name = expected['relation_member']
# 	name = byte_to_hex(name)
	
	




	

