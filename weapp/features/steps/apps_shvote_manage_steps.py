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


def __get_shvotePageJson(args):
    """
    传入参数，获取模板
    """

    __page_temple = {
        "type": "appkit.page",
        "cid": 1,
        "pid": "null",
        "auto_select": False,
        "selectable": "yes",
        "force_display_in_property_view": "no",
        "has_global_content": "no",
        "need_server_process_component_data": "no",
        "is_new_created": True,
        "property_view_title": "背景",
        "model": {
            "id": "",
            "class": "",
            "name": "",
            "index": 1,
            "datasource": {
                "type": "api",
                "api_name": ""
            },
            "content_padding": "15px",
            "title": "index",
            "event:onload": "",
            "uploadHeight": "568",
            "uploadWidth": "320",
            "site_title": "微信投票",
            "background": ""
        },
        "components": [{
            "type": "appkit.shvotedesc",
            "cid": 2,
            "pid": 1,
            "auto_select": False,
            "selectable": "yes",
            "force_display_in_property_view": "no",
            "has_global_content": "no",
            "need_server_process_component_data": "no",
            "property_view_title": "投票",
            "model": {
                "id": "",
                "class": "",
                "name": "",
                "index": 2,
                "datasource": {
                    "type": "api",
                    "api_name": ""
                },
                "title": args.get('name'),
                "rule": args.get('rule'),
                "start_time":  args.get("start_time"),
                "end_time": args.get("end_time"),
                "valid_time": args.get("valid_time"),
                "groups": args.get('groups'),
                "desc": args.get('desc'),
                "pic": args.get('pic'),
            },
            "components": []
        }]
    }

    return json.dumps(__page_temple)

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

def __shvote_name2id(name):
    """
    给高级投票项目的名字，返回id元祖
    返回（related_page_id,group_group中id）
    """
    obj = shvote_models.Shvote.objects.get(name=name)
    return (obj.related_page_id,obj.id)

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

def __get_actions(status):
    """
    根据输入高级投票状态
    返回对于操作列表
    """
    actions_list = []
    if status in [u"已结束", u"未开始"]:
        actions_list.append(u"删除")
    elif status==u"进行中":
        actions_list.append(u"关闭")
    actions_list.extend([u'链接', u'预览', u'报名详情', u'查看结果'])
    return actions_list

def __Create_Shvote(context,text,user):
    """
    创建高级投票项目
    写入mongo表：
        1.shvote_shvote表
        2.page表
    """

    design_mode = 0
    version = 1
    name = text.get("title","")

    cr_start_date = text.get('start_date', u'今天')
    start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

    cr_end_date = text.get('end_date', u'1天后')
    end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

    valid_time = "%s~%s"%(start_time,end_time)

    groups = text.get('groups',[])

    desc = text.get('desc','')

    rule = text.get("rule","")
    pic = text.get("pic","")

    page_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "groups":groups,
        "rule":rule,
        "desc": desc,
        "pic":pic
    }

    #step2: 编辑页面获得右边的page_json
    dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,context.project_id,version)
    context.client.get(dynamic_url)

    #step3:发送Page
    page_json = __get_shvotePageJson(page_args)

    termite_post_args = {
        "field":"page_content",
        "id":context.project_id,
        "page_id":"1",
        "page_json": page_json
    }
    termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,context.project_id,version)
    post_termite_response = context.client.post(termite_url,termite_post_args)
    related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

    # #step4:发送group_args

    post_shvote_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "groups":json.dumps(groups),
        "rule":rule,
        "desc":desc,
        "related_page_id":related_page_id
    }
    shvote_url ="/apps/shvote/api/shvote/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,context.project_id,version)
    context.client.post(shvote_url,post_shvote_args)

def __Update_Group(context,text,page_id,shvote_id):
    """
    模拟用户登录页面
    编辑高级投票项目
    写入mongo表：
        1.group_group表
        2.page表
    """

    design_mode=0
    version=1
    project_id = "new_app:group:"+page_id

    name = text.get("title","")

    cr_start_date = text.get('start_date', u'今天')
    start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

    cr_end_date = text.get('end_date', u'1天后')
    end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

    valid_time = "%s~%s"%(start_time,end_time)

    groups = text.get('groups',[])

    desc = text.get('desc','')

    rule = text.get("rule","")
    pic = text.get("pic","")

    page_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "groups":groups,
        "rule":rule,
        "desc": desc,
        "pic":pic
    }

    page_json = __get_shvotePageJson(page_args)

    update_page_args = {
        "field":"page_content",
        "id":project_id,
        "page_id":"1",
        "page_json": page_json
    }

    update_shvote_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "groups":json.dumps(groups),
        "rule":rule,
        "desc":desc,
        "id":shvote_id#updated的差别
    }

    #page 更新Page
    update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    context.client.post(update_page_url,update_page_args)

    #更新Shvote
    update_shvote_url ="/apps/shvote/api/shvote/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    context.client.post(update_shvote_url,update_shvote_args)


