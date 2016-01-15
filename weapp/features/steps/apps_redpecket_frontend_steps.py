#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'kuki'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.red_packet.models import RedPacket, RedPacketParticipance, RedPacketControl,RedPacketLog,RedPacketDetail
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member

def __get_red_packet_rule_name(title):
	material_url = material_models.News.objects.get(title=title).url
	red_packet_rule_name = material_url.split('-')[1]
	return red_packet_rule_name

def __get_red_packet_rule_id(red_packet_rule_name):
	return RedPacket.objects.get(name=red_packet_rule_name).id

def __get_channel_qrcode_name(red_packet_rule_id):
	return RedPacket.objects.get(id=red_packet_rule_id).qrcode['name']

def __get_into_red_packet_pages(context,webapp_owner_id,red_packet_rule_id,openid):
	#进入拼红包活动页面
	url = '/m/apps/red_packet/m_red_packet/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, red_packet_rule_id, context.member.token, openid)
	url = bdd_util.nginx(url)
	context.link_url = url
	response = context.client.get(url)
	if response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
		if response.status_code == 302:
			print('[info] redirect by change fmt in shared_url')
			redirect_url = bdd_util.nginx(response['Location'])
			context.last_url = redirect_url
			response = context.client.get(bdd_util.nginx(redirect_url))
		else:
			print('[info] not redirect')
	else:
		print('[info] not redirect')
	return response

def __get_red_packet_informations(context,webapp_owner_id,red_packet_rule_id,openid,fid):
	url = '/m/apps/red_packet/api/m_red_packet/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s&fid=%s' % (webapp_owner_id, red_packet_rule_id, context.member.token, openid,fid)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	while response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	if response.status_code == 200:
		return response
	else:
		print('[info] redirect error,response.status_code :')
		print(response.status_code)
		
@When(u'{webapp_user_name}点击图文"{title}"进入拼红包活动页面')
def step_impl(context, webapp_user_name, title):
	webapp_owner_id = context.webapp_owner_id
	if not context.__contains__('page_owner_member_id'):
		context.page_owner_member_id = Member.objects.get(username_hexstr=byte_to_hex(webapp_user_name)).id
	print(context.page_owner_member_id)
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	red_packet_rule_name = __get_red_packet_rule_name(title)
	red_packet_rule_id = __get_red_packet_rule_id(red_packet_rule_name)
	response = __get_into_red_packet_pages(context,webapp_owner_id,red_packet_rule_id,openid)
	context.red_packet_rule_id = red_packet_rule_id
	context.api_response = __get_red_packet_informations(context,webapp_owner_id,red_packet_rule_id,openid,context.page_owner_member_id).content
	context.page_owner_member_id = json.loads(context.api_response)['data']['member_info']['page_owner_member_id']
	print('context.api_response')
	print(context.api_response)

