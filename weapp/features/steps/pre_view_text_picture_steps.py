# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client

@When (u"{user}预览图文'{news_title}'")
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
    context.url = '/new_weixin/news_preview/?id=%s' % material_id

@Then (u"{user}获得图文'{news_title}'详情")
def step_impl(context, user, news_title):
    response = context.client.get(context.url)
    actual_datas = json.loads(response.context['newses'])
    expected_datas = json.loads(context.text)
    for actual_data in actual_datas:
        actual_data['content'] = actual_data.get('text','')
        actual_data['cover'] = [{'url':actual_data.get('pic_url','')}]
        actual_data['cover_in_the_text'] = actual_data.get('is_show_cover_pic')
        actual_data['jump_url'] = actual_data.get('url', '')
    for expected_data in expected_datas:
        expected_data['cover_in_the_text'] = True if (expected_data.get('cover_in_the_text', True) in ('true', 'yes', 'True', 'Yes', True)) else False
    print 'justing:',expected_datas,'\n',actual_datas
    bdd_util.assert_list(expected_datas, actual_datas)
