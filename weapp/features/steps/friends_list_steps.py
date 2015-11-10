# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client


sources_dict = {u'全部':'-1',u'直接关注':'0',u'推广扫码':'1',u'会员分享':'2'}

@Then (u"{user}获得'{webapp_user}'推荐关注统计")
def step_impl(context, user, webapp_user):
    #获取webapp_user 会员的id
    members_url = '/member/api/member_list/'
    response = context.client.get(bdd_util.nginx(members_url))
    members_list = json.loads(response.content)['data']['items']
    for member in members_list:
        if webapp_user == member['username']:
            context.member_id = member['id']
    #访问推荐关注的api并获取数据
    if not hasattr(context, 'focus_url'):
        context.focus_url = '/member/api/follow_relations/?member_id=%s&only_fans=true' %context.member_id
    response = context.client.get(bdd_util.nginx(context.focus_url))
    context.focus_data = json.loads(response.content)['data']
    #获取实际数据
    actual_data = {}
    actual_data['new_members'] = context.focus_data['population']
    actual_data['ordered_members'] = context.focus_data['population_order']
    actual_data['pay_money'] = context.focus_data['amount']

    expected_data = json.loads(context.text)

    bdd_util.assert_dict(expected_data, actual_data)
    

@Then (u"{user}获得'{webapp_user}'推荐关注列表")
def step_impl(context, user, webapp_user):
    actual_data = context.focus_data['items']
    for data in actual_data:
        data['pay_money'] = float(data['pay_money'])
    expected_data = []
    for row in context.table:
        adict = {}
        adict['username'] = row['member']
        adict['pay_money'] = float(row['pay_money'])
        adict['integral'] = row['integral']
        adict['source'] = sources_dict[row['Source']]
        adict['created_at'] = bdd_util.get_date_str(row['attention_time'])
        expected_data.append(adict)
    bdd_util.assert_list(expected_data, actual_data)


@Then (u"{user}获得'{webapp_user}'好友列表统计")
def step_impl(context, user, webapp_user):
    if not hasattr(context, 'friend_url'):
        context.friend_url = '/member/api/follow_relations/?member_id=%s&only_fans=flase&count_per_page=20' %context.member_id
    response = context.client.get(bdd_util.nginx(context.friend_url))
    context.friend_data = json.loads(response.content)['data']
    #获取实际数据
    actual_data = {}
    actual_data['friend_count'] = context.friend_data['population']
    actual_data['ordered_members'] = context.friend_data['population_order']
    actual_data['pay_money'] = context.friend_data['amount']

    expected_data = json.loads(context.text)

    bdd_util.assert_dict(expected_data, actual_data)

@Then (u"{user}获得'{webapp_user}'好友列表")
def step_impl(context, user, webapp_user):
    actual_data = context.friend_data['items']
    for data in actual_data:
        data['pay_money'] = float(data['pay_money'])
    expected_data = []
    for row in context.table:
        adict = {}
        adict['username'] = row['member']
        adict['pay_money'] = float(row['pay_money'])
        adict['integral'] = row['integral']
        adict['source'] = sources_dict[row['Source']]
        adict['father_name'] = row['recommended']
        adict['created_at'] = bdd_util.get_date_str(row['attention_time'])
        expected_data.append(adict)
    bdd_util.assert_list(expected_data, actual_data)


@When (u"{user}访问'{webapp_user}'推荐关注页")
def step_impl(context, user, webapp_user):
    #获取webapp_user 会员的id
    members_url = '/member/api/member_list/'
    response = context.client.get(bdd_util.nginx(members_url))
    members_list = json.loads(response.content)['data']['items']
    for member in members_list:
        if webapp_user == member['username']:
            context.member_id = member['id']
    #访问推荐关注的api并获取数据
    context.focus_url = '/member/api/follow_relations/?member_id=%s&only_fans=true&count_per_page=%s' %(context.member_id,context.count_per_page)
    context.friend_url = '/member/api/follow_relations/?member_id=%s&only_fans=false&count_per_page=%s' %(context.member_id,context.count_per_page)


@Then (u"{user}获得'{webapp_user}'推荐关注列表显示共{total_page}页")
def step_impl(context, user, webapp_user, total_page):
    response = context.client.get(bdd_util.nginx(context.focus_url))
    context.focus_data = json.loads(response.content)['data']
    actual_page = context.focus_data['pageinfo']['max_page']
    assert(int(total_page),int(actual_page))

@When (u"{user}浏览推荐关注列表第{cur_page}页")
def step_impl(context, user, cur_page):
    context.focus_url = '/member/api/follow_relations/?member_id=%s&only_fans=true&count_per_page=%s&page=%s' %(
        context.member_id,context.count_per_page, cur_page)
    response = context.client.get(bdd_util.nginx(context.focus_url))
    context.focus_data = json.loads(response.content)['data']


@Then (u"{user}获得'{webapp_user}'好友列表显示共{total_page}页")
def step_impl(context, user, webapp_user, total_page):
    response = context.client.get(bdd_util.nginx(context.friend_url))
    context.friend_data = json.loads(response.content)['data']
    actual_page = context.friend_data['pageinfo']['max_page']
    assert(int(total_page),int(actual_page))

@When (u"{user}浏览好友列表第{cur_page}页")
def step_impl(context, user, cur_page):
    context.friend_url = '/member/api/follow_relations/?member_id=%s&only_fans=false&count_per_page=%s&page=%s' %(
        context.member_id,context.count_per_page, cur_page)
    response = context.client.get(bdd_util.nginx(context.friend_url))
    context.friend_data = json.loads(response.content)['data']


