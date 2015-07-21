# -*- coding: utf-8 -*-
"""
营销工具(微信抽奖、渠道扫码)的steps

"""

__author__ = 'victor'
import json
import time
from test import bdd_util
from market_tools.tools.activity.models import *
from behave import *

from modules.member.models import MemberMarketUrl

from market_tools.tools.channel_qrcode.models import  ChannelQrcodeHasMember,ChannelQrcodeSettings
from market_tools.tools.lottery.models import LotteryRecord

from features.testenv.model_factory import UserFactory
from market_tools.tools.channel_qrcode.channel_qrcode_util import create_channel_qrcode_has_memeber
#from modules.member.models import Member

#from market_tools.prize import module_api
#from market_tools.prize.module_api import PrizeInfo


@given(u"{user}已添加'渠道扫码'营销活动")
def step_impl(context, user):
	"""
	添加若干渠道扫码的配置

	输入为配置的list(参考full_init.feature文件)
	"""
	client = context.client
	settings = json.loads(context.text)
	for setting in settings:
		context.response = client.post('/market_tools/channel_qrcode/edit_setting/', setting)
		time.sleep(1)
		channel_setting = bdd_util.get_channel_qrcode_setting(setting['name'])
		assert channel_setting is not None 
		owner_id = channel_setting.owner_id
		ChannelQrcodeSettings.objects.filter(owner_id=owner_id,name=setting['name']).update(ticket=setting['ticket'])


@then(u'{user}能看到的渠道扫码列表')
def step_impl(context, user):
	"""
	列出渠道扫码配置列表（按照添加顺序排列）
	"""
	client = context.client
	expected = json.loads(context.text)
	context.response = client.get('/market_tools/channel_qrcode/api/channel_qrcode_settings/get/?version=1&sort_attr=id&count_per_page=15&page=1&enable_paginate=1')
	#print("content: {}".format(context.response.content))
	results = json.loads(context.response.content)
	if results.has_key('data'):
		results = results['data']
	# 构造real_list，与expected_list比对
	items = results['items']
	real_list = []
	for item in items:
		real_list.append({
				'name': item['name'],
				'remark': item['remark']
			})
		#print('real: {} {}'.format(item['name'], item['remark']))
	"""        
	for item in expected:
		print('expected: {} {}'.format(item['name'], item['remark']))
	"""
	bdd_util.assert_list(expected, real_list)


@when(u"{webapp_user_name}通过扫描'{channel_qrcode_name}'二维码关注")
def step_impl(context, webapp_user_name, channel_qrcode_name):
	#webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	channel_setting = bdd_util.get_channel_qrcode_setting(channel_qrcode_name)
	assert channel_setting is not None 
	owner_id = channel_setting.owner_id
	is_new = False
	if webapp_user_name[0] == '-':
		# 表示此用户还不是会员，让其关注
		owner = User.objects.get(id=owner_id)
		webapp_user_name = webapp_user_name[1:]
		context.execute_steps(u"When %s关注%s的公众号" % (webapp_user_name, owner.username))
		is_new = True

	webapp_id = bdd_util.get_webapp_id_via_owner_id(owner_id)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	#user = UserFactory(username=webapp_user_name)
	#user = User.objects.get(id=owner_id)
	context.user_profile = UserProfile.objects.get(user_id=owner_id)
	ticket = channel_setting.ticket

	create_channel_qrcode_has_memeber(
		context.user_profile,
		member,
		ticket,
		is_new,
		)

	#if channel_setting.re_old_member!=0:
	#	ChannelQrcodeHasMember.objects.create( \
	#		channel_qrcode=channel_setting, \
	#		member=member \
	#		)

	#prize_info = PrizeInfo.from_json(channel_setting.award_prize_info)
	#module_api.award(prize_info, member, u'渠道扫码奖励')

	#Member.objects.filter(id=member.id).update(integral=int(integral_count))  
	


@given(u"{user}已添加'微信抽奖'活动配置")
def step_impl(context, user):
	"""
	添加若干抽奖活动的配置

	输入为配置的list(参考full_init.feature文件)
	"""
	client = context.client
	settings = json.loads(context.text)
	for setting in settings:
		context.response = client.post('/market_tools/lottery/api/lottery/edit/', setting)
		#print("response: {}".format(context.response.content))
		response_json = json.loads(context.response.content)
		assert response_json['code'] == 200


@when(u"{webapp_user_name}参加抽奖活动'{lottery_name}'")
def step_impl(context, webapp_user_name, lottery_name):
	#webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	lottery = bdd_util.get_lottery_setting(lottery_name)
	assert lottery is not None
	owner_id = lottery.owner_id
	webapp_id = bdd_util.get_webapp_id_via_owner_id(owner_id)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	#print("member: {}".format(member))
	LotteryRecord.objects.create(
		owner=lottery.owner,
		member=member,
		lottery=lottery,
		lottery_name=lottery.name,
		prize_type=0,
		prize_level=0,
		prize_name=u'谢谢参与',
		is_awarded=True,
		prize_number=time.time(),
		prize_detail='',
		prize_money=0
	)



