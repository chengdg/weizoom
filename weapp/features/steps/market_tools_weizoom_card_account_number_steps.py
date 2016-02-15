# -*- coding: utf-8 -*-
__author__ = 'slzhu'
import json
import time

from test import bdd_util
from features.testenv.model_factory import *
from market_tools.tools.weizoom_card.models import *


@given(u"{user}已有的账号")
def step_impl(context, user):
    context.accounts = json.loads(context.text)
    for account in context.accounts:
        username = account['account_number']
        UserFactory.create(username=username)

@when(u"{user}添加账号")
def step_impl(context, user):
    accounts = json.loads(context.text)
    for account in accounts:
        params = {
            "username": account['account_number'],
            "nickname": account['name']
        }
        context.client.post('/market_tools/weizoom_card/api/user/create/', params)


@then(u"{user}能获取账号列表")
def step_impl(context, user):
    expected = json.loads(context.text)
    response = context.client.get('/market_tools/weizoom_card/api/accounts/get')
    data = json.loads(response.content)['data']
    items = data['items']
    actual = []
    for item in items:
        actual_item = {}
        actual_item['name'] = item['nickname']
        actual_item['account_number'] = item['username']
        actual.append(actual_item)
    bdd_util.assert_list(sorted(expected), sorted(actual))