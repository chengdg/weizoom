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

@when(u'{user}添加分享红包')
def step_impl(context, user):
    rules = json.loads(context.text)
    for rule in rules:
        limit_money = rule.get('limit_money', 0)
        if limit_money == u'无限制':
            limit_money = 0
        data = {
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
        response = context.client.post('/mall2/api/red_envelope_rule/?_method=put', data)
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
            'status': status2name[rule['status']]
        })
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)
