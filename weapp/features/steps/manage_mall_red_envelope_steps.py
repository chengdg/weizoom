#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from behave import *
from mall.models import Order
from modules.member.models import Member

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
#from mall import module_api as mall_api
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule, RedEnvelopeToOrder
from utils.string_util import byte_to_hex
from weixin.message.material import models as material_models

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
        actions = [u'分析', u'删除', u'查看']
    elif not rule['status']:
        actions = [u'分析', u'开启', u'删除', u'查看']
    elif rule['status'] and not rule['receive_method']:
        actions = [u'分析', u'关闭', u'查看']
    elif rule['receive_method']:#图文领取
        actions = [u'分析', u'删除', u'查看']
    return actions

def __get_name(rule):
    if rule['receive_method']:
        return u'【图文领取】'+rule['rule_name']
    else:
        return rule['rule_name']

def __get_red_envelope_rule_name(title):
    material_url = material_models.News.objects.get(title=title).url
    red_envelope_rule_name = '【图文领取】'+material_url.split('-')[1]
    return red_envelope_rule_name

def __get_material_id(title):
    material_id = material_models.News.objects.get(title=title).material_id
    return material_id

def __get_red_envelope_rule_id(red_envelope_rule_name):
    if red_envelope_rule_name.rfind("【图文领取】")>=0:
        red_envelope_rule_name = red_envelope_rule_name.split("【图文领取】")[1]
        receive_method = 1
    else:
        receive_method = 0
    red_envelope_rule = promotion_models.RedEnvelopeRule.objects.get(name=red_envelope_rule_name,receive_method=receive_method)
    return red_envelope_rule.id

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
        receive_method = rule.get('receive_method', 0)
        if receive_method == u'下单领取':
            receive_method = False #下单领取
        else:
            receive_method = '' #图文领取,receive-method-order为空
        params = {
            'owner': context.client.user,
            'name': rule.get('name', ''),
            'coupon_rule': __get_coupon_rule_id(rule.get('prize_info', '')),
            'start_date': __get_date(rule.get('start_date', default_date)),
            'end_date': __get_date(rule.get('end_date', default_date)),
            'receive-method-order': receive_method,
            'limit_money': limit_money,
            'detail': rule.get('detail', ''),
            'share_pic': rule.get('share_pic', ''),
            'remark': rule.get('remark', '')
        }
        response = context.client.post('/apps/red_envelope/api/red_envelope_rule/?_method=put', params)
        bdd_util.assert_api_call_success(response)