@then(u"{webapp_user_name}获得{webapp_owner_name}的拼红包活动'{red_packet_rule_name}'的内容")
def step_tmpl(context, webapp_user_name, webapp_owner_name, red_packet_rule_name):
	red_packet_rule_id = __get_red_packet_rule_id(red_packet_rule_name)
	api_response_information = json.loads(context.api_response)['data']
	red_packet_info = RedPacket.objects.get(id=red_packet_rule_id)
	related_page_id = red_packet_info.related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_component = page['component']['components'][0]['model']

	# 构造实际数据
	actual = []
	actual.append({
		"name": red_packet_info.name,
		"is_show_countdown": page_component['timing']['timing']['select'],
		"rules": page_component['rules'],
		"red_packet_money": api_response_information['member_info']['red_packet_money']
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@When(u'{webapp_user_name}把{red_packet_owner_name}的拼红包活动链接分享到朋友圈')
def step_impl(context, webapp_user_name, red_packet_owner_name):
	context.shared_url = context.link_url
	print('context.shared_url:',context.shared_url)

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的拼红包活动链接')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	followed_member = Member.objects.get(username_hexstr=byte_to_hex(shared_webapp_user_name))
	if member:
		new_url = url_helper.remove_querystr_filed_from_request_path(context.shared_url, 'fmt')
		new_url = url_helper.remove_querystr_filed_from_request_path(new_url, 'opid')
		context.shared_url = "%s&fmt=%s" % (new_url, followed_member.token)
	response = context.client.get(context.shared_url)
	if response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	else:
		print('[info] not redirect')
		context.last_url = context.shared_url
	context.api_response = __get_red_packet_informations(context,webapp_owner_id,context.red_packet_rule_id,openid,context.page_owner_member_id).content
	print('context.api_response')
	print(context.api_response)

@When(u'{webapp_user_name}为好友{red_packet_owner_name}点赞')
def step_impl(context, webapp_user_name, red_packet_owner_name):
	# 要先进入拼红包活动页面创建participance记录
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	red_packet_rule_id = context.red_packet_rule_id
	response = __get_into_red_packet_pages(context,webapp_owner_id,red_packet_rule_id,openid)
	context.api_response = __get_red_packet_informations(context,webapp_owner_id,red_packet_rule_id,openid,context.page_owner_member_id).content
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': red_packet_rule_id,
		'fid': context.page_owner_member_id
	}
	response = context.client.post('/m/apps/red_packet/api/red_packet_participance/?_method=put', params)
	if json.loads(response.content)['code'] == 500:
		context.err_msg = json.loads(response.content)['errMsg']

@when(u"{webapp_user_name}通过识别拼红包弹层中的公众号二维码关注{mp_user_name}的公众号")
def step_tmpl(context, webapp_user_name, mp_user_name):
	context.execute_steps(u"when %s关注%s的公众号" % (webapp_user_name, mp_user_name))
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	# 因没有可用的API处理Member相关的source字段, 暂时直接操作Member对象
	Member.objects.filter(id=member.id).update(source=SOURCE_MEMBER_QRCODE)

@when(u"{webapp_user_name}通过识别拼红包弹层中的带参数二维码关注{mp_user_name}的公众号")
def step_tmpl(context, webapp_user_name, mp_user_name):
	red_packet_rule_id = context.red_packet_rule_id
	channel_qrcode_name = __get_channel_qrcode_name(red_packet_rule_id)
	context.execute_steps(u'when %s扫描带参数二维码"%s"' % (webapp_user_name, channel_qrcode_name))

@then(u'{webapp_user_name}获得"{red_packet_rule_name}"的已贡献好友列表')
def step_tmpl(context, webapp_user_name, red_packet_rule_name):
	api_response_information = json.loads(context.api_response)['data']
	print('api_response_information')
	print(api_response_information)
	helpers_info = api_response_information['helpers_info']
	actual = []
	if helpers_info != []:
		for p in helpers_info:
			p_dict = OrderedDict()
			p_dict[u"name"] = p['username']
			actual.append((p_dict))
	print("actual_data: {}".format(actual))
	expected = []
	if context.table:
		for row in context.table:
			cur_p = row.as_dict()
			expected.append(cur_p)
	else:
		expected = json.loads(context.text)
	print("expected: {}".format(expected))

	bdd_util.assert_list(expected, actual)

# @when(u"微信用户批量参加{webapp_owner_name}的拼红包活动")
# def step_impl(context, webapp_owner_name):
# 	for row in context.table:
# 		webapp_user_name = row['member_name']
# 		if webapp_user_name[0] == u'-':
# 			webapp_user_name = webapp_user_name[1:]
# 			#clear last member's info in cookie and context
# 			context.execute_steps(u"When 清空浏览器")
# 		else:
# 			context.execute_steps(u"When 清空浏览器")
# 			context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))
# 		data = {
# 			'webapp_user_name': webapp_user_name,
# 			'red_packet_value': row['red_packet_value'],
# 			'parti_time': bdd_util.get_datetime_str(row['parti_time']),
# 			'name': row['name']
# 		}
# 		webapp_owner_id = context.webapp_owner_id
# 		user = User.objects.get(id=webapp_owner_id)
# 		openid = "%s_%s" % (webapp_user_name, user.username)
# 		red_packet_rule_id = str(__get_red_packet_rule_id(data['name']))
# 		member = member_api.get_member_by_openid(openid, context.webapp_id)
# 		#先进入拼红包页面
# 		response = __get_into_red_packet_pages(context,webapp_owner_id,red_packet_rule_id,openid)
# 		context.red_packet_rule_id = red_packet_rule_id
# 		context.api_response = __get_red_packet_informations(context,webapp_owner_id,red_packet_rule_id,openid).content
# 		context.execute_steps(u"when %s把%s的拼红包活动链接分享到朋友圈" % (webapp_user_name, webapp_owner_name))
# 		powered_member_info = RedPacketParticipance.objects.get(member_id=member.id, belong_to=red_packet_rule_id)
# 		powered_member_info.update(set__created_at=data['parti_time'])
# 		i = 0
# 		webapp_test_user_name = 'test_user_'
# 		while i < int(data['red_packet_value']):
# 			i += 1
# 			context.execute_steps(u"When 清空浏览器")
# 			context.execute_steps(u"When %s关注%s的公众号" % (webapp_test_user_name+str(i), webapp_owner_name))
# 			context.execute_steps(u"When %s访问%s的webapp" % (webapp_test_user_name+str(i), webapp_owner_name))
# 			context.execute_steps(u"When %s点击%s分享的拼红包活动链接进行助力" % (webapp_test_user_name+str(i), webapp_user_name))
# 	context.execute_steps(u"When 更新助力排名")

@then(u'{webapp_user_name}获得拼红包活动提示"{err_msg}"')
def step_tmpl(context, webapp_user_name, err_msg):
	expected = err_msg
	actual = context.err_msg
	context.tc.assertEquals(expected, actual)
