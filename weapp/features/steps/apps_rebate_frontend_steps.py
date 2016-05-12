#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

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

@when(u'{webapp_user_name}扫描返利活动"{record_name}"的二维码')
def step_impl(context, webapp_user_name, record_name):
    rebate = get_app_by_name(rebate_models.Rebate, record_name)
    assert rebate is not None
    owner_id = rebate.owner_id
    owner = User.objects.get(id=owner_id)
    ticket = rebate.ticket
    # 模拟收到的消息
    openid = get_openid(webapp_user_name, owner.username)
    url = '/simulator/api/mp_user/qr_subscribe/?version=2'
    webapp_id = bdd_util.get_webapp_id_via_owner_id(owner_id)
    data = {
        "timestamp": "1402211023857",
        "webapp_id": webapp_id,
        "ticket": ticket,
        "from_user": openid
    }
    response = context.client.post(url, data)
    response_data = json.loads(response.content)
    context.qa_result = response_data['data']
