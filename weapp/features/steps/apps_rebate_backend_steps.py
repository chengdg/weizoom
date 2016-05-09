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

def __change_select(select):
    return '1'if select == "true" else '0'

@when(u'{user}新建返利活动')
def step_add_red_envelope_rule(context, user):
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

# @then(u'{user}获得返利活动列表')
# def step_impl(context, user):
#     param = {}
#     if hasattr(context, 'query_param'):
#         # 如果给定了query_param，则模拟按条件查询
#         # print("query_param: {}".format(context.query_param))
#         query_param = context.query_param
#         param['name'] = query_param.get('name', '')
#         coupon_name = query_param.get('prize_info', u"所有奖励")
#         if coupon_name  == u"所有奖励":
#             param['couponRule'] = 0
#         else:
#             owner_id = bdd_util.get_user_id_for(user)
#             coupon_rule = CouponRule.objects.get(owner_id=owner_id, name=coupon_name)
#             param['couponRule'] = coupon_rule.id
#         start_date = query_param.get('start_date', '')
#         if len(start_date)>0:
#             param['startDate'] = bdd_util.get_date(query_param['start_date']).strftime('%Y-%m-%d 00:00')
#         else:
#             param['startDate'] = ''
#         end_date = query_param.get('end_date', '')
#         if len(end_date)>0:
#             param['endDate'] = bdd_util.get_date(query_param['end_date']).strftime('%Y-%m-%d 00:00')
#         else:
#             param['endDate'] = ''
#         #param.update(context.query_param)
#     response = context.client.get('/apps/red_envelope/api/red_envelope_rule_list/?_method=get', param)
#     rules = json.loads(response.content)['data']['items']
#     status2name = {
#         True: u'开启',
#         False: u'关闭'
#     }
#
#     # 构造实际数据
#     actual = []
#     for rule in rules:
#         actual.append({
#             'name': __get_name(rule),
#             'status': status2name[rule['status']],
#             'is_permanant_active': rule['limit_time'],
#             'actions': __get_actions(rule),
#             'start_date': __to_date(rule['start_time']),
#             'end_date': __to_date(rule['end_time']),
#             'prize_info': [ rule['coupon_rule_name'] ],
#             'surplus': {
#                 'surplus_count': rule['remained_count'],
#                 'surplus_text': is_warring2text[rule['is_warring']]
#             }
#         })
#     print("actual_data: {}".format(actual))
#
#     expected = json.loads(context.text)
#     for expect in expected:
#         if 'start_date' in expect:
#             if expect['start_date'] == '':
#                 expect['start_date'] = default_date
#             else:
#                 expect['start_date'] = bdd_util.get_date_str(expect['start_date'])
#         if 'end_date' in expect:
#             if expect['end_date'] == '':
#                 expect['end_date'] = default_date
#             else:
#                 expect['end_date'] = bdd_util.get_date_str(expect['end_date'])
#     print("expected: {}".format(expected))
#
#     bdd_util.assert_list(expected, actual)

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
