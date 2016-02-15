# -*- coding: utf-8 -*-
# __editor__='justing'
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
#from weixin.message.qa.models import *
from weixin2.models import *
from modules.member.models import *

@when(u"{user}获得实时消息'{type}'列表")
def step_impl(context, user, type):
	if hasattr(context, 'filter_value'):
		filter_value = context.filter_value
	else:
		filter_value = None

	count_per_page = 30
	if hasattr(context, 'count_per_page'):
		count_per_page = context.count_per_page

	page_index = 1
	if hasattr(context, 'page_index'):
		page_index = context.page_index


	url = '/new_weixin/api/realtime_messages/?page=%s&count=%s' % (page_index, count_per_page)
	if type == "所有消息":
		url = '/new_weixin/api/realtime_messages/?page=%s&count=%s' % (page_index, count_per_page)
	elif type == "未读信息":
		url = '/new_weixin/api/realtime_messages/?page=%s&count=%s&filter_value=status:0' % (page_index, count_per_page)
	elif type == "未回复":
		url = '/new_weixin/api/realtime_messages/?page=%s&count=%s&filter_value=status:1' % (page_index, count_per_page)

	if filter_value:
		url = url + '&' + filter_value
	expected = json.loads(context.text)

	response = context.client.get(url)
	session_messages = json.loads(response.content)['data']['items']
	# print('-------url', url)
	# print('---:::::::::::::',session_messages)
	messages = []
	for message in session_messages:
		message_dict = {}
		message_dict['member_name'] = message['sender_username'].split('_')[0]
		message_dict['inf_content'] = message['text']
		message_dict['last_message_time'] = u'今天'
		message_dict['unread_count'] = message['unread_count']
		messages.append(message_dict)
		#now_time = datetime.today().strftime('%Y-%m-%d')

	bdd_util.assert_list(expected, messages)

@when(u"{user}设置实时消息查询条件")
def step_impl(context, user):
	#filter_value=status:1|content:33|tag_id:792|grade_id:142|name:123&date_interval=2015-09-08 00:00|2015-09-15 00:00
	filter_dict = json.loads(context.text)
	filter_list = []
	if filter_dict.has_key('member_name'):
		filter_list.append('name:%s' % filter_dict['member_name'])

	if filter_dict.has_key('inf_content'):
		filter_list.append('content:%s' % filter_dict['inf_content'])

	if filter_dict.has_key('tags'):
		tag_id = MemberTag.objects.get(name=filter_dict['tags']).id
		filter_list.append('tag_id:%s' % tag_id)

	if filter_dict.has_key('member_rank'):
		grade_id = MemberGrade.objects.get(name=filter_dict['member_rank']).id
		filter_list.append('grade_id:%s' % grade_id)

	date_interval = ''
	if filter_dict.has_key('start_date') and  filter_dict.has_key('start_date') :
		# start_date = filter_dict['start_date']
		# end_date = filter_dict['end_date']
		start_date = datetime.today().strftime('%Y-%m-%d')
		end_date = '2099-07-01'
		date_interval = 'date_interval=%s 00:00|%s 00:00' % (start_date,end_date)

	filter_value = None
	if filter_list:
		filter_value = '|'.join(filter_list)
		if filter_value and date_interval:
			filter_value = 'filter_value='+filter_value + '&' + date_interval

		elif date_interval:
			filter_value = date_interval
		else:
			filter_value = 'filter_value='+filter_value
	elif date_interval:
		filter_value = date_interval

	if filter_value:
		context.filter_value = filter_value

@when(u"{user}浏览列表第{page_index}页")
def step_impl(context, user, page_index):
	context.page_index = page_index

@when(u"{user}访问实时消息'{type}'")
def step_impl(context, user, type):
	url = '/new_weixin/api/realtime_messages/?page=1&count=30'
	if type == "所有信息":
		url = '/new_weixin/api/realtime_messages/?page=1&count=30&filter_value=status:-1'
	elif type == "未读信息":
		url = '/new_weixin/api/realtime_messages/?page=1&count=30&filter_value=status:0'
	elif type == "未回复":
		url = '/new_weixin/api/realtime_messages/?page=1&count=30&filter_value=status:1'
	elif type == "有备注":
		url = '/new_weixin/api/realtime_messages/?page=1&count=30&filter_value=status:2'
	elif type == "星标信息":
		url = '/new_weixin/api/realtime_messages/?page=1&count=30&filter_value=status:3'
	context.realtime_messages_url = url

@then(u"{user}获得实时消息'{type}'列表")
def step_impl(context, user, type):
	expected = json.loads(context.text)
	if expected:
		key_words = expected[0].keys()
	url = context.realtime_messages_url
	response = context.client.get(url)
	session_messages = json.loads(response.content)['data']['items']
	messages = []
	for message in session_messages:
		message_dict = {}
		for key in key_words:
			if key == 'member_name':
				message_dict['member_name'] = message['sender_username'].split('_')[0] or user
			elif key == 'inf_content':
				message_dict['inf_content'] = message['text']
			elif key == 'last_message_time':
				message_dict['last_message_time'] = u'今天'
			elif key == 'unread_count':
				message_dict['unread_count'] = message['unread_count']
			elif key == 'remark':
				message_dict['remark'] = message['remark']
			elif key == 'star':
				message_dict['star'] = 'true' if message['is_collected'] else 'false'
		messages.append(message_dict)
		#now_time = datetime.today().strftime('%Y-%m-%d')

	bdd_util.assert_list(expected, messages)


@When (u"{user}修改实时消息备注")
def step_impl(context, user):
    if hasattr(context, 'detail_url'):
        url = context.detail_url
    elif hasattr(context, 'realtime_messages_url'):
        url = context.realtime_messages_url
    else:
        url = '/new_weixin/api/realtime_messages/?filter_value=status:-1'
    response = context.client.get(bdd_util.nginx(url))
    realMsgs_data = json.loads(response.content)['data']['items']
    datas_text = json.loads(context.text)
    for data_text in datas_text:
        for realMsg_data in realMsgs_data:
            if hasattr(context, 'detail_url'):
                if data_text['inf_content'] == realMsg_data['text']:
                    message_id = realMsg_data['message_id']
                    session_id = realMsg_data['session_id']
                    break
            else:
                if data_text['member_name'] == realMsg_data['sender_username'].split('_')[0]:
                    message_id = realMsg_data['message_id']
                    session_id = realMsg_data['session_id']
                    break
        status = 1
        remark = data_text['remark']
        url = '/new_weixin/api/msg_memo/'
        response = context.client.post(url,{'message_id':message_id, 'status':status, 'session_id':session_id, 'message_remark':remark})
