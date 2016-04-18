#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24 aix'

from behave import *
from test import bdd_util
from collections import OrderedDict

from django.contrib.auth.models import User
from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from mall.models import WxCertSettings
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings
from weixin.message.material import models as material_models
from apps.customerized_apps.shvote import models as shvote_models
import termite.pagestore as pagestore_manager
import json
import copy
import apps_step_utils as apps_util

def __shvote_name2id(name, title=None):
    """
    给高级投票项目的名字，返回id元祖
    返回（related_page_id,group_group中id）
    """
    if title:
        name = material_models.News.objects.get(title=title).url
    shvote = shvote_models.Shvote.objects.get(name=name)
    return shvote.related_page_id,shvote.id

def __name2status(name):
    """
    高级投票： 文字 转 状态值
    """
    if name:
        name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
        return name2status_dic[name]
    else:
        return -1

@When(u"{webapp_user_name}点击图文'{title}'进入高级微信投票活动页面")
def step_impl(context, webapp_user_name, title):
    user = User.objects.get(id=context.webapp_owner_id)
    openid = "%s_%s" % (webapp_user_name, user.username)
    _, record_id = __shvote_name2id('', title)
    context.shvote_id = str(record_id)
    context.openid = openid

    #获取页面
    view_mobile_main_page(context)


def view_mobile_main_page(context):
    """
    进入活动主页
    @param context:
    @return:
    """
    return apps_util.get_response(context, {
        "app": "m/apps/shvote",
        "resource": "m_shvote",
        "method": "get",
        "type": "get",
        "args": {
            "webapp_owner_id": context.webapp_owner_id,
            "id": context.shvote_id
        }
    })

def get_dynamic_data(context):
    return apps_util.get_response(context, {
        "app": "m/apps/shvote",
        "resource": "m_shvote",
        "type": "api",
        "method": "get",
        "args": {
            "webapp_owner_id": context.webapp_owner_id,
            "recordId": context.shvote_id
        }
    })

@then(u"{webapp_user_name}获得微信高级投票活动主页的内容")
def step_impl(context, webapp_user_name):
    #获取动态数据
    response = get_dynamic_data(context)

    expected_data = json.loads(context.text)
    result_data = json.loads(response.content)['data']['record_info']
    expected_data['end_date'] = bdd_util.get_date_str(expected_data['end_date'])

    actual_data = {
        "total_participanted_count": 0,
        "total_voted_count": 0,
        "total_visits": 0,
        "end_date": ""
    }

    for k, v in result_data.items():
        if k == "total_parted":
            actual_data["total_participanted_count"] = v
        if k == "total_counts":
            actual_data["total_voted_count"] = v
        if k == "total_visits":
            actual_data["total_visits"] = v
        if k == "end_date":
            actual_data["end_date"] = v

    bdd_util.assert_dict(expected_data,actual_data)

@Then(u"{webapp_user_name}获得微信高级投票活动主页排行榜'{group}'列表")
def step_impl(context, webapp_user_name, group):
    #获取动态数据
    get_dynamic_data(context)
    response = __get_rank_data(context, group)
    expected_data = json.loads(context.text)

    result_data = json.loads(response.content)['data']['result_list']
    expected_keys = actual_data = []

    if len(expected_data) > 0:
        expected_keys = expected_data[0].keys()

    for data in result_data:
        expected_keys = expected_keys if expected_keys else data.keys()
        tmp_dict = {}
        for k, v in data.items():
            if k in expected_keys:
                tmp_dict[k] = v
        actual_data.append(tmp_dict)
    apps_util.debug_print(expected_data)
    apps_util.debug_print(actual_data)
    bdd_util.assert_list(expected_data,actual_data)

@Then(u"{webapp_user_name}获得微信高级投票活动单独页面排行榜'{group}'列表")
def step_impl(context, webapp_user_name, group):
    #获取页面
    apps_util.get_response(context, {
        "app": "m/apps/shvote",
        "resource": "m_shvote_rank",
        "method": "get",
        "args": {
            "webapp_owner_id": context.webapp_owner_id,
            "id": context.shvote_id
        }
    })

    #获取排行数据
    response = __get_rank_data(context, group)
    expected_data = json.loads(context.text)

    result_data = json.loads(response.content)['data']['result_list']
    expected_keys = actual_data = []

    if len(expected_data) > 0:
        expected_keys = expected_data[0].keys()

    for data in result_data:
        expected_keys = expected_keys if expected_keys else data.keys()
        tmp_dict = {}
        for k, v in data.items():
            if k in expected_keys:
                tmp_dict[k] = v
        actual_data.append(tmp_dict)
    apps_util.debug_print(expected_data)
    apps_util.debug_print(actual_data)
    bdd_util.assert_list(expected_data,actual_data)

def __get_rank_data(context, group, search=""):
        return apps_util.get_response(context, {
            "app": "m/apps/shvote",
            "resource": "m_shvote_rank",
            "method": "get",
            "type": "api",
            "args": {
                "webapp_owner_id": context.webapp_owner_id,
                "recordId": context.shvote_id,
                "current_group": group,
                "search_name": search
            }
        })