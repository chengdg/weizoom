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
from apps.customerized_apps.red_packet.models import RedPacket, RedPacketParticipance, RedPacketControl,RedPacketLog,RedPacketDetail,RedPacketAmountControl
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json


import time
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from modules.member.models import Member


class Command(BaseCommand):
	help = 'start red_packet stats task'
	args = ''

	def handle(self, *args, **options):
		"""

		@param args: clear: 清除所有apps_red_packet_*的缓存
		@param options:
		@return:
		"""
		print 'red_packet timer task start...'
		start_time = time.time()

		"""
		更新已关注会员的点赞详情
		"""
		need_del_red_packet_logs_ids = []
		all_red_packets = RedPacket.objects(status=1)
		red_packet_ids = [str(p.id) for p in all_red_packets]
		red_packet_logs = RedPacketLog.objects(belong_to__in=red_packet_ids)
		red_packet_participances = RedPacketParticipance.objects(belong_to__in=red_packet_ids)
		red_packet_member_ids = [p.helper_member_id for p in red_packet_logs]
		member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=red_packet_member_ids)}

		need_be_add_logs_list = [p for p in red_packet_logs if member_id2subscribe[p.helper_member_id]]
		red_packet_log_ids = [p.id for p in need_be_add_logs_list]
		be_helped_member_ids = [p.be_helped_member_id for p in need_be_add_logs_list]

		need_be_add_logs = red_packet_logs.filter(be_helped_member_id__in=be_helped_member_ids)
		need_be_add_record_ids = [p.belong_to for p in need_be_add_logs]
		#计算点赞金额值
		need_helped_member_id2money = {}
		for m_id in be_helped_member_ids:
			red_packet_log_info = need_be_add_logs.filter(be_helped_member_id=m_id)
			total_help_money = 0
			for i in red_packet_log_info:
				total_help_money += i.help_money
			if not need_helped_member_id2money.has_key(m_id):
				need_helped_member_id2money[m_id] = total_help_money
			else:
				need_helped_member_id2money[m_id] += total_help_money
		for r_id in need_be_add_record_ids:
			for m_id in need_helped_member_id2money.keys():
				need_helped_member_info = red_packet_participances.filter(belong_to=r_id,member_id=m_id).first()
				if not need_helped_member_info.red_packet_status: #如果红包已经拼成功，则不把钱加上去
					need_helped_member_info.update(inc__current_money=need_helped_member_id2money[m_id])
					need_helped_member_info.reload()
					#最后一个通过非会员参与完成目标金额，设置红包状态为成功
					if need_helped_member_info.current_money == need_helped_member_info.red_packet_money:
						need_helped_member_info.update(set__red_packet_status=True, set__finished_time=datetime.now())

		#更新已关注会员的点赞详情
		detail_helper_member_ids = [p.helper_member_id for p in need_be_add_logs_list]
		RedPacketDetail.objects(belong_to__in=need_be_add_record_ids, helper_member_id__in=detail_helper_member_ids).update(set__has_helped=True)
		need_del_red_packet_logs_ids += red_packet_log_ids

		#删除计算过的log
		RedPacketLog.objects(id__in=need_del_red_packet_logs_ids).delete()

		"""
		所有取消关注的用户，设置为未参与，参与记录无效，但是红包状态、发放状态暂时不改变（防止完成拼红包后，通过取关方式再次参与）
		"""
		record_id2members = {}
		all_has_join_member_ids = []
		all_has_join_participances = red_packet_participances.filter(has_join=True)
		for p in all_has_join_participances:
			all_has_join_member_ids.append(p.member_id)
			if record_id2members.has_key(p.belong_to):
				record_id2members[p.belong_to].append(p)
			else:
				record_id2members[p.belong_to] = [p]

		un_subscribed_ids = [m.id for m in Member.objects.filter(id__in=all_has_join_member_ids, is_subscribed=False)]
		need_clear_participances = all_has_join_participances.filter(member_id__in=un_subscribed_ids)
		need_clear_participances_record_ids = [p.belong_to for p in need_clear_participances]
		need_clear_participances.update(set__has_join=False,set__is_valid=False)

		for record_id in need_clear_participances_record_ids:
			try:
				amount_control = RedPacketAmountControl.objects.filter(belong_to=record_id).first()
				amount_control.update(dec__red_packet_amount = 1)
				red_packet_info = all_red_packets.get(id=record_id)
				# 拼手气红包，取关了的参与者，需要把已领取的放回总红包池中
				if red_packet_info.type == u'random':
					random_total_money = float(red_packet_info.random_total_money)
					random_packets_number = float(red_packet_info.random_packets_number)
					random_average = round(random_total_money/random_packets_number,2) #红包金额/红包个数
					for p in need_clear_participances:
						red_packet_info.update(push__random_random_number_list=p.red_packet_money-random_average)
			except:
				print('dec RedPacketAmountControl error!')

		"""
		所有取消关注再关注的参与用户，如果红包已经拼成功，参与状态为已参与（防止完成拼红包后，通过取关方式再次参与）
		"""
		all_unvalid_member_participance = red_packet_participances.filter(is_valid=False)
		all_unvalid_member_participance_ids = [p.member_id for p in all_unvalid_member_participance]
		re_subscribed_ids = [m.id for m in Member.objects.filter(id__in=all_unvalid_member_participance_ids, is_subscribed=True)]

		#已成功的不清除记录，只是使之有效，且不可以重新领取红包（has_join=True）
		need_reset_member_ids = [p.member_id for p in red_packet_participances.filter(member_id__in=re_subscribed_ids, red_packet_status=True)]
		red_packet_participances.filter(member_id__in=need_reset_member_ids).update(set__has_join = True,set__is_valid = True)


		end_time = time.time()
		diff = (end_time-start_time)*1000
		print 'red_packet timer task end...expend %s' % diff

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

@then(u'{webapp_user_name}获得拼红包活动提示"{err_msg}"')
def step_tmpl(context, webapp_user_name, err_msg):
	expected = err_msg
	actual = context.err_msg
	context.tc.assertEquals(expected, actual)

@When(u'更新拼红包信息')
def step_impl(context):
	command = Command()
	command.handle()