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
from apps.customerized_apps.group.models import Group, GroupRelations, GroupDetail
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member

def __get_group_rule_name(title):
	material_url = material_models.News.objects.get(title=title).url
	group_rule_name = material_url.split('-')[1]
	return group_rule_name

def __get_group_rule_id(group_rule_name):
	return Group.objects.get(name=group_rule_name).id

def __get_into_group_pages(context,webapp_owner_id,group_rule_id,openid):
	#进入微助力活动页面
	url = '/m/apps/powerme/m_powerme/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, group_rule_id, context.member.token, openid)
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

def __get_group_rank_informations(context,webapp_owner_id,group_rule_id,openid):
	url = '/m/apps/powerme/api/m_powerme/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, group_rule_id, context.member.token, openid)
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

@When(u'{webapp_user_name}点击图文"{title}"进入团购活动页面')
def step_impl(context, webapp_user_name, title):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	group_rule_name = __get_group_rule_name(title)
	group_rule_id = __get_group_rule_id(group_rule_name)
	response = __get_into_group_pages(context,webapp_owner_id,group_rule_id,openid)
	context.group_rule_id = group_rule_id
	context.rank_response = __get_group_rank_informations(context,webapp_owner_id,group_rule_id,openid).content

# @then(u"{webapp_user_name}获得{webapp_owner_name}的'{group_rule_name}'的内容")
# def step_tmpl(context, webapp_user_name, webapp_owner_name, group_rule_name):
# 	group_rule_id = __get_group_rule_id(group_rule_name)
# 	rank_information = json.loads(context.rank_response)['data']
# 	group_info = PowerMe.objects.get(id=group_rule_id)
# 	related_page_id = group_info.related_page_id
# 	pagestore = pagestore_manager.get_pagestore('mongo')
# 	page = pagestore.get_page(related_page_id, 1)
# 	page_component = page['component']['components'][0]['model']
#
# 	color2name = {
# 		'yellow': u'冬日暖阳',
# 		'red': u'玫瑰茜红',
# 		'orange': u'热带橙色'
# 	}
# 	# 构造实际数据
# 	actual = []
# 	actual.append({
# 		"name": group_info.name,
# 		"is_show_countdown": page_component['timing']['timing']['select'],
# 		"desc": page_component['description'],
# 		"background_pic": page_component['background_image'],
# 		"background_color": color2name[page_component['color']],
# 		"rules": page_component['rules'],
# 		"my_rank": rank_information['current_member_rank_info']['rank'] if rank_information['current_member_rank_info'] else u'无',
# 		"my_power_score": rank_information['current_member_rank_info']['power'] if rank_information['current_member_rank_info'] else '0',
# 		"total_participant_count": rank_information['total_participant_count']
# 	})
# 	print("actual_data: {}".format(actual))
# 	expected = json.loads(context.text)
# 	print("expected: {}".format(expected))
# 	bdd_util.assert_list(expected, actual)
#
# @then(u'{webapp_user_name}获得"{group_rule_name}"的助力值排名')
# def step_tmpl(context, webapp_user_name, group_rule_name):
# 	rank_information = json.loads(context.rank_response)['data']
# 	participances = rank_information['participances']
# 	actual = []
# 	if participances != []:
# 		rank = 0
# 		for p in participances:
# 			rank += 1
# 			p_dict = OrderedDict()
# 			p_dict[u"rank"] = rank
# 			p_dict[u"name"] = p['username']
# 			p_dict[u"value"] = p['power']
# 			actual.append((p_dict))
# 	print("actual_data: {}".format(actual))
# 	expected = []
# 	if context.table:
# 		for row in context.table:
# 			cur_p = row.as_dict()
# 			expected.append(cur_p)
# 	else:
# 		expected = json.loads(context.text)
# 	print("expected: {}".format(expected))
#
# 	bdd_util.assert_list(expected, actual)
#
# @When(u'{webapp_user_name}把{powerme_owner_name}的微助力活动链接分享到朋友圈')
# def step_impl(context, webapp_user_name, powerme_owner_name):
# 	context.shared_url = context.link_url
# 	print('context.shared_url:',context.shared_url)
# 	webapp_owner_id = context.webapp_owner_id
# 	webapp_owner_name = User.objects.get(id=webapp_owner_id).username
# 	if powerme_owner_name == webapp_owner_name: #如果是分享自己的助力活动
# 		context.page_owner_member_id = json.loads(context.rank_response)['data']['member_info']['page_owner_member_id']
# 	params = {
# 		'webapp_owner_id': context.webapp_owner_id,
# 		'id': context.group_rule_id,
# 		'fid': context.page_owner_member_id
# 	}
# 	response = context.client.post('/m/apps/powerme/api/powerme_participance/?_method=post', params)
#
# @When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的微助力活动链接进行参与')
# def step_impl(context, webapp_user_name, shared_webapp_user_name):
# 	webapp_owner_id = context.webapp_owner_id
# 	user = User.objects.get(id=webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
# 	member = member_api.get_member_by_openid(openid, context.webapp_id)
# 	followed_member = Member.objects.get(username_hexstr=byte_to_hex(shared_webapp_user_name))
# 	if member:
# 		new_url = url_helper.remove_querystr_filed_from_request_path(context.shared_url, 'fmt')
# 		new_url = url_helper.remove_querystr_filed_from_request_path(new_url, 'opid')
# 		context.shared_url = "%s&fmt=%s" % (new_url, followed_member.token)
# 	response = context.client.get(context.shared_url)
# 	if response.status_code == 302:
# 		print('[info] redirect by change fmt in shared_url')
# 		redirect_url = bdd_util.nginx(response['Location'])
# 		context.last_url = redirect_url
# 		response = context.client.get(bdd_util.nginx(redirect_url))
# 	else:
# 		print('[info] not redirect')
# 		context.last_url = context.shared_url
#
# @When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的微助力活动链接进行助力')
# def step_impl(context, webapp_user_name, shared_webapp_user_name):
# 	# 要先进入微助力活动页面创建participance记录
# 	webapp_owner_id = context.webapp_owner_id
# 	user = User.objects.get(id=webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
# 	group_rule_id = context.group_rule_id
# 	response = __get_into_group_pages(context,webapp_owner_id,group_rule_id,openid)
# 	context.rank_response = __get_group_rank_informations(context,webapp_owner_id,group_rule_id,openid).content
# 	params = {
# 		'webapp_owner_id': webapp_owner_id,
# 		'id': group_rule_id,
# 		'fid': context.page_owner_member_id
# 	}
# 	response = context.client.post('/m/apps/powerme/api/powerme_participance/?_method=put', params)
# 	if json.loads(response.content)['code'] == 500:
# 		context.err_msg = json.loads(response.content)['errMsg']
#
#
# @when(u"{webapp_user_name}通过识别弹层中的公众号二维码关注{mp_user_name}的公众号")
# def step_tmpl(context, webapp_user_name, mp_user_name):
# 	context.execute_steps(u"when %s关注%s的公众号" % (webapp_user_name, mp_user_name))
# 	webapp_owner_id = context.webapp_owner_id
# 	user = User.objects.get(id=webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
# 	member = member_api.get_member_by_openid(openid, context.webapp_id)
# 	# 因没有可用的API处理Member相关的source字段, 暂时直接操作Member对象
# 	Member.objects.filter(id=member.id).update(source=SOURCE_MEMBER_QRCODE)
#
# @when(u"{webapp_user_name}通过识别弹层中的带参数二维码关注{mp_user_name}的公众号")
# def step_tmpl(context, webapp_user_name, mp_user_name):
# 	group_rule_id = context.group_rule_id
# 	channel_qrcode_name = __get_channel_qrcode_name(group_rule_id)
# 	context.execute_steps(u'when %s扫描带参数二维码"%s"' % (webapp_user_name, channel_qrcode_name))
#
# @when(u"{webapp_user_name}点击{shared_webapp_user_name}分享的微助力活动链接")
# def step_tmpl(context, webapp_user_name, shared_webapp_user_name):
# 	webapp_owner_id = context.webapp_owner_id
# 	user = User.objects.get(id=webapp_owner_id)
# 	openid = "%s_%s" % (webapp_user_name, user.username)
# 	group_rule_id = context.group_rule_id
# 	response = __get_into_group_pages(context,webapp_owner_id,group_rule_id,openid)
# 	# context.powerme_result = response.context
# 	context.rank_response = __get_group_rank_informations(context,webapp_owner_id,group_rule_id,openid).content
#
# @when(u"微信用户批量参加{webapp_owner_name}的微助力活动")
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
# 			'powerme_value': row['powerme_value'],
# 			'parti_time': bdd_util.get_datetime_str(row['parti_time']),
# 			'name': row['name']
# 		}
# 		webapp_owner_id = context.webapp_owner_id
# 		user = User.objects.get(id=webapp_owner_id)
# 		openid = "%s_%s" % (webapp_user_name, user.username)
# 		group_rule_id = str(__get_group_rule_id(data['name']))
# 		member = member_api.get_member_by_openid(openid, context.webapp_id)
# 		#先进入微助力页面
# 		response = __get_into_group_pages(context,webapp_owner_id,group_rule_id,openid)
# 		context.group_rule_id = group_rule_id
# 		context.rank_response = __get_group_rank_informations(context,webapp_owner_id,group_rule_id,openid).content
# 		context.execute_steps(u"when %s把%s的微助力活动链接分享到朋友圈" % (webapp_user_name, webapp_owner_name))
# 		powered_member_info = PowerMeParticipance.objects.get(member_id=member.id, belong_to=group_rule_id)
# 		powered_member_info.update(set__created_at=data['parti_time'])
# 		i = 0
# 		webapp_test_user_name = 'test_user_'
# 		while i < int(data['powerme_value']):
# 			i += 1
# 			context.execute_steps(u"When 清空浏览器")
# 			context.execute_steps(u"When %s关注%s的公众号" % (webapp_test_user_name+str(i), webapp_owner_name))
# 			context.execute_steps(u"When %s访问%s的webapp" % (webapp_test_user_name+str(i), webapp_owner_name))
# 			context.execute_steps(u"When %s点击%s分享的微助力活动链接进行助力" % (webapp_test_user_name+str(i), webapp_user_name))
# 	context.execute_steps(u"When 更新助力排名")
#
# @then(u'{webapp_user_name}获得微助力活动提示"{err_msg}"')
# def step_tmpl(context, webapp_user_name, err_msg):
# 	expected = err_msg
# 	actual = context.err_msg
# 	context.tc.assertEquals(expected, actual)
