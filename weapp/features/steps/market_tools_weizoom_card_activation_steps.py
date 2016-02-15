# -*- coding: utf-8 -*-
__author__ = 'slzhu'
import json
import time

from test import bdd_util
from features.testenv.model_factory import *
from market_tools.tools.weizoom_card.models import *


@given(u"{user}已添加的微众卡目标账号")
def step_impl(context, user):
    if hasattr(context, 'client') is False:
        context.client = bdd_util.login(user, password=None, context=context)
    context.accounts = json.loads(context.text)
    for account in context.accounts:
        username = account['account_number']
        UserFactory.create(username=username)
    WeizoomCardHasAccount.objects.all().delete()
    for account in context.accounts:
        params = {
            "username": account['account_number'],
            "nickname": account['name']
        }
        context.client.post('/market_tools/weizoom_card/api/user/create/', params)

@given(u"{user}已有的微众卡")
def step_impl(context, user):
    weizoom_cards = json.loads(context.text)
    rule = WeizoomCardRule.objects.create(
        owner = context.client.user,
        money = 100,
        expired_time = '2014-11-26 10:10'
    )
    WeizoomCard.objects.all().delete()
    context.id2card = {}
    for weizoom_card in weizoom_cards:
        card = WeizoomCard.objects.create(
            owner = context.client.user,
            weizoom_card_rule = rule,
            weizoom_card_id = weizoom_card['card_number'],
            money = 100,
            expired_time = '2014-11-26 10:10'
        )
        context.id2card[card.weizoom_card_id] = card


@when(u"{user}激活微众卡")
def step_impl(context, user):
    weizoom_cards = json.loads(context.text)
    card_ids = []
    for weizoom_card in weizoom_cards:
        card_ids.append(str(context.id2card.get(weizoom_card['card_number']).id))
    context.card_ids = ",".join(card_ids)


@when(u"{user}能获取微众卡激活目标")
def step_impl(context, user):
    targets = json.loads(context.text)
    for target in targets:
        if target.has_key('whether_you_choose') and target['whether_you_choose'] == u'是':
            card_has_account = WeizoomCardHasAccount.objects.get(account_name=target['name'])
            context.target_id = card_has_account.account.id
    params = {
        "card_ids": context.card_ids,
        "target_id":context.target_id
    }
    context.client.post('/market_tools/weizoom_card/api/batch_status/update', params)


@then(u"{user}获取微众卡")
def step_impl(context, user):
    expected = json.loads(context.text)
    expected_ids = []
    for ex in expected:
        expected_ids.append(ex['id'])
    cards = WeizoomCard.objects.filter(weizoom_card_id__in=expected_ids)
    actual = []
    for card in cards:
        # card_has_account = WeizoomCardHasAccount.objects.get(owner=context.client.user, account_id=card.target_user_id)
        actual_item = {}
        actual_item['id'] = card.weizoom_card_id
        actual_item['card_number'] = card.weizoom_card_id
        actual_item['password'] = card.password
        if card.status == WEIZOOM_CARD_STATUS_UNUSED:
            actual_item['status'] = u'未使用'
        elif card.status == WEIZOOM_CARD_STATUS_USED:
            actual_item['status'] = u'已使用'
        elif card.status == WEIZOOM_CARD_STATUS_EMPTY:
            actual_item['status'] = u'已用完'
        elif card.status == WEIZOOM_CARD_STATUS_INACTIVE:
            actual_item['status'] = u'未激活'
        actual_item['price'] =card.money
        # actual_item['distribution_targets'] = card_has_account.account_name
        actual.append(actual_item)
    print(sorted(expected), sorted(actual))
    bdd_util.assert_list(sorted(expected), sorted(actual))
