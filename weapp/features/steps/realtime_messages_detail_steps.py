# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time
from behave import *
from test import bdd_util
from django.test.client import Client

label_dict = {u'所有信息':-1,u'未读信息':0,u'未回复':1,u'有备注':2,u'星标信息':3}
@When (u"{user}查看'{weapp_user}'的消息详情")
def step_impl(context, user, weapp_user):
    #获取weapp_user的url
    realMsg_url = '/new_weixin/api/realtime_messages/?filter_value=status:-1'
    response = context.client.get(bdd_util.nginx(realMsg_url))
    realMsgs_data = json.loads(response.content)['data']['items']
    for realMsg_data in realMsgs_data:
        if realMsg_data['sender_username'] == weapp_user:
            session_id = realMsg_data['session_id']
            reply = realMsg_data['could_replied']
            context.detail_url = '/new_weixin/api/realtime_messages_detail/?session_id=%s&replied=%s' %(session_id, reply)
            break
    

@Then (u"{user}获得'{weapp_user}'消息详情消息列表")
def step_impl(context, user, weapp_user):

    #获取消息详情的数据并处理
    response = context.client.get(bdd_util.nginx(context.detail_url))
    realMsgs_data = json.loads(response.content)['data']['items']
    actual_data = []
    for realMsg_data in realMsgs_data:
        adict = {}
        if realMsg_data['is_reply']:
            adict['member_name'] = realMsg_data['mp_username'] or user
        else:
            adict['member_name'] = realMsg_data['sender_username']
        adict['inf_content'] = realMsg_data['text']
        if realMsg_data['is_news_type']:
            adict['inf_content'] = realMsg_data['news_title']
        adict['time'] = bdd_util.get_date_str(realMsg_data['created_at'][:10])
        actual_data.append(adict)
    expected_datas = json.loads(context.text)
    for expected_data in expected_datas:
        expected_data['time'] = bdd_util.get_date_str(expected_data['time'])
    print 'justing:',expected_datas, '\n', actual_data
    bdd_util.assert_list(expected_datas, actual_data)



