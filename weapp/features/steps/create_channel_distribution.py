# -*- coding: utf-8 -*-

import json
from behave import *
from mall.promotion.models import CouponRule
from modules.member.models import MemberGrade, MemberTag, Member
from test import bdd_util
import logging


from utils.string_util import byte_to_hex

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
		# if response['code'] != 200:
		# 	assert Exception('...')

@Then(u"{user}获得渠道分销二维码列表")
def step_impl(context, user):
	expected = json.loads(context.text)

	params = {}
	response = context.client.get('/new_weixin/api/channel_distributions/', params)
	# logging.info(dir(response))
	# logging.info(response.context)
	# logging.info(response.content)

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


