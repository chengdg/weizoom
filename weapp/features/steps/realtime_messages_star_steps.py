# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time
from behave import *
from test import bdd_util
from django.test.client import Client

label_dict = {u'所有信息':-1,u'未读信息':0,u'未回复':1,u'有备注':2,u'星标信息':3}


@When (u"{user}修改实时消息星标")
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


            else:
                if data_text['member_name'] == realMsg_data['sender_username'].split('_')[0]:
                    message_id = realMsg_data['message_id']
                    
                    break
        status = 0 if (data_text.get('star', True) in ('true', 'yes', 'True', 'Yes', True)) else 1
        url = '/new_weixin/api/message_collect/'
        response = context.client.post(url,{'message_id':message_id, 'status':status})

