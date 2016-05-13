#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

import time
import random
from behave import *
from mall.models import Order
from modules.member.models import Member,MemberInfo

from test import bdd_util
from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
import datetime as dt
from utils.string_util import byte_to_hex
from apps.customerized_apps.rebate import models as rebate_models
from apps_step_utils import *
from weixin2.models import Material, News

def __create_random_ticket():
    ticket = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return '%s%03d' % (ticket, random.randint(1, 999))


@when(u'{webapp_user_name}扫描返利活动"{record_name}"的二维码')
def step_impl(context, webapp_user_name, record_name):
    rebate = get_app_by_name(rebate_models.Rebate, record_name)
    rebate.ticket = __create_random_ticket()
    rebate.save()
    assert rebate is not None
    owner_id = rebate.owner_id
    owner = User.objects.get(id=owner_id)
    ticket = rebate.ticket
    debug_print(ticket)
    # 模拟收到的消息
    openid = get_openid(webapp_user_name, owner.username)
    url = '/simulator/api/mp_user/qr_subscribe/?version=2'
    webapp_id = bdd_util.get_webapp_id_via_owner_id(owner_id)
    data = {
        "timestamp": "1463055119171",
        "webapp_id": webapp_id,
        "ticket": ticket,
        "from_user": openid
    }
    response = context.client.post(url, data)
    response_data = json.loads(response.content)
    context.qa_result = response_data['data']
    debug_print(context.qa_result)

@then(u'{user}获得"{record_name}"列表')
def step_impl(context, user, record_name):
    expected_data = json.loads(context.text)
    app = get_app_by_name(rebate_models.Rebate, record_name)
    #首先进入活动列表页面
    url = "/apps/rebate/rebates/"
    get_response(context, url)
    #获取列表
    response = get_response(context, {
        "app": "apps/rebate",
        "resource": "rebates",
        "method": "get",
        "type": "api",
        "args": {
            "count_per_page": 10,
            "page": 1,
            "enable_paginate": 1
        }
    })
    items = json.loads(response.content)['data']['items']
    actual_data = {}
    for item in items:
        if item['name'] == expected_data['code_name']:
            item['code_name'] = item['name']
            actual_data = item
            break
    bdd_util.assert_dict(expected_data, actual_data)

@then(u'{webapp_user_name}能获得返利微众卡')
def step_impl(context, webapp_user_name):
    expected = json.loads(context.text)
    actual = []

    #获取微众卡
    webapp_owner_id = context.webapp_owner_id
    user = User.objects.get(id=context.webapp_owner_id)
    openid = "%s_%s" % (webapp_user_name, user.username)
    url = '/workbench/jqm/preview/?module=market_tool:weizoom_card&model=weizoom_card_exchange_list&action=get&workspace_id=market_tool:weizoom_card&webapp_owner_id=%s&project_id=0&fmt=%s&opid=%s' % (webapp_owner_id, context.member.token, openid)
    url = bdd_util.nginx(url)
    response = context.client.get(url)
    while response.status_code == 302:
        print('[info] redirect by change fmt in shared_url')
        redirect_url = bdd_util.nginx(response['Location'])
        context.last_url = redirect_url
        response = context.client.get(bdd_util.nginx(redirect_url))
    if response.status_code == 200:
        cards = response.context['cards']['card']
        print('cards!!!!!!!!!!!!!!')
        print(cards)
        data_cards = []
        for card in cards:
            data_cards.append({
                'id': card['card_id']
            })
        bdd_util.assert_list(expected, actual)
    else:
        print('[info] redirect error,response.status_code :')
        print(response.status_code)

@when(u"{user}绑定手机号'{phone_number}'")
def step_impl(context,user,phone_number):
    username_hexstr = byte_to_hex(user)
    member_id = Member.objects.get(username_hexstr = username_hexstr).id
    member_info = MemberInfo.objects.filter(member_id = member_id)
    if member_info.count() > 0:
        member_info[0].update(
            phone_number = phone_number,
            is_binded = True
        )
    else:
        MemberInfo.objects.create(
            member_id = member_id,
            phone_number = phone_number,
            is_binded = True,
            sex = 0,
            name = user
        )
