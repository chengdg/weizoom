#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

import time
import random
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

def __create_random_ticket():
    ticket = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return '%s%03d' % (ticket, random.randint(1, 999))


@when(u'{webapp_user_name}扫描返利活动"{record_name}"的二维码')
def step_impl(context, webapp_user_name, record_name):
    rebate = get_app_by_name(rebate_models.Rebate, record_name)
    rebate = update_apps_status(rebate)
    if rebate.ticket == "":
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