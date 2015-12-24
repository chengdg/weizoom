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
from apps.customerized_apps.survey.models import survey, surveyParticipance
from utils.string_util import byte_to_hex
import json
import re

def __itemName2item(itemName):
	itemName_dic={u"姓名":'name',u"手机":'phone',u"邮箱":'email',u"QQ":'qq',u"qq":'qq',u"职位":"job",u"住址":"addr"}
	if itemName in itemName_dic:
		return itemName_dic[itemName]
	else:
		return itemName

def __name2Bool(name):
	name_dic = {u'是':True,u'否':False}
	if name:
		return name_dic[name]
	else:
		return None

def __typeName2type(typeName):
	typeName_dic={u"问答题":'appkit.qa',u"选择题":'appkit.selection',u"快捷模块":'appkit.textlist',u"上传图片":'appkit.uploadimg'}
	if typeName in typeName_dic:
		return typeName_dic[typeName]
	else:
		return typeName

def __get_survey_id(survey_name):
	return survey.objects.get(name=survey_name).id

def __get_into_survey_pages(context,webapp_owner_id,survey_id,openid):
	#进入微助力活动页面
	url = '/m/apps/survey/m_survey/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, survey_id, context.member.token, openid)
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

def __participate_survey(context,webapp_owner_id,survey_id):
	termite_data = json.loads(context.text)
	i = 0
	data = {}
	for k,v in termite_data.iteritems():
		print(k)
		print(v)
		for v in v:
			if k == u"快捷模块":
				item_name = __itemName2item(k) if k!=u'' else ''
			else:
				item_name = v['title']
			name = '0'+str(i)+'_'+item_name
			if k == u"选择题":
				value = {}
				j = i+1
				for n in v['value']:
					selectionInputName = str(j)+'_'+ n['title']
					if n['type'] == u'单选':
						selectionInputType = "radio"
					else:
						selectionInputType = "checkbox"
					value[selectionInputName] = {
						'type': selectionInputType,
						'isSelect': __name2Bool(n['isSelect'])
					}
					j += 1
				i = j
			else:
				value = v['value']

			data[name] = {
				'type': __typeName2type(k) if k!=u'' else '',
				'value': value
			}
			i += 1
	related_page_id = survey.objects.get(id=survey_id).related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	prize = page['component']['components'][0]['model']['prize']
	params = {
		'webapp_owner_id': webapp_owner_id,
		'belong_to': survey_id,
		'termite_data': json.dumps(data),
		'prize': json.dumps(prize)
	}
	response = context.client.post('/m/apps/survey/api/survey_participance/?_method=put', params)
	context.response_json = json.loads(response.content)

@when(u"{webapp_user_name}参加{webapp_owner_name}的用户调研活动'{survey_name}'")
def step_impl(context,webapp_user_name,webapp_owner_name,survey_name):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	survey_id = __get_survey_id(survey_name)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	response = __get_into_survey_pages(context,webapp_owner_id,survey_id,openid)
	if member:
		is_already_participanted = (surveyParticipance.objects(belong_to=str(survey_id), member_id=member.id).count() > 0 )
	else:
		is_already_participanted = False
	if is_already_participanted:
		context.survey_hint = u'您已参与'
	else:
		activity_status = response.context['activity_status']
		if activity_status == u'已结束':
			context.survey_hint = u'活动已结束'
		elif activity_status == u'未开始':
			context.survey_hint = u'请等待活动开始...'
		elif activity_status == u'进行中':
			permission = response.context['permission']
			print(permission)
			isMember =  response.context['isMember']
			print(isMember)
			if permission == 'member':
				if isMember:
					__participate_survey(context,webapp_owner_id,survey_id)
				else:
					pass #弹二维码
			else:
				__participate_survey(context,webapp_owner_id,survey_id)

			response_json = context.response_json
			if response_json['code'] == 200:
				context.survey_hint = u"提交成功"

@When(u"{webapp_user_name}把{webapp_owner_name}的用户调研活动'{survey_name}'的活动链接分享到朋友圈")
def step_impl(context, webapp_user_name, webapp_owner_name,survey_name):
	context.shared_url = context.link_url

@When(u"{webapp_user_name}点击{shared_webapp_user_name}分享的用户调研活动'{survey_name}'的活动链接")
def step_impl(context, webapp_user_name, shared_webapp_user_name,survey_name):
	survey_id = __get_survey_id(survey_name)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	__get_into_survey_pages(context,webapp_owner_id,survey_id,openid)


# @When(u"微信用户批量参加{webapp_owner_name}的微信抽奖活动")
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
# 			'name': row['name'],
# 			'webapp_user_name': webapp_user_name,
# 			'prize_grade': row['prize_grade'],
# 			'prize_name': row['prize_name'],
# 			'survey_time': row['survey_time'],
# 			'receive_status': row['receive_status']
# 		}
# 		context.execute_steps(u'when %s参加微信抽奖活动"%s"于"%s"' % (webapp_user_name, data['name'], data['survey_time']))