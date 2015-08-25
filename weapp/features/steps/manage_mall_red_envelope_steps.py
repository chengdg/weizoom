#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
from mall import module_api as mall_api
from mall.promotion import models as  promotion_models

def __get_coupon_rule_id(coupon_rule_name):
    coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
    return coupon_rule.id

default_date = '2000-01-01'
def __get_date(date):
    date = bdd_util.get_date_str(date)
    if date == default_date:
        date = ''

    return date

def __get_actions(rule):
    actions = []
    if rule['is_timeout'] and not rule['limit_time']:
        actions = [u'删除', u'查看']
    elif not rule['status']:
        actions = [u"开启", u"删除", u"查看"]
    elif rule['status']:
        actions = [u"关闭", u"查看"]
    return actions

@when(u'{user}添加分享红包')
def step_impl(context, user):
    rules = json.loads(context.text)
    for rule in rules:
        limit_money = rule.get('limit_money', 0)
        if limit_money == u'无限制':
            limit_money = 0
        params = {
            'owner': context.client.user,
            'name': rule.get('name', ''),
            'coupon_rule': __get_coupon_rule_id(rule.get('prize_info', '')),
            'start_date': __get_date(rule.get('start_date', default_date)),
            'end_date': __get_date(rule.get('end_date', default_date)),
            'limit_money': limit_money,
            'detail': rule.get('detail', ''),
            'share_pic': rule.get('logo_url', ''),
            'remark': rule.get('desc', '')
        }
        response = context.client.post('/mall2/api/red_envelope_rule/?_method=put', params)
        bdd_util.assert_api_call_success(response)

@then(u'{user}能获取分享红包列表')
def step_impl(context, user):
    response = context.client.get('/mall2/api/red_envelope_rule_list/')
    rules = json.loads(response.content)['data']['items']
    status2name = {
        True: u'开启',
        False: u'关闭'
    }
    actual = []
    for rule in rules:
        actual.append({
            'name': rule['rule_name'],
            'status': status2name[rule['status']], 
            'actions': __get_actions(rule)
        })
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)

def __get_red_envelope_rule_id(red_envelope_rule_name):
    red_envelope_rule = promotion_models.RedEnvelopeRule.objects.get(name=red_envelope_rule_name)
    return red_envelope_rule.id

action2code = {
    u'开启': 'start',
    u'关闭': 'over', 
    u'删除': 'delete'
}
@when(u'{user}-{action}分享红包"{red_envelope_rule_name}"')
def step_impl(context, user, action, red_envelope_rule_name):
    id = __get_red_envelope_rule_id(red_envelope_rule_name)
    params = {
        'id': id,
        'status': action2code[action]
    }

    response = context.client.post('/mall2/api/red_envelope_rule/?_method=post', params)
    api_code = json.loads(response.content)['code']

    if api_code == 500:
        err_msg = json.loads(response.content)['errMsg']
        context.err_msg = err_msg
    else:
        bdd_util.assert_api_call_success(response)

@then(u'{user}获得错误提示"{err_msg}"')
def step_impl(context, user, err_msg):
   context.tc.assertEquals(context.err_msg, err_msg)