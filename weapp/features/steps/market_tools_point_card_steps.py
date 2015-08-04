# -*- coding: utf-8 -*-
import json
import time
from test import bdd_util
from market_tools.tools.point_card.models import *


def __add_point_card(context, point_card):
    context.client.post('/market_tools/point_card/point_card_rule/create/', point_card)

@when(u"{user}添加积分卡规则")
def step_impl(context, user):
    client = context.client
    point_cards = json.loads(context.text)

    for point_card in point_cards:
        __add_point_card(context, point_card)

@given(u"{user}添加积分卡规则")
def step_impl(context, user):
    client = context.client
    point_cards = json.loads(context.text)

    for point_card in point_cards:
        __add_point_card(context, point_card)

@then(u"{user}能获得积分卡规则'{point_card}'")
def step_impl(context, user, point_card):
    expected = json.loads(context.text)
    point_card_rule = PointCardRule.objects.get(name=point_card)

    response = context.client.get('/market_tools/point_card/point_card_rule/update/%d/' % point_card_rule.id)
    actual_data = response.context['point_card_rule']
    actual = {}
    actual['name'] = actual_data.name
    actual['prefix'] = actual_data.prefix
    actual['point'] = str(actual_data.point)
    bdd_util.assert_dict(expected, actual)

@then(u"{user}能获得积分卡规则列表")
def step_impl(context, user):
    expected = json.loads(context.text)

    response = context.client.get('/market_tools/point_card/')
    actual_data = response.context['point_card_rules']
    actual = []
    for rule in actual_data:
        actual.append({
            "name": rule.name
    })

    bdd_util.assert_list(expected, actual)

@when(u'{user}手工为积分卡规则生成积分卡')
def step_impl(context, user):
    point_cards_info = json.loads(context.text)
    rule_id = PointCardRule.objects.get(name=point_cards_info['point_card_rule']).id
    point_cards_info['rule_id'] = rule_id
    context.client.post('/market_tools/point_card/api/point_card/create/', point_cards_info)

@then(u'jobs能获得积分卡列表')
def step_impl(context):
    point_cards = json.loads(context.text)
    expected = point_cards
    response = context.client.get('/market_tools/point_card/api/records/get/')
    actual_data = json.loads(response.content)['data']['items']
    actual = []
    for point_card in actual_data:
        if point_card['status'] == 0:
            status = u'未使用'
        elif point_card['status'] == 1:
            status = u'已被使用'
        else:
            status = u'已过期'
        actual.append({
            "point_card_rule_name": point_card['point_card_rule_name'],
            "point": str(point_card['point']),
            "status": status
        })
    bdd_util.assert_list(expected, actual)

