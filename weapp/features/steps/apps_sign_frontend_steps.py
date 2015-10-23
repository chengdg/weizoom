# -*- coding: utf-8 -*-
__author__ = 'aix'

import json

from behave import *

from test import bdd_util


@when(u'{user}进入{mp_user}的签到页面')
def step_tmpl(context, user, mp_user):
    webapp_owner_id = bdd_util.get_user_id_for(mp_user)
    response = context.client.get('/m/apps/sign/m_sign/?webapp_owner_id=%d' % webapp_owner_id)
    context.response = response


@then(u'{user}获取"签到活动1"内容')
def step_tmpl(context, user):
    rules = json.loads(context.text)
    response_context = context.response.context
    print response_context
    bdd_util.assert_dict(response_context, rules)