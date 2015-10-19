#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
#from mall import module_api as mall_api
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule

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

@given(u'{user}已添加分享红包')
def step_impl(context, user):
    step_add_red_envelope_rule(context, user)

@when(u'{user}添加分享红包')
def step_add_red_envelope_rule(context, user):
    rules = json.loads(context.text)
    for rule in rules:
        limit_money = rule.get('limit_money', 0)
        if limit_money == u'无限制':
            limit_money = 0
        if rule('receive_method', '') == u'下单领取':
            receive_method = 0
        else:
            receive_method = 1
        params = {
            'owner': context.client.user,
            'name': rule.get('name', ''),
            'coupon_rule': __get_coupon_rule_id(rule.get('prize_info', '')),
            'start_date': __get_date(rule.get('start_date', default_date)),
            'end_date': __get_date(rule.get('end_date', default_date)),
            'receive_method': receive_method,
            'limit_money': limit_money,
            'detail': rule.get('detail', ''),
            'share_pic': rule.get('logo_url', ''),
            'remark': rule.get('desc', '')
        }
        response = context.client.post('/apps/red_envelope/api/red_envelope_rule/?_method=put', params)
        bdd_util.assert_api_call_success(response)

def __to_date(str):
    return dt.datetime.strptime(str, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d')

@then(u'{user}能获取分享红包列表')
def step_impl(context, user):
    # context.query_param由When...指定
    param = {}
    if hasattr(context, 'query_param'):
        # 如果给定了query_param，则模拟按条件查询
        #print("query_param: {}".format(context.query_param))
        query_param = context.query_param
        param['name'] = query_param['name']
        coupon_name = query_param['prize_info'] 
        if coupon_name  == u"所有奖励":
            param['couponRule'] = 0
        else:
            owner_id = bdd_util.get_user_id_for(user)
            coupon_rule = CouponRule.objects.get(owner_id=owner_id, name=coupon_name)
            param['couponRule'] = coupon_rule.id
        start_date = query_param.get('start_date', '')
        if len(start_date)>0:
            param['startDate'] = bdd_util.get_date(query_param['start_date']).strftime('%Y-%m-%d 00:00')
        else:
            param['startDate'] = ''
        end_date = query_param.get('end_date', '')
        if len(end_date)>0:
            param['endDate'] = bdd_util.get_date(query_param['end_date']).strftime('%Y-%m-%d 00:00')
        else:
            param['endDate'] = ''
        #param.update(context.query_param)

    response = context.client.get('/apps/red_envelope/api/red_envelope_rule_list/', param)
    rules = json.loads(response.content)['data']['items']

    status2name = {
        True: u'开启',
        False: u'关闭'
    }

    # 构造实际数据
    actual = []
    for rule in rules:
        actual.append({
            'name': rule['rule_name'],
            'status': status2name[rule['status']], 
            'actions': __get_actions(rule),
            'start_date': __to_date(rule['start_time']),
            'end_date': __to_date(rule['end_time']),
            'prize_info': [ rule['coupon_rule_name'] ]
        })
    print("actual_data: {}".format(actual))

    expected = json.loads(context.text)
    for expect in expected:
        if 'start_date' in expect:
            expect['start_date'] = bdd_util.get_date_str(expect['start_date'])
        if 'end_date' in expect:
            expect['end_date'] = bdd_util.get_date_str(expect['end_date'])
    print("expected: {}".format(expected))

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

    response = context.client.post('/apps/red_envelope/api/red_envelope_rule/?_method=post', params)
    api_code = json.loads(response.content)['code']

    if api_code == 500:
        err_msg = json.loads(response.content)['errMsg']
        context.err_msg = err_msg
    else:
        bdd_util.assert_api_call_success(response)


@then(u'{user}获得错误提示"{err_msg}"')
def step_impl(context, user, err_msg):
   context.tc.assertEquals(context.err_msg, err_msg)

is_can2code = {
    u'能够': True,
    u'不能': False
}
@then(u'{member}-{is_can}领取分享红包')
def step_impl(context, member, is_can):
    client = context.client
    pay_result = context.pay_result
    is_show_red_envelope = pay_result['is_show_red_envelope']
    if is_show_red_envelope:
        red_envelope_rule_id = pay_result['red_envelope_rule_id']
        order = steps_db_util.get_latest_order()
        url = '/workbench/jqm/preview/?module=market_tool:share_red_envelope&model=share_red_envelope&action=get&webapp_owner_id=%s&order_id=%s&red_envelope_rule_id=%s&fmt=%s' % (context.webapp_owner_id, order.id, red_envelope_rule_id, context.member.token)
        url = bdd_util.nginx(url)
        context.red_envelope_url = url
        response = context.client.get(url)
    
    context.tc.assertEquals(is_show_red_envelope, is_can2code[is_can])

@When(u'{webapp_user_name}把{webapp_owner_name}的分享红包链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name):
    context.shared_url = context.red_envelope_url

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享红包链接')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
    webapp_owner_id = context.webapp_owner_id
    user = User.objects.get(id=webapp_owner_id)
    openid = "%s_%s" % (webapp_user_name, user.username)
    member = member_api.get_member_by_openid(openid, context.webapp_id)


    if member:
        new_url = url_helper.remove_querystr_filed_from_request_path(context.shared_url, 'fmt')
        context.shared_url = "%s&fmt=%s" % (new_url, member.token)
    response = context.client.get(context.shared_url)

    if response.status_code == 302:
        print('[info] redirect by change fmt in shared_url')
        redirect_url = bdd_util.nginx(response['Location'])
        context.last_url = redirect_url
        response = context.client.get(bdd_util.nginx(redirect_url))
    else:
        print('[info] not redirect')
        context.last_url = context.shared_url