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
from apps.customerized_apps.vote.models import vote, voteParticipance
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
	typeName_dic={u"文本选项":'appkit.textselection',u"图片选项":'appkit.imageselection',u"参与人信息":'appkit.textlist'}
	if typeName in typeName_dic:
		return typeName_dic[typeName]
	else:
		return typeName

def __get_vote_id(vote_name):
	return vote.objects.get(name=vote_name).id

def __get_into_vote_pages(context,webapp_owner_id,vote_id,openid):
	#进入投票页面
	url = '/m/apps/vote/m_vote/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (webapp_owner_id, vote_id, context.member.token, openid)
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

def __participate_vote(context,webapp_owner_id,vote_id):
	if context.text:
		termite_data = json.loads(context.text)
	else:
		termite_data = context.termite_data
	cid = 0
	data = {}
	"""
	格式例如：
	# type: "问答题":
			   [{
	# values:	   "title":"问答题",
				   "value":"bill问答题内容"
			   }]
	"""
	for type,values in termite_data.iteritems():
		for v in values:
			if type == u"参与人信息":
				cid_1 = cid+1
				for k,v in v['value'].iteritems():
					item_name = __itemName2item(k) if k!=u'' else ''
					name = '0'+ str(cid_1) +'_'+item_name if cid_1 < 10 else str(cid_1) +'_'+item_name
					data[name] = {
						'type': 'appkit.textlist',
						'value': v
					}
					cid_1 += 1
				cid = cid_1
			else:
				item_name = v['title']
				name = '0'+ str(cid) +'_'+item_name if cid < 10 else str(cid)+'_'+item_name
				if type == u"文本选项":
					value = {}
					cid_1 = cid+1
					for n in v['value']:
						selectionInputName = '0'+ str(cid_1)+'_'+ n['title'] if cid_1 < 10 else str(cid_1)+'_'+ n['title']
						if n['type'] == u'单选':
							selectionInputType = "radio"
						else:
							selectionInputType = "checkbox"
						value[selectionInputName] = {
							'type': selectionInputType,
							'isSelect': __name2Bool(n['isSelect'])
						}
						cid_1 += 1
					cid = cid_1
				else:
					value = v['value']

				data[name] = {
					'type': __typeName2type(type) if type!=u'' else '',
					'value': value
				}
	related_page_id = vote.objects.get(id=vote_id).related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	prize = page['component']['components'][0]['model']['prize']
	params = {
		'webapp_owner_id': webapp_owner_id,
		'belong_to': vote_id,
		'termite_data': json.dumps(data),
		'prize': json.dumps(prize)
	}
	response = context.client.post('/m/apps/vote/api/vote_participance/?_method=put', params)
	context.response_json = json.loads(response.content)

@when(u'{webapp_user_name}参加微信投票活动"{vote_name}"于"{date}"')
def step_impl(context,webapp_user_name,vote_name,date):
	context.termite_data = json.loads(context.text)
	date = bdd_util.get_date(date)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	vote_id = __get_vote_id(vote_name)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	if member:
		is_already_participanted = (voteParticipance.objects(belong_to=str(vote_id), member_id=member.id).count() > 0 )
	else:
		is_already_participanted = False
	if is_already_participanted:
		context.vote_hint = u'您已参与'
	else:
		response = __get_into_vote_pages(context,webapp_owner_id,vote_id,openid)
		activity_status = response.context['activity_status']
		if activity_status == u'已结束':
			context.vote_hint = u'活动已结束'
		elif activity_status == u'未开始':
			context.vote_hint = u'请等待活动开始...'
		elif activity_status == u'进行中':
			permission = response.context['permission']
			isMember =  response.context['isMember']
			if permission == 'member':
				if isMember:
					__participate_vote(context,webapp_owner_id,vote_id)
					#修改参与时间
					vote_info = voteParticipance.objects.get(member_id=member.id, belong_to=str(vote_id))
					vote_info.update(set__created_at=date)
				else:
					pass #弹二维码
			else:
				__participate_vote(context,webapp_owner_id,vote_id)
				#修改参与时间
				vote_info = voteParticipance.objects.get(member_id=member.id, belong_to=str(vote_id))
				vote_info.update(set__created_at=date)

			response_json = context.response_json
			if response_json['code'] == 200:
				context.vote_hint = u"提交成功"


@When(u"{webapp_user_name}把{webapp_owner_name}的微信投票活动'{vote_name}'的活动链接分享到朋友圈")
def step_impl(context, webapp_user_name, webapp_owner_name,vote_name):
	context.shared_url = context.link_url

@When(u"{webapp_user_name}点击{shared_webapp_user_name}分享的微信投票活动'{vote_name}'的活动链接")
def step_impl(context, webapp_user_name, shared_webapp_user_name,vote_name):
	vote_id = __get_vote_id(vote_name)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	__get_into_vote_pages(context,webapp_owner_id,vote_id,openid)
