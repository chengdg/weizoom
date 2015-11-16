# -*- coding: utf-8 -*-

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

def __get_sign_record_id(webapp_owner_id):
	return Sign.objects.get(owner_id=webapp_owner_id).id

@when(u"{webapp_user_name}进入{webapp_owner_name}签到页面进行签到")
def step_tmpl(context, webapp_user_name, webapp_owner_name):
	webapp_owner_id = context.webapp_owner_id
	appRecordId = __get_sign_record_id(webapp_owner_id)
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': appRecordId
	}
	response = context.client.post('/m/apps/sign/api/sign_participance/?_method=put', params)
	context.datas = json.loads(response.content)['data']

@then(u"{webapp_user_name}获取签到成功的内容")
def step_tmpl(context, webapp_user_name):
	datas = context.datas
	# 构造实际数据
	actual = []
	actual.append({
		'serial_count': datas['serial_count'],
		'daily_prize': {
			'integral': datas['daily_prize']['integral'],
			'coupon': datas['daily_prize']['coupon']['name']
		},
		'curr_prize': {
			'integral': datas['curr_prize']['integral'],
			'coupon': datas['curr_prize']['coupon']['name']
		}
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

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
	context.shared_url = context.link_url

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的签到链接进行签到')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	if member.is_subscribed: #非会员不可签到
		appRecordId = __get_sign_record_id(webapp_owner_id)
		params = {
			'webapp_owner_id': webapp_owner_id,
			'id': appRecordId
		}
		response = context.client.post('/m/apps/sign/api/sign_participance/?_method=put', params)
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