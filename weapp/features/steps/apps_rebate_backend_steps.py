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
