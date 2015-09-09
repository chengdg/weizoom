# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from add_multy_text_picture_steps import adict_addNews
@When (u"{user}已编辑图文'{news_title}'")
def step_impl(context, user, news_title):
    #获取图文的类型及id
    materials_url = '/new_weixin/api/materials/'
    response = context.client.get(bdd_util.nginx(materials_url))
    newses_info = json.loads(response.content)['data']['items']
    for news_info in newses_info:
        if news_info['newses'][0]['title'] == news_title:
            material_id = news_info['id']
            material_type = news_info['type']
            post_info = news_info
    #获取该图文的url
    post_url = '/new_weixin/api/%s_news/' % material_type
    #获取编辑图文的内容
    post_data = json.loads(context.text)
    data = []
    print 'justing',post_info['newses']
    for index,addNews in enumerate(post_data):
        adict = adict_addNews(addNews)
        adict['id'] = post_info['newses'][index]['id']
        data.append(adict)
    response = context.client.post(post_url,{'data':json.dumps(data),'material_id':material_id})

    