#
# def __Open_Group(context,group_id):
#     """
#     开启高级投票活动
#     写入mongo表：
#         1.group_group表
#
#     注释：page表在原后台，没有被删除
#     """
#     design_mode = 0
#     version = 1
#     open_group_url = "/apps/group/api/group_status/?design_mode={}&version={}".format(design_mode,version)
#     open_args ={
#         "id":group_id,
#         "target":"running"
#
#     }
#     open_group_response = context.client.post(open_group_url,open_args)
#     return open_group_response
#
#
# def __Delete_Group(context,group_id):
#     """
#     删除高级投票活动
#     写入mongo表：
#         1.group_group表
#
#     注释：page表在原后台，没有被删除
#     """
#     design_mode = 0
#     version = 1
#     del_group_url = "/apps/group/api/group/?design_mode={}&version={}&_method=delete".format(design_mode,version)
#     del_args ={
#         "id":group_id
#     }
#     del_group_response = context.client.post(del_group_url,del_args)
#     return del_group_response
#
# def __Stop_Group(context,group_id):
#   """
#   关闭高级投票活动
#   """
#
#   design_mode = 0
#   version = 1
#   stop_group_url = "/apps/group/api/group_status/?design_mode={}&version={}".format(design_mode,version)
#   stop_args ={
#       "id":group_id,
#       "target":'stoped',
#       "is_test": True
#   }
#   stop_group_response = context.client.post(stop_group_url,stop_args)
#   return stop_group_response
#
# def __Search_Group(context,search_dic):
#     """
#     搜索高级投票活动
#
#     输入搜索字典
#     返回数据列表
#     """
#
#     design_mode = 0
#     version = 1
#     page = 1
#     enable_paginate = 1
#     count_per_page = 10
#
#     group_name = unicode(search_dic["group_name"])
#     product_name = unicode(search_dic["product_name"])
#     start_time = search_dic["start_time"]
#     end_time = search_dic["end_time"]
#     status = __name2status(search_dic["status"])
#
#
#
#     search_url = "/apps/group/api/groups/?design_mode={}&version={}&group_name={}&product_name={}&status={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
#             design_mode,
#             version,
#             group_name,
#             product_name,
#             status,
#             start_time,
#             end_time,
#             count_per_page,
#             page,
#             enable_paginate)
#
#     print 111111111111111111111
#     print search_url
#     search_response = context.client.get(search_url)
#     bdd_util.assert_api_call_success(search_response)
#     return search_response


@when(u'{user}新建微信高级投票活动')
def create_Shvote(context,user):
    text_list = json.loads(context.text)
    #访问页面，获得分配的project_id
    get_pw_response = context.client.get("/apps/shvote/shvote/")
    context.project_id = get_pw_response.context['project_id']#{new_app:group:0}
    for text in text_list:
        __Create_Shvote(context,text,user)

