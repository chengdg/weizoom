#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'kuki'

from behave import *
from mall.models import Order
from modules.member.models import Member

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
import datetime as dt
from utils.string_util import byte_to_hex
from apps.customerized_apps.rebate import models as rebate_models
from apps_step_utils import *
from weixin2.models import Material, News

def __get_material_id(context,title):
    material_ids = Material.objects.filter(owner_id=context.webapp_owner_id, is_deleted=False).values_list('id', flat=True)
    material_id = News.objects.get(material_id__in=material_ids, title=title).material_id
    return material_id

def __get_rebate_id(rebate_name):
    id = rebate_models.Rebate.objects.get(name=rebate_name).id
    return id

def __change_select(select):
    return '1'if select == "true" else '0'

@when(u'{user}新建返利活动')
def step_impl(context, user):
    rules = json.loads(context.text)
    for rule in rules:
        params = {
            'owner_id': context.client.user,
            'name': rule.get('code_name', ''),
            'start_time': date2time(rule.get('start_time', '')),
            'end_time': date2time(rule.get('end_time', '')),
            'permission': __change_select(rule.get('is_attention_in', '')),
            'is_limit_first_buy': __change_select(rule.get('is_limit_first_buy', '')),
            'is_limit_cash': __change_select(rule.get('is_limit_cash', '')),
            'rebate_order_price': rule.get('order_rebate').get('rebate_order_price'),
            'rebate_money': rule.get('order_rebate').get('rebate_money'),
            'weizoom_card_id_from': rule.get('weizoom_card_id_from', ''),
            'weizoom_card_id_to': rule.get('weizoom_card_id_to', '')
        }
        if rule['reply_type'] == "文字":
            params['reply_type'] = 1
            params['reply_detail'] = rule['scan_code_reply']
            params['reply_material_id'] = 0
        else:
            params['reply_type'] = 2
            params['reply_detail'] = ''
            params['reply_material_id'] = __get_material_id(context,rule['scan_code_reply'])
        response = context.client.post('/apps/rebate/api/rebate/?_method=put', params)
        debug_print(response)
        bdd_util.assert_api_call_success(response)

@when(u'{user}编辑返利活动"{rebate_name}"')
def step_impl(context, user, rebate_name):
    rules = json.loads(context.text)
    for rule in rules:
        params = {
            'id': __get_rebate_id(rebate_name),
            'name': rule.get('code_name', ''),
            'start_time': date2time(rule.get('start_time', '')),
            'end_time': date2time(rule.get('end_time', '')),
            'permission': __change_select(rule.get('is_attention_in', '')),
            'is_limit_first_buy': __change_select(rule.get('is_limit_first_buy', '')),
            'is_limit_cash': __change_select(rule.get('is_limit_cash', '')),
            'rebate_order_price': rule.get('order_rebate').get('rebate_order_price'),
            'rebate_money': rule.get('order_rebate').get('rebate_money'),
            'weizoom_card_id_from': rule.get('weizoom_card_id_from', ''),
            'weizoom_card_id_to': rule.get('weizoom_card_id_to', '')
        }
        if rule['reply_type'] == "文字":
            params['reply_type'] = 1
            params['reply_detail'] = rule['scan_code_reply']
            params['reply_material_id'] = 0
        else:
            params['reply_type'] = 2
            params['reply_detail'] = ''
            params['reply_material_id'] = __get_material_id(context,rule['scan_code_reply'])
        response = context.client.post('/apps/rebate/api/rebate/?_method=post', params)
        bdd_util.assert_api_call_success(response)

@then(u'{user}获得返利活动列表')
def step_impl(context, user):
    param = {}
    if hasattr(context, 'query_param'):
        # 如果给定了query_param，则模拟按条件查询
        # print("query_param: {}".format(context.query_param))
        query_param = context.query_param
        param['name'] = query_param.get('name', '')
        start_time = query_param.get('start_time', '')
        if len(start_time)>0:
            param['start_time'] = date2time(query_param['start_time'])
        else:
            param['start_time'] = ''
        end_time = query_param.get('end_time', '')
        if len(end_time)>0:
            param['end_time'] = date2time(query_param['end_time'])
        else:
            param['end_time'] = ''
        #param.update(context.query_param)
    response = context.client.get('/apps/rebate/api/rebates/?_method=get', param)
    rules = json.loads(response.content)['data']['items']

    # 构造实际数据
    actual = []
    for rule in rules:
        actual.append({
            'code_name': rule['name'],
            'attention_number': rule['attention_number'],
            'order_money': rule['order_money'],
            'first_buy_num': rule['first_buy_num'],
            'start_time': rule['start_time'],
            'end_time': rule['end_time']
        })
    print("actual_data: {}".format(actual))

    expected = json.loads(context.text)
    for expect in expected:
        if 'start_time' in expect:
            expect['start_time'] = date2time(expect['start_time'])
        if 'end_time' in expect:
            expect['end_time'] = date2time(expect['end_time'])
    print("expected: {}".format(expected))

    bdd_util.assert_list(expected, actual)

