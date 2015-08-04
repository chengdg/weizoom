# -*- coding: utf-8 -*-
__author__ = 'slzhu'
import json
import time

from test import bdd_util
from features.testenv.model_factory import *
from market_tools.tools.weizoom_card.models import *

status2text = {
    WEIZOOM_CARD_STATUS_UNUSED: u'未使用',
    WEIZOOM_CARD_STATUS_USED: u'已被使用',
    WEIZOOM_CARD_STATUS_EMPTY: u'已用完',
    WEIZOOM_CARD_STATUS_INACTIVE: u'未激活'
}
text2status = {
    u'未使用': WEIZOOM_CARD_STATUS_UNUSED,
    u'已被使用': WEIZOOM_CARD_STATUS_USED,
    u'已用完': WEIZOOM_CARD_STATUS_EMPTY,
    u'未激活': WEIZOOM_CARD_STATUS_INACTIVE
}

def __create_weizoom_card_wallet(context, wallets):
    WeizoomCardRule.objects.all().delete()
    WeizoomCard.objects.all().delete()

    context.rule2wallet = {}
    for wallet in wallets:
        name = wallet['name']
        money = wallet['price']
        remark = wallet['remarks']
        card = wallet['card']
        count = card['count']
        password = card['password']
        expire_time_items = wallet['expire_time'].split(' ')
        expired_time = expire_time_items[0]
        expired_hour = expire_time_items[1].split(':')[0]
        expired_minute = expire_time_items[1].split(':')[1]
        params = {
            'name': name,
            'money': money,
            'remark': remark,
            'number': count,
            'expired_time': expired_time,
            'expired_hour': expired_hour,
            'expired_minute': expired_minute
        }
        response = context.client.post('/market_tools/weizoom_card/api/weizoom_cards/create/', params)
        data = json.loads(response.content)['data']
        WeizoomCard.objects.filter(owner=context.client.user, weizoom_card_rule=data['id']).update(password=password)
        context.rule2wallet[name] = data['id']


@given(u"{user}已添加微众卡钱包")
def step_impl(context, user):
    WeizoomCardRule.objects.all().delete()
    WeizoomCard.objects.all().delete()

    wallets = json.loads(context.text)
    __create_weizoom_card_wallet(context, wallets)


@given(u"{user}待激活微众卡")
def step_impl(context, user):
    wallets = []
    wallet = json.loads(context.text)
    wallet_card = {}
    wallet_card['count'] = wallet['count']
    wallet_card['password'] = ''
    wallet['card'] = wallet_card
    wallets.append(wallet)
    __create_weizoom_card_wallet(context, wallets)
    for card in wallet['cards']:
        WeizoomCard.objects.filter(owner=context.client.user, weizoom_card_id=card['id']).update(password=card['password'], status=text2status.get(card['status']))

@when(u"{user}创建微众卡钱包")
def step_impl(context, user):
    wallets = json.loads(context.text)
    __create_weizoom_card_wallet(context, wallets)


@when(u"{user}给微众卡钱包'{wallet_name}'追加{number}张微众卡")
def step_impl(context, user, wallet_name, number):
    params = {
        'rule_id': context.rule2wallet[wallet_name],
        'card_num': number
    }
    context.client.post('/market_tools/weizoom_card/api/weizoom_cards/append/', params)


@when(u"{user}给id为'{card_id}'的微众卡激活")
def step_impl(context, user, card_id):
    WeizoomCard.objects.filter(
                               owner=context.client.user,
                               weizoom_card_id=card_id
    ).update(status=0)


@when(u"{user}给id为'{card_id}'的微众卡停用")
def step_impl(context, user, card_id):
    WeizoomCard.objects.filter(
                               owner=context.client.user,
                               weizoom_card_id=card_id
    ).update(status=1)


@then(u"{user}能获取微众卡钱包'{wallet_name}'")
def step_impl(context, user, wallet_name):
    expected = json.loads(context.text)
    rule_id = context.rule2wallet[wallet_name]

    params = {
        'count_per_page': 10000,
        'weizoom_card_rule_id': rule_id
    }
    wallet_data = WeizoomCardRule.objects.get(id=rule_id)
    response = context.client.get('/market_tools/weizoom_card/api/weizoom_cards/get/', params)
    card_data = json.loads(response.content)['data']

    actual = {}
    actual['name'] = wallet_data.name
    actual['price'] = wallet_data.money
    actual['count'] = wallet_data.count
    actual['expire_time'] = wallet_data.expired_time
    actual['remarks'] = wallet_data.remark
    cards = []
    for card in card_data['items']:
        card_item = {}
        card_item['id'] = card['id']
        card_item['password'] = card['password']
        card_item['status'] = status2text.get(card['status'])
        card_item['price'] = card['money']
        if card['activated_at']:
            card_item['active_time'] = card['activated_at']
        else:
            card_item['active_time'] = ''
        card_item['target'] = card['target_name']
        if card['status'] == WEIZOOM_CARD_STATUS_INACTIVE:
            card_item['actions'] = u'["激活"]'
        else:
            card_item['actions'] = u'["停用"]'
        cards.append(card_item)
    actual['cards'] = cards

    bdd_util.assert_list(sorted(expected), sorted(actual))


@then(u"{user}能获取微众卡钱包列表")
def step_impl(context, user):
    expected = json.loads(context.text)
    params = {
        'count_per_page': 10000
    }
    response = context.client.get('/market_tools/weizoom_card/api/weizoom_card_rules/get/', params)
    wallet_data = json.loads(response.content)['data']

    actual = []
    for wallet in wallet_data['items']:
        actual_item = {}
        actual_item['name'] = wallet['name']
        actual_item['price'] = wallet['money']
        actual_item['count'] = wallet['count']
        actual_item['remarks'] = wallet['remark']
        actual.append(actual_item)
    for ex in expected:
        ex['price'] = '%.2f' % ex['price']
    bdd_util.assert_list(sorted(expected), sorted(actual))
