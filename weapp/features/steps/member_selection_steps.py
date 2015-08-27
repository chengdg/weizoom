# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *


@When(u'{user}访问会员列表')
def step_impl(context, user):
    pass

@then(u'{user}获得会员列表默认查询条件')
def step_impl(context, user):
    context.url = '/member/api/members/get/?design_mode=0&version=1&status=1&count_per_page=50&page=1&enable_paginate=1'

@Then(u'{user}获得刷选结果人数')
def step_impl(context, user):
    response = context.client.get(bdd_util.nginx(context.url))
    actual_count = json.loads(response.content)['data']['total_count']
    json_data = json.loads(context.text)
    expected_count = json_data[0]['result_quantity']
    #print 'hellokitty',expected_count,':',actual_count
    assert int(expected_count) == int(actual_count)


@When(u'{user}设置会员查询条件')
def step_impl(context, user):
    status_dict = {u'全部':'-1',u'已关注':'1',u'取消关注':'0'}
    sources_dict = {u'全部':'-1',u'直接关注':'0',u'推广扫码':'1',u'会员分享':'2'}
    grades_dict = {}
    tags_dict = {}
    members_filter_params = context.client.get('/member/api/members_filter_params/get/')
    for item in json.loads(members_filter_params.content)['data']['grades']:
        grades_dict[item['name']] = item['id']
    for item in json.loads(members_filter_params.content)['data']['tags']:
        tags_dict[item['name']] = item['id']
    options = json.loads(context.text)[0]
    options_url = []
    init_url = '/member/api/members/get/?design_mode=0&version=1&status=1&filter_value='
    if options['pay_money_start'] and options['pay_money_end']:
        options_url.append('pay_money:%s--%s' %(options['pay_money_start'],options['pay_money_end']))
    if options['integral_start'] and options['integral_end']:
        options_url.append('integral:%s--%s' %(options['integral_start'],options['integral_end']))
    if options['pay_times_start'] and options['pay_times_end']:
        options_url.append('pay_times:%s--%s' %(options['pay_times_start'],options['pay_times_end']))
    #最后购买时间
    if options['last_buy_start_time'] and options['last_buy_end_time']:
        options_url.append('first_pay:%s--%s' %(options['last_buy_start_time'],options['last_buy_end_time']))
    if options['attention_start_time'] and options['attention_end_time']:
        options_url.append('sub_date:%s--%s' %(options['attention_start_time'],options['attention_end_time']))
    if options['message_start_time'] and options['message_end_time']:
        options_url.append('last_message_time:%s--%s' %(options['message_start_time'],options['message_end_time']))
    if options['name']:
        options_url.append('name:%stag_id:%s' %(options['name'],''))
    ###
    if options['tags'] and options['tags'] != u'全部':
        options_url.append('tag_id:%s' %tags_dict[options['tags']])
    ###
    if options['member_rank'] and options['member_rank'] != u'全部':
        options_url.append('grade_id:%s' %grades_dict[options['member_rank']])
    # if options['status'] :
    #     if options['status'] == u'全部':
    #         context.url = '/member/api/members/get/?design_mode=0&version=1&count_per_page=50&page=1&enable_paginate=1'
    #     else:
    #         options_url.append('status:%s' %status_dict[options['status']])
    ###
    if options['status'] :
        options_url.append('status:%s' %status_dict[options['status']])
    if options['source'] and options['tags'] != u'全部':
        options_url.append('source:%s' %sources_dict[options['source']])
    init_url = init_url +'|'.join(options_url) + '&page=1&count_per_page=50&enable_paginate=1'
    context.url = init_url
    #print 'helloworld',context.url

        



