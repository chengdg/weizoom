# -*- coding: utf-8 -*-
__author__ = 'Mark24'

from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
#from mall import module_api as mall_api
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule
from weixin.message.material import models as material_models
import termite.pagestore as pagestore_manager
from apps.customerized_apps.sign.models import Sign
import json
import re


def __debug_print(content,type_tag=True):
    """
    debug工具函数
    """
    if content:
        print '++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++'
        if type_tag:
            print "====== Type ======"
            print type(content)
            print "==================="
        print content
        print '++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++'
    else:
        pass


@when(u'{user}进入{mp_user}的签到页面')
def step_tmpl(context, user, mp_user):
    # webapp_owner_id = bdd_util.get_user_id_for(mp_user)
    # response = context.client.get('/m/apps/sign/m_sign/?webapp_owner_id=%d' % webapp_owner_id)
    # context.response = response
    pass


@then(u'{user}获取"签到活动1"内容')
def step_tmpl(context, user):
    # rules = json.loads(context.text)
    # response_context = context.response.context
    # print response_context
    # bdd_util.assert_dict(response_context, rules)
    pass

@then(u"{user}获得系统回复的消息'{answer}'")
def step_impl(context, user, answer):
    result = context.qa_result["data"]
    begin = result.find('<div class="content">') + len('<div class="content">')
    end = result.find('<a', begin)
    actual  = result[begin:end]
    if answer:
        answer = answer
    expected = answer
    if expected == 'None':
        expected = ''
    context.tc.assertEquals(expected, actual)
    link_url = '/m/apps/sign/m_sign/?webapp_owner_id=%s' % (context.webapp_owner_id)
    link_url = bdd_util.nginx(link_url)
    context.link_url = link_url
    print(link_url)

@when(u'{user}点击系统回复的链接')
def step_tmpl(context, user):
    url = "%s&fmt=%s" % (context.link_url, context.member.token)
    response = context.client.get(url)