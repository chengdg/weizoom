# -*- coding: utf-8 -*-
__author__ = 'guoliyan'
import json
import time
from test import bdd_util
from market_tools.tools.weizoom_card.models import *

#######################################################################
# __supplement_weizoom_card: 补足一个钱包的数据
#######################################################################
def __supplement_weizoom_card(weizoom_rule):
    weizoom_rule_prototype = {
        "name": u"微众钱包",
        "money": u"100",
        "number": u"10",
        "remark": u"备注"
    }

    weizoom_rule_prototype.update(weizoom_rule)
    return weizoom_rule_prototype


#######################################################################
# __add_weizoom_rule: 添加一个钱包
#######################################################################
def __add_weizoom_rule(context, weizoom_card):
    weizoom_card = __supplement_weizoom_card(weizoom_card)
    __process_activity_data(weizoom_card)
    context.client.post("/market_tools/weizoom_card/weizoom_card/create/", weizoom_card)


@when(u"{user}创建钱包")
def step_impl(context, user):
    client = context.client
    context.weizoom_rules = json.loads(context.text)
    for weizoom_rule in context.weizoom_rules:
        __add_weizoom_rule(context, weizoom_rule)
        time.sleep(1)


@then(u"{user}能获取钱包'{weizoom_card_rule_name}'")
def step_impl(context, user, weizoom_card_rule_name):
    context.client = bdd_util.login(user)
    client = context.client
    rule = WeizoomCardRule.objects.filter(name=weizoom_card_rule_name)
    response = client.get('/market_tools/weizoom_card/weizoom_card_rule_detail/?id=%s' % rule.id)
    weizoom_rule = response.context['weizoom_card_rule']
    actual_data = []
    data_weizoom_rule = {
        "name": weizoom_rule.name,
        "money": weizoom_rule.money,
        "Number": weizoom_rule.number,
        "Remarks": weizoom_rule.remark
    }
    #获取微众卡
    response = client.get('/market_tools/weizoom_card/api/weizoom_cards/get/?weizoom_card_rule_id=%s' % rule.id)
    weizoom_cards = json.loads(response.data.items)
    data_cards = []
    for c in weizoom_cards:
        data_cards.append({
            'card_id': c['weizoom_card_id'],
            'password': c['password']
        })
    data_weizoom_rule['cards'] = data_cards

    expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual_data)


@given(u"{user}已有微众卡支付权限")
def step_impl(context, user):
    client = context.client
    AccountHasWeizoomCardPermissions.objects.create(owner_id=client.user.id,is_can_use_weizoom_card=True)


@given(u"{user}已创建微众卡")
def step_impl(context, user):
    """
    e.g.:
    {
        "cards":[{
            "id":"0000001",
            "password":"1234567",
            "status":"未激活",
            "price":5.00
        },{
            "id":"0000002",
            "password":"1231231",
            "status":"已过期",
            "price":5.00
        }]
    }
    """
    client = context.client
    user = client.user
    WeizoomCardRule.objects.filter(owner=user).delete()
    rule = WeizoomCardRule.objects.create(
        owner=user,
        name='a',
        money=100,
        count=10,
        remark="",
        expired_time="3000-12-12 00:00:00",
        valid_time_from = "2000-1-1 00:00:00"
        valid_time_to = "3000-12-12 00:00:00"
        )

    weizoom_cards = json.loads(context.text)
    for card in weizoom_cards.get('cards'):
        status, is_expired = _get_status(card['status'])
        WeizoomCard.objects.create(
            owner_id=user.id,
            weizoom_card_rule=rule,
            status = status,
            money = card['price'],
            weizoom_card_id = card['id'],
            password = card['password'],
            expired_time = "3000-12-12 00:00:00",
            is_expired = is_expired
        )

def _get_status(status_str):
    is_expired = False
    status = WEIZOOM_CARD_STATUS_UNUSED
    if status_str == u"未使用":
        status = WEIZOOM_CARD_STATUS_UNUSED
    if status_str == u"已使用":
        status = WEIZOOM_CARD_STATUS_USED
    if status_str == u"已用完":
        status = WEIZOOM_CARD_STATUS_EMPTY
    if status_str == u"未激活":
        status = WEIZOOM_CARD_STATUS_INACTIVE

    if status_str == u"已过期":
        is_expired = True
        status = WEIZOOM_CARD_STATUS_INACTIVE
    return status, is_expired

def _get_weizoom_card_log(expense_records):
    data = []
    for record in expense_records:
        item = {
            "merchant": record.owner.username,
            "order_id": record.event_type,
            "price": float(record.money)
        }
        data.append(item)
    return data


@then(u"{user}能获取微众卡'{weizoom_card_id}'")
def step_impl(context, user, weizoom_card_id):
    context.client = bdd_util.login(user)
    client = context.client
    card = WeizoomCard.objects.get(weizoom_card_id=weizoom_card_id)
    response = client.get('/market_tools/weizoom_card/weizoom_card/%s/expense_record/' % card.id)
    card = response.context['card']
    expense_records = response.context['expense_records']

    expected_json = json.loads(context.text)
    status,_ = _get_status(expected_json['status'])
    actual_data = {
        "status": int(status),
        "price": float(expected_json['price'])
    }
    expected = {
        "status": int(card.status),
        "price": float(card.money)
    }
    # 是否需要验证日志
    if expected_json.get('log'):
        actual_data['log'] = expected_json.get('log')
        expected['log'] = _get_weizoom_card_log(expense_records)

    # print("*"*80, "能获取微众卡")
    # from pprint import pprint
    # pprint(expected)
    # pprint(actual_data)
    # print("*"*120)

    bdd_util.assert_dict(expected, actual_data)


@when(u"{user}开通使用微众卡权限")
def step_impl(context, user):
    client = context.client
    AccountHasWeizoomCardPermissions.objects.create(owner_id=client.user.id,is_can_use_weizoom_card=True)


@when(u"{webapp_user}使用'微众卡兑换积分'进行兑换")
def step_impl(context, webapp_user):
    client = context.client
    webapp_owner_id = context.webapp_owner_id
    url = '/webapp/api/project_api/call/'
    args = json.loads(context.text)

    # 获取微众卡id
    data = {
        "woid": webapp_owner_id,
        "module": 'mall',
        "target_api": "weizoom_card/check",
        "project_id": "market_tool:weizoom_card:{}".format(webapp_owner_id),
        "name": args.get("id"),
        "password": args.get("password")
    }
    response = context.client.post(url, data)
    response_json = json.loads(response.content)

    if response_json.get('code') == 200:
        # 根据微众卡id兑换积分
        data = {
            "woid": webapp_owner_id,
            "module": 'mall',
            "target_api": "weizoom_card_to_integral/change",
            "project_id": "market_tool:weizoom_card:{}".format(webapp_owner_id),
            "card_id": response_json.get("data").get('id')
        }
        response = context.client.post(url, data)
    else:
        context.server_error_msg=response_json.get("data").get('msg')
