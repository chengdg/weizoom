# -*- coding: utf-8 -*-
__author__ = 'Mark24'

from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.sign.models import Sign
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re


def __debug_print(content,type_tag=True):
	"""
	debug工具函数
	"""
	if content:
		print '++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++'
		if type_tag:
			print "====== Type ======"
			print type(content)
			print "==================="
		print content
		print '++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++'
	else:
		pass

def __get_sign_record_id(webapp_owner_id):
	return Sign.objects.get(owner_id=webapp_owner_id).id

@when(u'{webapp_user_name}进入{webapp_owner_name}签到页面进行签到')
def step_tmpl(context, webapp_user_name, webapp_owner_name):
	webapp_owner_id = context.webapp_owner_id
	appRecordId = __get_sign_record_id(webapp_owner_id)
	url = 'm/apps/sign/api/sign_participance/?design_mode=0&version=2&method=put&webapp_owner_id=%s&id=%s' % (webapp_owner_id, appRecordId)
	url = bdd_util.nginx(url)
	print('url!!!!')
	print(url)
	response = context.client.get(url)
	redirect_url = bdd_util.nginx(response['Location'])
	context.last_url = redirect_url
	response = context.client.get(bdd_util.nginx(redirect_url))
	print('response!!!!!!!!!!!!!!')
	print(response.status_code)
	print(response)


@then(u'{user}获取"{sign}"的内容')
def step_tmpl(context, user,sign):
	url = '/m/apps/sign/m_sign/?webapp_owner_id=%s' % (context.webapp_owner_id)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	response = context.client.get(bdd_util.nginx(response['Location']))

@then(u"{user}获得系统回复的消息'{answer}'")
def step_impl(context, user, answer):
	result = context.qa_result["data"]
	begin = result.find('<div class="content">') + len('<div class="content">')
	if result.find('<a href=') != -1: #result存在a标签
		end = result.find('<a', begin)
		link_url = '/m/apps/sign/m_sign/?webapp_owner_id=%s' % (context.webapp_owner_id)
		link_url = bdd_util.nginx(link_url)
		context.link_url = link_url
	else:
		end = result.find('</div>', begin)
	actual  = result[begin:end]
	expected = answer
	if answer == ' ':
		expected = ''
	context.tc.assertEquals(expected, actual)


@when(u'{user}点击系统回复的链接')
def step_tmpl(context, user):
	url = "%s&fmt=%s" % (context.link_url, context.member.token)
	context.sign_url = url
	response = context.client.get(url)

@when(u"修改系统时间为'{date}'")
def step_impl(context, date):
	if date == u'1天后':
		context.now_date = datetime.now()
		delta = timedelta(days=1)
		next_date = (context.now_date + delta).strftime('%Y-%m-%d')
	elif date == u'2天后':
		delta = timedelta(days=2)
		next_date = (context.now_date + delta).strftime('%Y-%m-%d')
	os.system("date %s" %(next_date))

@when(u'还原系统时间')
def step_impl(context):
	os.system("date %s" %(context.now_date))

@When(u'{webapp_user_name}把{webapp_owner_name}的签到活动链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name):
	context.shared_url = context.sign_url
	print('context.shared_url1111111',context.shared_url)

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的签到链接')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	if member.is_subscribed: #非会员不可签到
		followed_member = Member.objects.get(username_hexstr=byte_to_hex(shared_webapp_user_name))
		if member:
			new_url = url_helper.remove_querystr_filed_from_request_path(context.shared_url, 'fmt')
			new_url = url_helper.remove_querystr_filed_from_request_path(new_url, 'opid')
			context.shared_url = "%s&fmt=%s" % (new_url, followed_member.token)
			print('context.shared_url22222222',context.shared_url)
		response = context.client.get(context.shared_url)
		print('response!!!!!!!!!!!!!')
		print(response)
		if response.status_code == 302:
			print('[info] redirect by change fmt in shared_url')
			redirect_url = bdd_util.nginx(response['Location'])
			context.last_url = redirect_url
			response = context.client.get(bdd_util.nginx(redirect_url))
			print('response22222222222!!!!!!!!!!!!!')
			print(response)
		else:
			print('[info] not redirect')
			context.last_url = context.shared_url
	else:
		pass

@When(u'{webapp_user_name}通过弹出的二维码关注{mp_user_name}的公众号')
def step_impl(context, webapp_user_name, mp_user_name):
	context.execute_steps(u"when %s关注%s的公众号" % (webapp_user_name, mp_user_name))
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	# 因没有可用的API处理Member相关的source字段, 暂时直接操作Member对象
	Member.objects.filter(id=member.id).update(source=SOURCE_MEMBER_QRCODE)