#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

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

def debug_print(content,type_tag=True):
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

def bool2Bool(bo):
    """
    JS字符串布尔值转化为Python布尔值
    """
    bool_dic = {'true':True,'false':False,'True':True,'False':False}
    if bo:
        result = bool_dic[bo]
    else:
        result = None
    return result

def date_delta(start,end):
    """
    获得日期，相差天数，返回int
    格式：
        start:(str){2015-11-23}
        end :(str){2015-11-30}
    """
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()
    return (end-start).days

def date2time(date_str):
    """
    字符串 今天/明天……
    转化为字符串 "%Y-%m-%d %H:%M"
    """
    cr_date = date_str
    p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
    return p_time

def datetime2str(dt_time):
    """
    datetime型数据，转为字符串型，日期
    转化为字符串 "%Y-%m-%d %H:%M"
    """
    dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
    return dt_time

def app_name2id(model, name, title=None):
    """
    model: 如Vote, PowerMe 这些model class
    name: 活动名称
    title: 图文链接的名称
    返回（related_page_id,group_group中id）
    """
    if title:
        name = material_models.News.objects.get(title=title).url
    obj = model.objects.get(name=name)
    return (obj.related_page_id,obj.id)

def get_app_by_name(model, record_name):
    """
    通过活动名称获取活动记录
    @param model: apps的model class
    @param record_name: 活动名称
    @return: app model实例
    """
    try:
        app = model.objects.filter(name=record_name)
    except:
        return None
    if app.count() <= 0:
        return None
    return app.first()

def get_openid(webapp_user_name, username):
    """
    通过微信端用户名和pc端用户名获取openid
    @param webapp_user_name: 微信端用户名
    @param username: pc端用户名
    @return:
    """
    return '%s_%s' % (webapp_user_name, username)

def name2status(name):
    """
    高级投票： 文字 转 状态值
    """
    if name:
        name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
        return name2status_dic[name]
    else:
        return -1

def get_actions(status, exist=[]):
    """
    根据状态 status
    exist: 固定的操作列表
    返回对于操作列表
    """
    actions_list = []
    if status in [u"已结束", u"未开始"]:
        actions_list.append(u"删除")
    elif status==u"进行中":
        actions_list.append(u"关闭")
    actions_list.extend(exist)
    return actions_list


def username2user(webapp_user_name):
    return User.objects.get(username=webapp_user_name)

def get_response(context, options, param=None):
    """
    apps的api请求可能出现302
    @param context
    @param options {
                "app": 'm/apps/shvote',
                "resource": "get_rank_list",
                "method": "get",
                "args": {
                    "webapp_owner_id": 2,
                    "recordId": "asfas123adsfcagf"
                }
                "type": "api" 代表是api请求还是普通get请求
            }
    @return:
    """
    def __call(method, url, param):
        response = __get_response(method, url, param)
        req_count = 0
        context.link_url = url
        while response.status_code == 302:
            req_count += 1
            redirect_url = response['Location']
            context.last_url = redirect_url
            param = param if method == 'post' else {}
            debug_print("method====="+method+"redirect_url======"+redirect_url)
            debug_print(param)
            response = __get_response(method, redirect_url, param)
            if req_count >= 5:
                break
        return response
    def __get_response(method, url, param):
        if method == "get":
            return context.client.get(url)
        else:
            return context.client.post(url, param)

    if isinstance(options, (str, unicode)):
        param = param if param else {}
        url = options
        return __call("get", url, param)

    type = options.get("type", "get")

    type_str = "/api/" if type == "api" else "/"

    param = options.get("args", {})

    app = options.get("app","")
    resource = options.get("resource", "")

    _method = "" if options.get("method", "get") == "get" and not type == "api" else "_method={}&".format(options.get("method"))
    pc_method = "" if options.get("method", "get") == "get" and not type == "api" else "?_method={}".format(options.get("method"))
    #区分手机端请求和pc端请求
    if app.startswith("m"):
        url = "/{}{}{}/?{}opid={}&fmt={}".format(app, type_str, resource, _method, context.openid, context.member.token)
    else:
        url = "/{}{}{}/{}".format(app, type_str, resource, pc_method)
    method = "post" if options.get("method", "get") in ["post", "put", "delete"] else "get"
    if method == "get":
        for k, v in param.items():
            url = "{}&{}={}".format(url, k, v)
    debug_print("url==== "+url)
    return __call(method, url, param)