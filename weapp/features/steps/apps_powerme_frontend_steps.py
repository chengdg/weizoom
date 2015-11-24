#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.powerme.models import PowerMe, PowerMeParticipance, PowerMeControl
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

def __get_power_me_rule_name(title):
	material_url = material_models.News.objects.get(title=title).url
	power_me_rule_name = material_url.split('-')[1]
	return power_me_rule_name

def __get_power_me_rule_id(power_me_rule_name):
	return PowerMe.objects.get(name=power_me_rule_name).id

@When(u'{webapp_user_name}点击图文"{title}"进入微助力活动页面')
def step_impl(context, webapp_user_name, title):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	power_me_rule_name = __get_power_me_rule_name(title)
	power_me_rule_id = __get_power_me_rule_id(power_me_rule_name)
	url = '/m/apps/powerme/m_powerme/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (context.webapp_owner_id, power_me_rule_id, context.member.token, openid)
	url = bdd_util.nginx(url)
	print('url!!!!!!!!')
	print(url)
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
	context.powerme_result = response.context

@then(u"{webapp_user_name}获得{webapp_owner_name}的'{power_me_rule_name}'的内容")
def step_tmpl(context, webapp_user_name, webapp_owner_name, power_me_rule_name):
	result = context.powerme_result
	related_page_id = PowerMe.objects.get(id=result['record_id']).related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_component = page['component']['components'][0]['model']

	color2name = {
		'yellow': u'冬日暖阳',
		'red': u'玫瑰茜红',
		'orange': u'热带橙色'
	}
	# 构造实际数据
	actual = []
	actual.append({
		"name": result['page_title'],
		"is_show_countdown": 'true' if result['timing'] else 'false',
		"desc": page_component['description'],
		"background_pic": page_component['background_image'],
		"background_color": color2name[page_component['color']],
		"rules": page_component['rules'],
		"my_rank": result['current_member_rank_info']['rank'] if result['current_member_rank_info'] else u'无',
		"my_power_score": result['current_member_rank_info']['power'] if result['current_member_rank_info'] else '0',
		"total_participant_count": result['total_participant_count']
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@then(u'{webapp_user_name}获得"{power_me_rule_name}"的助力值排名')
def step_tmpl(context, webapp_user_name, power_me_rule_name):
	result = context.powerme_result
	participances = json.loads(result['participances_list'])
	actual = []
	if participances != []:
		rank = 0
		for p in participances:
			rank += 1
			p_dict = OrderedDict()
			p_dict[u"rank"] = rank
			p_dict[u"name"] = p['username']
			p_dict[u"value"] = p['power']
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

@When(u'{webapp_user_name}把{webapp_owner_name}的微助力活动链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name):
	context.shared_url = context.link_url
	params = {
		'webapp_owner_id': context.webapp_owner_id,
		'id': context.powerme_result['record_id'],
		'fid': context.powerme_result['page_owner_member_id']
	}
	print('params!!!!!!!!!')
	print(params)
	response = context.client.post('/m/apps/powerme/api/powerme_participance/?_method=post', params)
	print('response!!!!!!!!!!!')
	print(response)

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的微助力活动链接进行参与')
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

@then(u"{webapp_user_name}获得弹层提示信息'{text}'")
def step_tmpl(context, webapp_user_name, text):
	pass