# action2code = {
#     u'开启': 'start',
#     u'关闭': 'over',
#     u'删除': 'delete'
# }
#
# @when(u"{user}'{action}'返利活动'{red_envelope_rule_name}'")
# def step_impl(context, user, action, red_envelope_rule_name):
#     id = __get_red_envelope_rule_id(red_envelope_rule_name)
#     params = {
#         'id': id,
#         'status': action2code[action]
#     }
#
#     response = context.client.post('/apps/red_envelope/api/red_envelope_rule/?_method=post', params)
#     api_code = json.loads(response.content)['code']
#
#     if api_code == 500:
#         err_msg = json.loads(response.content)['errMsg']
#         context.err_msg = err_msg
#     else:
#         bdd_util.assert_api_call_success(response)

@then(u"{user}能获取'{rebate_name}'会员列表")
def step_impl(context, user, rebate_name):
    rebate_id = str(__get_rebate_id(rebate_name))
    #首先进入页面
    url = "/apps/rebate/rebate_participances/?id="+rebate_id
    get_response(context, url)
    #获取会员列表
    response = get_response(context, {
        "app": "apps/rebate",
        "resource": "rebate_participances",
        "method": "get",
        "type": "api",
        "args": {
            "count_per_page": 50,
            "page": 1,
            "enable_paginate": 1,
            "record_id": rebate_id,
            "is_show": "1" if not hasattr(context, "is_show") else context.is_show
        }
    })

    response_data = json.loads(response.content)
    actual = []
    for item in response_data['data']['items']:
        actual.append({
            "fans_name": item['username'],
            "buy_number": item['pay_times'],
            "integral": item['integral'],
            "price": item['pay_money'],
            "follow_time": item['follow_time']
        })
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)

@when (u"{user}取消对'{rebate_name}'进行'{operation_name}'操作")
def step_impl(context, user, rebate_name, operation_name):
    context.is_show = 0

@then(u"{user}能获取'{rebate_name}'订单列表")
def step_impl(context, user, rebate_name):
    rebate_id = __get_rebate_id(rebate_name)
    # 首先进入页面
    url = "/apps/rebate/rebate_order_list/?id=" + str(rebate_id)
    get_response(context, url)
    # 获取会员列表
    response = get_response(context, {
        "app": "apps/rebate",
        "resource": "rebate_order_list",
        "method": "get",
        "type": "api",
        "args": {
            "count_per_page": 50,
            "page": 1,
            "enable_paginate": 1,
            "record_id": rebate_id,
            "is_show": "1" if not hasattr(context, "is_show") else context.is_show
        }
    })

    response_data = json.loads(response.content)

    context.final_price = response_data['data']['final_price']
    context.weizoom_card_money = response_data['data']['weizoom_card_money']

    actual = []
    for item in response_data['data']['items']:
        order_info = {}
        order_info['order_id'] = item['order_id']
        # order_info['order_time'] = '今天' if item['created_at'].split(" ")[0] == datetime.now().strftime('%Y-%m-%d') else \
        # item['created_at'].split(" ")[0]
        # order_info['payment_time'] = '今天' if item['payment_time'].split(" ")[0] == datetime.now().strftime(
        #     '%Y-%m-%d') else item['payment_time'].split(" ")[0]
        # order_info['consumer'] = item['buyer_name']
        products_list = []
        for product in item['products']:
            product_info = {}
            product_info['name'] = product['name']
            product_info['count']  = product['count']
            product_info['price']  = product['price']
            products_list.append(product_info)

        order_info['products'] = products_list
        order_info['final_price'] = item['pay_money']
        # order_info['pay_type'] = item['pay_interface_name']
        # order_info['postage'] = item['postage']
        # order_info['discount_amount'] = item['save_money']
        # order_info['paid_amount'] = item['pay_money']
        order_info['status'] = item['status']
        actual.append(order_info)

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)

@then(u"{user}获得总消费金额")
def step_impl(context, user):
    actual = {}
    if hasattr(context, 'final_price'):
        actual['cash_payment'] = context.final_price
    if hasattr(context, 'final_price'):
        actual['card_payment'] = context.weizoom_card_money

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)