def __to_date(str):
    return dt.datetime.strptime(str, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d')

is_warring2text = {
    True: u'库存告急',
    False: u''
}
@then(u'{user}能获取分享红包列表')
def step_impl(context, user):
    # context.query_param由When...指定
    param = {}
    if hasattr(context, 'query_param'):
        # 如果给定了query_param，则模拟按条件查询
        # print("query_param: {}".format(context.query_param))
        query_param = context.query_param
        param['name'] = query_param.get('name', '')
        coupon_name = query_param.get('prize_info', u"所有奖励")
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
    response = context.client.get('/apps/red_envelope/api/red_envelope_rule_list/?_method=get', param)
    rules = json.loads(response.content)['data']['items']
    status2name = {
        True: u'开启',
        False: u'关闭'
    }

    # 构造实际数据
    actual = []
    for rule in rules:
        actual.append({
            'name': __get_name(rule),
            'status': status2name[rule['status']],
            'is_permanant_active': rule['limit_time'],
            'actions': __get_actions(rule),
            'start_date': __to_date(rule['start_time']),
            'end_date': __to_date(rule['end_time']),
            'prize_info': [ rule['coupon_rule_name'] ],
            'surplus': {
                'surplus_count': rule['remained_count'],
                'surplus_text': is_warring2text[rule['is_warring']]
            }
        })
    print("actual_data: {}".format(actual))

    expected = json.loads(context.text)
    for expect in expected:
        if 'start_date' in expect:
            if expect['start_date'] == '':
                expect['start_date'] = default_date
            else:
                expect['start_date'] = bdd_util.get_date_str(expect['start_date'])
        if 'end_date' in expect:
            if expect['end_date'] == '':
                expect['end_date'] = default_date
            else:
                expect['end_date'] = bdd_util.get_date_str(expect['end_date'])
    print("expected: {}".format(expected))

    bdd_util.assert_list(expected, actual)

action2code = {
    u'开启': 'start',
    u'关闭': 'over', 
    u'删除': 'delete'
}

@when(u"{user}'{action}'分享红包'{red_envelope_rule_name}'")
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
@then(u"{member}'{is_can}'领取分享红包")
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

    followed_member = Member.objects.get(username_hexstr=byte_to_hex(shared_webapp_user_name))
    if member:
        new_url = url_helper.remove_querystr_filed_from_request_path(context.shared_url, 'fmt')
        new_url = url_helper.remove_querystr_filed_from_request_path(new_url, 'opid')
        context.shared_url = "%s&fmt=%s" % (new_url, followed_member.token)

    response = context.client.get(context.shared_url)
    if response.status_code == 302:
        print('[info] redirect by change fmt in shared_url')
        redirect_url = bdd_util.nginx(response['Location'])
        context.last_url = redirect_url
        response = context.client.get(bdd_util.nginx(redirect_url))
    else:
        print('[info] not redirect')
        context.last_url = context.shared_url

@When(u'{webapp_user_name}点击图文"{title}"')
def step_impl(context, webapp_user_name, title):
    user = User.objects.get(id=context.webapp_owner_id)
    openid = "%s_%s" % (webapp_user_name, user.username)
    red_envelope_rule_name = __get_red_envelope_rule_name(title)
    red_envelope_rule_id = __get_red_envelope_rule_id(red_envelope_rule_name)
    material_id = __get_material_id(title)
    url = '/workbench/jqm/preview/?module=market_tool:share_red_envelope&model=share_red_envelope&action=get&webapp_owner_id=%s&material_id=%s&red_envelope_rule_id=%s&fmt=%s&opid=%s' % (context.webapp_owner_id, material_id, red_envelope_rule_id, context.member.token,openid)
    url = bdd_util.nginx(url)
    context.red_envelope_url = url
    response = context.client.get(url)
    response = context.client.get(bdd_util.nginx(response['Location']))

@then(u'{user}获取库存提示弹窗')
def step_impl(context, user):
    response = context.client.get('/apps/red_envelope/red_envelope_rule_list/')
    rules = response.context['items']
    # 构造实际数据
    actual = []
    for rule in rules:
        actual.append({
            'name': __get_name(rule),
            'surplus_text': u'即将用完'
        })
    print("actual_data: {}".format(actual))

    expected = json.loads(context.text)
    print("expected: {}".format(expected))

    bdd_util.assert_list(expected, actual)

@then(u'{user}能获得分享红包"{red_envelope_rule_name}"的分析统计')
def step_impl(context, user, red_envelope_rule_name):
    id = __get_red_envelope_rule_id(red_envelope_rule_name)
    params = {
        'id': id
    }
    response = context.client.get('/apps/red_envelope/red_envelope_participances/', params)
    participances = response.context
    actual = [{
        u"新关注人数": participances['new_member_count'],
        u"领取人数": participances['received_count'],
        u"产生消费": participances['consumption_sum'],
	    u"使用人数": participances['total_use_count']
    }]
    print("actual_data: {}".format(actual))

    expected = json.loads(context.text)
    print("expected: {}".format(expected))

    bdd_util.assert_list(expected, actual)

@then(u'{user}能获得分享红包"{red_envelope_rule_name}"的分析详情')
def step_impl(context, user, red_envelope_rule_name):
    id = __get_red_envelope_rule_id(red_envelope_rule_name)
    params = {
        'id': id
    }
    response = context.client.get('/apps/red_envelope/api/red_envelope_participances/?_method=get', params)
    participances = json.loads(response.content)['data']['items']
    actual = []
    for p in participances:
        p_dict = OrderedDict()
        p_dict[u"下单会员"] = p['username_truncated']
        p_dict[u"会员状态"] = p['grade']
        p_dict[u"引入领取人数"] = p['introduce_received_number_count']
        p_dict[u"引入使用人数"] = p['introduce_used_number_count']
        p_dict[u"引入新关注"] = p['introduce_new_member_count']
        p_dict[u"引入消费额"] = p['introduce_sales_number']
        p_dict[u"领取时间"] = p['created_at']
        p_dict[u"使用状态"] = p['coupon_status_name']
        p_dict[u"操作"] = [u'查看引入详情',u'查看使用订单'] if p['coupon_status'] ==1 else u'查看引入详情'
        actual.append((p_dict))
    print("actual_data: {}".format(actual))
    expected = []
    if context.table:
        for row in context.table:
            cur_p = row.as_dict()
            if u'领取时间' in cur_p:
                cur_p[u'领取时间'] = bdd_util.get_date_str(cur_p[u'领取时间'])
            expected.append(cur_p)
    else:
        expected = json.loads(context.text)
    print("expected: {}".format(expected))

    bdd_util.assert_list(expected, actual)

@then(u"{user}能获得分享红包'{red_envelope_rule_name}-{share_member}'订单号'{order_no}'的引入详情")
def step_impl(context, user, red_envelope_rule_name,share_member,order_no):
    id = __get_red_envelope_rule_id(red_envelope_rule_name)

    followed_member = Member.objects.get(username_hexstr=byte_to_hex(share_member))

    order_id = Order.objects.get(order_id=order_no).id
    relation_id = RedEnvelopeToOrder.objects.get(red_envelope_rule_id=id,order_id=order_id).id
    params = {
        'rule_id': id,
        'introduced_by': followed_member.id,
        'relation_id': relation_id
    }
    response = context.client.get('/apps/red_envelope/api/red_envelope_participances/?_method=get', params)
    participances = json.loads(response.content)['data']['items']
    actual = []
    for p in participances:
        p_dict = OrderedDict()
        p_dict[u"分享会员"] = p['username_truncated']
        p_dict[u"会员状态"] = p['grade']
        p_dict[u"引入领取人数"] = p['introduce_received_number_count']
        p_dict[u"引入使用人数"] = p['introduce_used_number_count']
        p_dict[u"引入新关注"] = p['introduce_new_member_count']
        p_dict[u"引入消费额"] = p['introduce_sales_number']
        p_dict[u"领取时间"] = p['created_at']
        p_dict[u"使用状态"] = p['coupon_status_name']
        p_dict[u"操作"] = u'查看使用订单' if p['coupon_status'] ==1 else ""
        actual.append((p_dict))
    print("actual_data: {}".format(actual))
    expected = []
    if context.table:
        for row in context.table:
            cur_p = row.as_dict()
            if u'领取时间' in cur_p:
                cur_p[u'领取时间'] = bdd_util.get_date_str(cur_p[u'领取时间'])
            expected.append(cur_p)
    else:
        expected = json.loads(context.text)
    print("expected: {}".format(expected))

    bdd_util.assert_list(expected, actual)

