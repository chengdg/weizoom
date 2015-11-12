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
    webapp_owner_id = bdd_util.get_user_id_for(mp_user)

    __debug_print(webapp_owner_id)
    url_0 = '/m/apps/sign/m_sign/?webapp_owner_id=%d' % webapp_owner_id
    response_0 = context.client.get(url_0)


    prefix,url_1 = response_0['Location'].split('&')
    url_1 = url_0+"&"+url_1
    response_1 = context.client.get(url_1)
    __debug_print(url_1)
    __debug_print(response_1)


    context.response_0 = response_0

    __debug_print(response_0)
    # context.response_1 = response_1


@then(u'{user}获取"{sign}"内容')
def step_tmpl(context, user,sign):
    rules = json.loads(context.text)
    # response_context = context.response.context
    # print response_context
    # bdd_util.assert_dict(response_context, rules)
    pass

@then(u"{user}获得系统回复的消息'{answer}'")
def step_impl(context, user, answer):
    result = context.qa_result["data"]
    begin = result.find('<div class="content">') + len('<div class="content">')
    if result.find('<a href=') != -1: #result存在a标签
        end = result.find('<a', begin)
        link_url = '/m/apps/sign/m_sign/?webapp_owner_id=%s' % (context.webapp_owner_id)
        link_url = bdd_util.nginx(link_url)
        context.link_url = link_url
    else:
        end = result.find('</div>', begin)
    actual  = result[begin:end]
    expected = answer
    if answer == ' ':
        expected = ''
    context.tc.assertEquals(expected, actual)


@when(u'{user}点击系统回复的链接')
def step_tmpl(context, user):
    url = "%s&fmt=%s" % (context.link_url, context.member.token)
    response = context.client.get(url)

@when(u"修改系统时间为'{date}'")
def step_impl(context, date):
    if date == u'1天后':
        context.now_date = datetime.now()
        delta = timedelta(days=1)
        next_date = (context.now_date + delta).strftime('%Y-%m-%d')
    elif date == u'2天后':
        delta = timedelta(days=2)
        next_date = (context.now_date + delta).strftime('%Y-%m-%d')
    os.system("date %s" %(next_date))

@when(u'还原系统时间')
def step_impl(context):
    os.system("date %s" %(context.now_date))