@then(u'{user}获得微信高级投票活动列表')
def step_impl(context,user):
    design_mode = 0
    count_per_page = 10
    version = 1
    page = 1
    enable_paginate = 1

    actual_list = []
    expected = json.loads(context.text)

    #搜索查看结果
    if hasattr(context,"search_group"):
        pass
    #     rec_search_list = context.search_group
    #     for item in rec_search_list:
    #         tmp = {
    #             "id":item['id'],
    #             "name":item['name'],
    #             "product_name":item["product_name"],
    #             "product_img":item["product_img"],
    #             "product_id":item["product_id"],
    #             "status":item['status'],
    #             "group_item_count":item['group_item_count'],
    #             "group_visitor_count":item['group_visitor_count'],
    #             "group_customer_count":item['group_customer_count'],
    #             "handle_status":item['handle_status'],
    #             "related_page_id":item['related_page_id'],
    #             "start_time":"%s %s"%(item['start_time_date'].replace('/','-'),item["start_time_time"]),
    #             "end_time":"%s %s"%(item['end_time_date'].replace('/','-'),item["end_time_time"]),
    #             "created_at":item["created_at"]
    #         }
    #         tmp["actions"] = __get_actions(item['status'],item['handle_status'])
    #         actual_list.append(tmp)
    #
    #     for expect in expected:
    #         if 'start_date' in expect:
    #             expect['start_time'] = __date2time(expect['start_date'])
    #             del expect['start_date']
    #         if 'end_date' in expect:
    #             expect['end_time'] = __date2time(expect['end_date'])
    #             del expect['end_date']
    #     print("expected: {}".format(expected))
    #
    #     bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
    #其他查看结果
    else:
        #分页情况，更新分页参数
        # if hasattr(context,"paging"):
        #     pass
        #     paging_dic = context.paging
        #     count_per_page = paging_dic['count_per_page']
        #     page = paging_dic['page_num']

        for expect in expected:
            if 'start_date' in expect:
                expect['start_time'] = __date2time(expect['start_date'])
                del expect['start_date']
            if 'end_date' in expect:
                expect['end_time'] = __date2time(expect['end_date'])
                del expect['end_date']


        print("expected: {}".format(expected))

        rec_group_url ="/apps/shvote/api/shvotes/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
        rec_group_response = context.client.get(rec_group_url)
        rec_group_list = json.loads(rec_group_response.content)['data']['items']#[::-1]

        for item in rec_group_list:
            tmp = {
                "name":item['name'],
                "total_participanted_count":item['total_participanted_count'],
                "total_voted_count":item['total_voted_count'],
                "status":item['status'],
                "start_time":item['start_time'],
                "end_time":item['end_time'],
            }
            tmp["actions"] = __get_actions(item['status'])
            actual_list.append(tmp)
        bdd_util.assert_list(expected,actual_list)

@when(u"{user}编辑高级投票活动'{shvote_name}'")
def step_impl(context,user,shvote_name):
    expect = json.loads(context.text)
    shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
    __Update_Group(context,expect,shvote_page_id,shvote_id)



# @when(u"{user}删除高级投票活动'{group_name}'")
# def step_impl(context,user,group_name):
#     group_page_id,group_id = __group_name2id(group_name)#纯数字
#     del_response = __Delete_Group(context,group_id)
#     bdd_util.assert_api_call_success(del_response)
#
#
# @when(u"{user}开启高级投票活动'{group_name}'")
# def step_impl(context,user,group_name):
#     group_page_id,group_id = __group_name2id(group_name)#纯数字
#     open_response = __Open_Group(context,group_id)
#     bdd_util.assert_api_call_success(open_response)
#
#
# @when(u"{user}关闭高级投票活动'{group_name}'")
# def step_impl(context,user,group_name):
#   group_page_id,group_id = __group_name2id(group_name)#纯数字
#   stop_response = __Stop_Group(context,group_id)
#   bdd_util.assert_api_call_success(stop_response)
#
# @when(u"{user}设置高级投票活动列表查询条件")
# def step_impl(context,user):
#     expect = json.loads(context.text)
#     if 'start_date' in expect:
#         expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
#         del expect['start_date']
#
#     if 'end_date' in expect:
#         expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
#         del expect['end_date']
#
#     search_dic = {
#         "group_name": expect.get("name",""),
#         "product_name": expect.get("product_name",""),
#         "start_time": expect.get("start_time",""),
#         "end_time": expect.get("end_time",""),
#         "status": expect.get("status",u"全部")
#     }
#     search_response = __Search_Group(context,search_dic)
#     group_array = json.loads(search_response.content)['data']['items']
#     context.search_group = group_array
#
# @when(u"{user}访问高级投票活动列表第'{page_num}'页")
# def step_impl(context,user,page_num):
#     count_per_page = context.count_per_page
#     context.paging = {'count_per_page':count_per_page,"page_num":page_num}
#
# @when(u"{user}访问高级投票活动列表下一页")
# def step_impl(context,user):
#     paging_dic = context.paging
#     count_per_page = paging_dic['count_per_page']
#     page_num = int(paging_dic['page_num'])+1
#     context.paging = {'count_per_page':count_per_page,"page_num":page_num}
#
# @when(u"{user}访问高级投票活动列表上一页")
# def step_impl(context,user):
#     paging_dic = context.paging
#     count_per_page = paging_dic['count_per_page']
#     page_num = int(paging_dic['page_num'])-1
#     context.paging = {'count_per_page':count_per_page,"page_num":page_num}
#
# def __name2user(username):
#     user = User.objects.get(username=username)
#     return user