# -*- coding: utf-8 -*-
import json
import time

from utils.string_util import byte_to_hex
from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *

def handtime(atime):
    alist = atime.split(' ')
    if len(alist) ==1:
        return alist[0]
    else:
        return ' '.join(alist)
@Then(u'{user}访问所有会员')
def step_impl(context, user):
    ###访问会员详情页：访问会员详情页会使购买信息自动调整正确
    url = '/member/api/members/get/?design_mode=0&version=1&status=1&filter_value=status:-1&page=1&count_per_page=50&enable_paginate=1'
    response = context.client.get(bdd_util.nginx(url))
    items = json.loads(response.content)['data']['items']
    for member_item in items:
        member_detail_url = '/member/member_detail/edit/?id=%s' %member_item['id']
        #print 'kitty',member_detail_url
        visit_member_detail_url = context.client.get(member_detail_url)
    ###以上为访问会员详情页
        p = 'a'
        if member_item['username'] in [u'tom2',u'tom4']:
            p = Member.objects.get(id = member_item['id'])
            p.is_subscribed = False
            p.save()
        if member_item['username'] == u'tom1':
            p = Member.objects.get(id = member_item['id'])
            p.last_pay_time = '2015-01-02'
        if member_item['username'] == u'tom2':
            p = Member.objects.get(id = member_item['id'])
            p.last_pay_time = '2015-02-02'
        if member_item['username'] == u'tom3':
            p = Member.objects.get(id = member_item['id'])
            p.last_pay_time = '2015-03-05'
        if p is not 'a':
            p.save()

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
    print 'hellokittyassert',expected_count,':',actual_count
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
    ###判断时间是否为'今天'
    for key,value in options.items():
        if value ==u'今天':
            options[key] = time.strftime('%Y-%m-%d')
    ###
    options_url = []
    init_url = '/member/api/members/get/?design_mode=0&version=1&status=1&filter_value='
    if options.has_key('pay_money_start') and options.has_key('pay_money_end') :
        if options['pay_money_start'] and options['pay_money_end']:
            options_url.append('pay_money:%s--%s' %(options['pay_money_start'],options['pay_money_end']))
    if options.has_key('integral_start') and options.has_key('integral_end'):
         if options['integral_start'] and options['integral_end']:
            options_url.append('integral:%s--%s' %(options['integral_start'],options['integral_end']))
    if options.has_key('pay_times_start') and options.has_key('pay_times_end'):
        if options['pay_times_start'] and options['pay_times_end']:
            options['pay_times_start'] = handtime(options['pay_times_start'])
            options['pay_times_end'] = handtime(options['pay_times_end'])
            options_url.append('pay_times:%s--%s' %(options['pay_times_start'],options['pay_times_end']))
    #最后购买时间
    if options.has_key('last_buy_start_time') and options.has_key('last_buy_end_time'):
        if options['last_buy_start_time'] and options['last_buy_end_time']:
            options['last_buy_start_time'] = handtime(options['last_buy_start_time'])
            options['last_buy_end_time'] = handtime(options['last_buy_end_time'])
            options_url.append('first_pay:%s--%s' %(options['last_buy_start_time'],options['last_buy_end_time']))
    if options.has_key('attention_start_time') and options.has_key('attention_end_time'):
        if options['attention_start_time'] and options['attention_end_time']:
            options['attention_start_time'] = handtime(options['attention_start_time'])
            options['attention_end_time'] = handtime(options['attention_end_time'])
            options_url.append('sub_date:%s--%s' %(options['attention_start_time'],options['attention_end_time']))
    if options.has_key('message_start_time') and options.has_key('message_end_time'):
        if options['message_start_time'] and options['message_end_time']:
            options['message_start_time'] = handtime(options['message_start_time'])
            options['message_end_time'] = handtime(options['message_end_time'])
            options_url.append('last_message_time:%s--%s' %(options['message_start_time'],options['message_end_time']))
    if options.has_key('name'):
        if options['name']:
            options_url.append('name:%s' %options['name'])
    ###
    if options.has_key('tags'):
        if options['tags'] != u'全部' and options['tags']:
            options_url.append('tag_id:%s' %tags_dict[options['tags']])
    ###
    if options.has_key('member_rank'):
        if options['member_rank'] != u'全部' and options['member_rank']:
            options_url.append('grade_id:%s' %grades_dict[options['member_rank']])
    if options.has_key('status'):
        if options['status']:
            options_url.append('status:%s' %status_dict[options['status']])
    if options.has_key('source'):
        if options['source'] != u'全部' and options['status']:
            options_url.append('source:%s' %sources_dict[options['source']])
    init_url = init_url +'|'.join(options_url) + '&page=1&count_per_page=50&enable_paginate=1'
    context.url = init_url
    context.filter_str = "&filter_value=" + '|'.join(options_url)

