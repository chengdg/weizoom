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

def __debug_print(content,type_tag=True):
    """
    debug工具函数
    """
    print('++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++')
    if type_tag:
        print("====== Type ======")
        print(type(content))
        print("===================")
    print(content)
    print('++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++')



def __bool2Bool(bo):
    """
    JS字符串布尔值转化为Python布尔值
    """
    bool_dic = {'true':True,'false':False,'True':True,'False':False}
    if bo:
        result = bool_dic[bo]
    else:
        result = None
    return result

def __date_delta(start,end):
    """
    获得日期，相差天数，返回int
    格式：
        start:(str){2015-11-23}
        end :(str){2015-11-30}
    """
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()
    return (end-start).days

def __date2time(date_str):
    """
    字符串 今天/明天……
    转化为字符串 "%Y-%m-%d %H:%M"
    """
    cr_date = date_str
    p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
    return p_time

def __datetime2str(dt_time):
    """
    datetime型数据，转为字符串型，日期
    转化为字符串 "%Y-%m-%d %H:%M"
    """
    dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
    return dt_time

def __shvote_name2id(name, title=None):
    """
    给高级投票项目的名字，返回id元祖
    返回（related_page_id,group_group中id）
    """
    if title:
        name = material_models.News.objects.get(title=title).url
    shvote = shvote_models.Shvote.objects.get(name=name)
    return shvote.related_page_id,shvote.id

# def __status2name(status_num):
#     """
#     高级投票：状态值 转 文字
#     """
#     status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
#     return status2name_dic[status_num]

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
    url = '/m/apps/shvote/m_shvote/?webapp_owner_id=%s&id=%s&fmt=%s&opid=%s' % (context.webapp_owner_id, str(record_id), context.member.token, openid)

    #获取页面
    response = context.client.get(url)
    while response.status_code == 302:
        redirect_url = response['Location']
        response = context.client.get(redirect_url)

@then(u"{webapp_user_name}获得微信高级投票活动'{name}'主页的内容")
def step_impl(context, webapp_user_name, name):
    #获取动态数据
    _, record_id = __shvote_name2id(name)
    dynamic_url = '/m/apps/shvote/api/m_shvote/?_method=get'
    param = {
        "webapp_owner_id": context.webapp_owner_id,
        "recordId": record_id,
        "fmt": context.member.token
    }
    response = context.client.get(dynamic_url, param)
    while response.status_code == 302:
        redirect_url = response['Location']
        response = context.client.get(redirect_url)

    expected_data = json.loads(context.text)
    result_data = json.loads(response.content)['data']['record_info']
    expected_data['end_date'] = bdd_util.get_date_str(expected_data['end_date'])

    actual_data = {k: v for k, v in result_data.items() if k in expected_data.keys()}

    bdd_util.assert_dict(expected_data,actual_data)
