#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings
from weixin.message.material import models as material_models
from apps.customerized_apps.group import models as group_models
import termite.pagestore as pagestore_manager
import json

def __debug_print(content,type_tag=True):
    """
    debug工具函数
    """
    if content:
        print('++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++')
        if type_tag:
            print("====== Type ======")
            print(type(content))
            print("===================")
        print(content)
        print('++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++')
    else:
        pass


# def __get_groupPageJson(args):
#     """
#     传入参数，获取模板
#     """
#     __page_temple = {
#         "type": "appkit.page",
#         "cid": 1,
#         "pid": None,
#         "auto_select": False,
#         "selectable": "yes",
#         "force_display_in_property_view": "no",
#         "has_global_content": "no",
#         "need_server_process_component_data": "no",
#         "is_new_created": True,
#         "property_view_title": "背景",
#         "model": {
#             "id": "",
#             "class": "",
#             "name": "",
#             "index": 1,
#             "datasource": {
#                 "type": "api",
#                 "api_name": ""
#             },
#             "content_padding": "15px",
#             "title": "index",
#             "event:onload": "",
#             "uploadHeight": "568",
#             "uploadWidth": "320",
#             "site_title": "团购",
#             "background": ""
#         },
#         "components": [{
#             "type": "appkit.groupdescription",
#             "cid": 2,
#             "pid": 1,
#             "auto_select": False,
#             "selectable": "yes",
#             "force_display_in_property_view": "no",
#             "has_global_content": "no",
#             "need_server_process_component_data": "no",
#             "property_view_title": "拼手气",
#             "model": {
#                 "id": "",
#                 "class": "",
#                 "name": "",
#                 "index": 2,
#                 "datasource": {
#                     "type": "api",
#                     "api_name": ""
#                 },
#                 "title": args.get("title"),
#                 "start_time": args.get("start_time"),
#                 "end_time": args.get("end_time"),
#                 "valid_time": args.get("valid_time"),
#                 "timing": {
#                     "timing": {
#                         "select": args.get("timing_status")
#                     }
#                 },
#                 "timing_value": {
#                     "day": args.get("timing_value_day",0),
#                     "hour": "00",
#                     "minute": "00",
#                     "second": "00"
#                 },
#                 "random_total_money": args.get("group_random_total_money"),
#                 "random_packets_number": args.get("group_random_packets_number"),
#                 "regular_packets_number": args.get("group_regular_packets_number"),
#                 "regular_per_money": args.get("group_regular_per_money"),
#                 "group_type":args.get("group_type"),
#                 "start_money": args.get("start_money"),
#                 "end_money": args.get("end_money"),
#                 "money_range": args.get("money_range"),
#                 "reply_content": args.get("reply_content"),
#                 "qrcode": args.get("qrcode"),
#                 "wishing": args.get("wishing"),
#                 "rules": args.get("rules"),
#                 "material_image": args.get("material_image"),
#                 "share_description": args.get("share_description")
#             },
#             "components": []
#         }, {
#             "type": "appkit.submitbutton",
#             "cid": 3,
#             "pid": 1,
#             "auto_select": False,
#             "selectable": "no",
#             "force_display_in_property_view": "no",
#             "has_global_content": "no",
#             "need_server_process_component_data": "no",
#             "property_view_title": "",
#             "model": {
#                 "id": "",
#                 "class": "",
#                 "name": "",
#                 "index": 99999,
#                 "datasource": {
#                     "type": "api",
#                     "api_name": ""
#                 },
#                 "text": "提交"
#             },
#             "components": []
#         }, {
#             "type": "appkit.componentadder",
#             "cid": 4,
#             "pid": 1,
#             "auto_select": False,
#             "selectable": "yes",
#             "force_display_in_property_view": "no",
#             "has_global_content": "no",
#             "need_server_process_component_data": "no",
#             "property_view_title": "添加模块",
#             "model": {
#                 "id": "",
#                 "class": "",
#                 "name": "",
#                 "index": 3,
#                 "datasource": {
#                     "type": "api",
#                     "api_name": ""
#                 },
#                 "components": ""
#             },
#             "components": []
#         }]
#     }

#     return json.dumps(__page_temple)

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

# def __date_delta(start,end):
#     """
#     获得日期，相差天数，返回int
#     格式：
#         start:(str){2015-11-23}
#         end :(str){2015-11-30}
#     """
#     start = dt.datetime.strptime(start, "%Y-%m-%d").date()
#     end = dt.datetime.strptime(end, "%Y-%m-%d").date()
#     return (end-start).days

# def __date2time(date_str):
#     """
#     字符串 今天/明天……
#     转化为字符串 "%Y-%m-%d %H:%M"
#     """
#     cr_date = date_str
#     p_date = bdd_util.get_date_str(cr_date)
#     p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
#     return p_time

# def __datetime2str(dt_time):
#     """
#     datetime型数据，转为字符串型，日期
#     转化为字符串 "%Y-%m-%d %H:%M"
#     """
#     dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
#     return dt_time

# def __group_name2id(name):
#     """
#     给团购项目的名字，返回id元祖
#     返回（related_page_id,group_group中id）
#     """
#     obj = group_models.Group.objects.get(name=name)
#     return (obj.related_page_id,obj.id)

# def __status2name(status_num):
#     """
#     团购：状态值 转 文字
#     """
#     status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
#     return status2name_dic[status_num]

# def __name2status(name):
#     """
#     团购： 文字 转 状态值
#     """
#     if name:
#         name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
#         return name2status_dic[name]
#     else:
#         return -1

# def __name2color(name):
#   """
#   团购背景色：文字 转 状态值
#   """
#   name2color_dic = {
#       u"冬日暖阳":"yellow",
#       u"玫瑰茜红":"red",
#       u"热带橙色":"orange"
#   }
#   return name2color_dic[name]

# def __color2name(color):
#   """
#   团购背景色：状态值 转 文字
#   """
#   color2name_dic = {
#       'yellow': u'冬日暖阳',
#       'red': u'玫瑰茜红',
#       'orange': u'热带橙色'
#   }
#   return color2name_dic[color]


# def __get_qrcode(context,qrcode_name):
#   """
#   传入二维码名字，获得二维码，信息字典
#   """

#   qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
#   qrcode_i_url = '/new_weixin/qrcode/?setting_id=%s' % str(qrcode_id)
#   qrcode_response = context.client.get(qrcode_i_url)
#   qrcode_info = qrcode_response.context['qrcode']
#   qrcode_ticket_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qrcode_info.ticket)
#   qrcode = {"ticket":qrcode_ticket_url,"name":qrcode_info.name}
#   return qrcode

def __get_actions(status):
    """
    根据输入团购状态
    返回对于操作列表
    """
    actions_list = [u"查看",u"预览",u"复制链接"]
    if status == u"已结束":
        actions_list.append(u"删除")
    # elif status=="进行中" or "未开始":
    #   actions_list.append(u"关闭")
    return actions_list

def __Create_Group(context,text,user):
    """
    模拟用户登录页面
    创建团购项目
    写入mongo表：
        1.group_group表
        2.page表
    """

    design_mode = 0
    version = 1
    text = text

    title = text.get("name","")

    cr_start_date = text.get('start_date', u'今天')
    start_date = bdd_util.get_date_str(cr_start_date)
    start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

    cr_end_date = text.get('end_date', u'1天后')
    end_date = bdd_util.get_date_str(cr_end_date)
    end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

    valid_time = "%s~%s"%(start_time,end_time)

    timing_status = text.get("is_show_countdown","")
    timing_value_day = __date_delta(start_date,end_date)

    group_arr = text.get("group","")#红包类型
    group_type = group_arr.get('group_type',""),
    group_random_total_money = group_arr.get('random_total_money',""),
    group_random_packets_number = group_arr.get("random_packets_number",""),
    group_regular_packets_number = group_arr.get("regular_packets_number",""),
    group_regular_per_money = group_arr.get("regular_per_money",""),

    contribution_start_range = text.get("contribution_start_range",0)
    contribution_end_range = text.get("contribution_end_range",0)
    money_range = "{}-{}".format(contribution_start_range,contribution_end_range)

    reply_content = text.get("reply","")


    wishing = text.get("open_packet_reply","")
    rules = text.get("rules","")
    material_image = text.get("share_pic","")
    share_description = text.get("share_desc","")



    page_args = {
        "title":title,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "timing_status":timing_status,
        "timing_value_day":timing_value_day,
        "group_type":group_type,
        "group_random_total_money":group_random_total_money,
        "group_random_packets_number":group_random_packets_number,
        "group_regular_packets_number":group_regular_packets_number,
        "group_regular_per_money":group_regular_per_money,
        "start_money":contribution_start_range,
        "end_money":contribution_end_range,
        "money_range":money_range,
        "reply_content":reply_content,
        "qrcode":qrcode,
        "wishing":wishing,
        "rules":rules,
        "material_image":material_image,
        "share_description":share_description,
    }

    #step1：登录页面，获得分配的project_id
    get_pw_response = context.client.get("/apps/group/group/")
    pw_args_response = get_pw_response.context
    project_id = pw_args_response['project_id']#(str){new_app:group:0}

    #step2: 编辑页面获得右边的page_json
    dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    dynamic_response = context.client.get(dynamic_url)
    dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

    #step3:发送Page
    page_json = __get_groupPageJson(page_args)

    termite_post_args = {
        "field":"page_content",
        "id":project_id,
        "page_id":"1",
        "page_json": page_json
    }
    termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    post_termite_response = context.client.post(termite_url,termite_post_args)
    related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

    #step4:发送group_args
    post_group_args = {
        "name":title,
        "start_time":start_time,
        "end_time":end_time,
        "timing":timing_status,
        "group_type":group_type,
        "random_total_money":group_random_total_money,
        "random_packets_number":group_random_packets_number,
        "regular_packets_number":group_regular_packets_number,
        "regular_per_money":group_regular_per_money,
        "money_range":money_range,
        "reply_content":reply_content,
        "material_image":material_image,
        "qrcode":json.dumps(qrcode),
        "wishing":wishing,
        "related_page_id":related_page_id
    }
    group_url ="/apps/group/api/group/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
    post_group_response = context.client.post(group_url,post_group_args)

# def __Update_Group(context,text,page_id,group_id):
#     """
#     模拟用户登录页面
#     编辑团购项目
#     写入mongo表：
#         1.group_group表
#         2.page表
#     """

#     design_mode=0
#     version=1
#     project_id = "new_app:group:"+page_id

#     title = text.get("name","")

#     cr_start_date = text.get('start_date', u'今天')
#     start_date = bdd_util.get_date_str(cr_start_date)
#     start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

#     cr_end_date = text.get('end_date', u'1天后')
#     end_date = bdd_util.get_date_str(cr_end_date)
#     end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

#     valid_time = "%s~%s"%(start_time,end_time)

#     timing_status = text.get("is_show_countdown","")
#     timing_value_day = __date_delta(start_date,end_date)

#     group_arr = text.get("group","")#红包类型
#     group_type = group_arr.get('group_type',""),
#     group_random_total_money = group_arr.get('random_total_money',""),
#     group_random_packets_number = group_arr.get("random_packets_number",""),
#     group_regular_packets_number = group_arr.get("regular_packets_number",""),
#     group_regular_per_money = group_arr.get("regular_per_money",""),

#     contribution_start_range = text.get("contribution_start_range",0)
#     contribution_end_range = text.get("contribution_end_range",0)
#     money_range = "{}-{}".format(contribution_start_range,contribution_end_range)

#     reply_content = text.get("reply","")

#     qrcode_name = text.get("qr_code","")
#     if qrcode_name:
#         qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
#         qrcode_i_url = '/new_weixin/qrcode/?setting_id=%s' % str(qrcode_id)
#         qrcode_response = context.client.get(qrcode_i_url)
#         qrcode_info = qrcode_response.context['qrcode']
#         qrcode_ticket_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qrcode_info.ticket)
#         qrcode = {"ticket":qrcode_ticket_url,"name":qrcode_info.name}
#     else:
#         qrcode = {"ticket":"","name":""}

#     wishing = text.get("open_packet_reply","")
#     rules = text.get("rules","")
#     material_image = text.get("share_pic","")
#     share_description = text.get("share_desc","")

#     page_args = {
#         "title":title,
#         "start_time":start_time,
#         "end_time":end_time,
#         "valid_time":valid_time,
#         "timing_status":timing_status,
#         "timing_value_day":timing_value_day,
#         "group_type":group_type,
#         "group_random_total_money":group_random_total_money,
#         "group_random_packets_number":group_random_packets_number,
#         "group_regular_packets_number":group_regular_packets_number,
#         "group_regular_per_money":group_regular_per_money,
#         "start_money":contribution_start_range,
#         "end_money":contribution_end_range,
#         "money_range":money_range,
#         "reply_content":reply_content,
#         "qrcode":qrcode,
#         "wishing":wishing,
#         "rules":rules,
#         "material_image":material_image,
#         "share_description":share_description,
#     }

#     page_json = __get_groupPageJson(page_args)

#     update_page_args = {
#         "field":"page_content",
#         "id":project_id,
#         "page_id":"1",
#         "page_json": page_json
#     }

#     update_group_args = {
#         "name":title,
#         "start_time":start_time,
#         "end_time":end_time,
#         "timing":timing_status,
#         "group_type":group_type,
#         "random_total_money":group_random_total_money,
#         "random_packets_number":group_random_packets_number,
#         "regular_packets_number":group_regular_packets_number,
#         "regular_per_money":group_regular_per_money,
#         "money_range":money_range,
#         "reply_content":reply_content,
#         "material_image":material_image,
#         "qrcode":json.dumps(qrcode),
#         "wishing":wishing,
#         "id":group_id#updated的差别
#     }


#     #page 更新Page
#     update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
#     update_page_response = context.client.post(update_page_url,update_page_args)

#     #step4:更新Group
#     update_group_url ="/apps/group/api/group/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
#     update_group_response = context.client.post(update_group_url,update_group_args)

# def __Delete_Group(context,group_id):
#     """
#     删除团购活动
#     写入mongo表：
#         1.group_group表

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

# def __Stop_Group(context,group_id):
#   """
#   关闭团购活动
#   """

#   design_mode = 0
#   version = 1
#   stop_group_url = "/apps/group/api/group_status/?design_mode={}&version={}".format(design_mode,version)
#   stop_args ={
#       "id":group_id,
#       "target":'stoped'
#   }
#   stop_group_response = context.client.post(stop_group_url,stop_args)
#   return stop_group_response

# def __Search_Powerme(context,search_dic):
#     """
#     搜索团购活动

#     输入搜索字典
#     返回数据列表
#     """

#     design_mode = 0
#     version = 1
#     page = 1
#     enable_paginate = 1
#     count_per_page = 10

#     name = search_dic["name"]
#     start_time = search_dic["start_time"]
#     end_time = search_dic["end_time"]
#     status = __name2status(search_dic["status"])



#     search_url = "/apps/group/api/groups/?design_mode={}&version={}&name={}&status={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
#             design_mode,
#             version,
#             name,
#             status,
#             start_time,
#             end_time,
#             count_per_page,
#             page,
#             enable_paginate)

#     search_response = context.client.get(search_url)
#     bdd_util.assert_api_call_success(search_response)
#     return search_response

# def __Search_Powerme_Result(context,search_dic):
#   """
#   搜索,团购参与结果

#   输入搜索字典
#   返回数据列表
#   """

#   design_mode = 0
#   version = 1
#   page = 1
#   enable_paginate = 1
#   count_per_page = 10

#   id = search_dic["id"]
#   participant_name = search_dic["participant_name"]
#   start_time = search_dic["start_time"]
#   end_time = search_dic["end_time"]



#   search_url = "/apps/group/api/group_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
#           design_mode,
#           version,
#           id,
#           participant_name,
#           start_time,
#           end_time,
#           count_per_page,
#           page,
#           enable_paginate)

#   search_response = context.client.get(search_url)
#   bdd_util.assert_api_call_success(search_response)
#   return search_response


@when(u'{user}新建团购活动时设置参与活动的商品查询条件')
def step_impl(context,user):
    text_list = json.loads(context.text)
    search_name = text_list['name']
    rec_product_url ="/mall2/api/group_product_list/?design_mode=0&project_id=new_app:group:0&version=1&name=&count_per_page=5&page=1&enable_paginate=1"
    rec_product_response = context.client.get(rec_product_url)
    rec_product_list = json.loads(rec_product_response.content)['data']['items']#[::-1]
    context.rec_product_list = rec_product_list

@then(u'{user}获得团购活动可以访问的已上架商品列表')
def step_impl(context,user):
    expected = []
    if context.table:
        for row in context.table:
            cur_p = row.as_dict()
            expected.append(cur_p)

    actual = []
    if context.rec_product_list:
        for product in context.rec_product_list:
            tmp_product = OrderedDict()
            tmp_product['name'] = product['name']
            tmp_product['price'] = product['display_price']
            tmp_product['stocks'] = product['stocks']
            tmp_product['have_promotion'] = ""
            tmp_product['actions'] = u"选取"
            actual.append(tmp_product)

    print("expected: {}".format(expected))
    print("actual_data: {}".format(actual))
    bdd_util.assert_list(expected, actual)


@when(u'{user}新建团购活动')
def create_Group(context,user):
    text_list = json.loads(context.text)
    for text in text_list:
        __Create_Group(context,text,user)

# @when(u'{user}新建普通红包活动')
# def step_impl(context,user):
#     create_Group(context,user)

# @then(u'{user}获得团购活动列表')
# def step_impl(context,user):
#     design_mode = 0
#     count_per_page = 10
#     version = 1
#     page = 1
#     enable_paginate = 1

#     actual_list = []
#     expected = json.loads(context.text)

#     #搜索查看结果
#     if hasattr(context,"search_group"):
#         rec_search_list = context.search_group
#         for item in rec_search_list:
#             tmp = {
#                 "name":item['name'],
#                 "participant_count":item['participant_count'],
#                 "group_type":item['group_type'],
#                 "status":item['status'],
#                 "total_money":item['total_money'],
#                 "already_paid_money":item['already_paid_money'],
#                 "start_time":__date2time(item['start_time']),
#                 "end_time":__date2time(item['end_time']),
#             }
#             tmp["actions"] = __get_actions(item['status'])
#             actual_list.append(tmp)

#         for expect in expected:
#             if 'start_date' in expect:
#                 expect['start_time'] = __date2time(expect['start_date'])
#                 del expect['start_date']
#             if 'end_date' in expect:
#                 expect['end_time'] = __date2time(expect['end_date'])
#                 del expect['end_date']
#         print("expected: {}".format(expected))

#         bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
#     #其他查看结果
#     else:
#         #分页情况，更新分页参数
#         if hasattr(context,"paging"):
#             paging_dic = context.paging
#             count_per_page = paging_dic['count_per_page']
#             page = paging_dic['page_num']

#         for expect in expected:
#             if 'start_date' in expect:
#                 expect['start_time'] = __date2time(expect['start_date'])
#                 del expect['start_date']
#             if 'end_date' in expect:
#                 expect['end_time'] = __date2time(expect['end_date'])
#                 del expect['end_date']


#         print("expected: {}".format(expected))

#         rec_group_url ="/apps/group/api/groups/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
#         rec_group_response = context.client.get(rec_group_url)
#         rec_group_list = json.loads(rec_group_response.content)['data']['items']#[::-1]

#         for item in rec_group_list:
#             tmp = {
#                 "name":item['name'],
#                 "participant_count":item['participant_count'],
#                 "group_type":item['group_type'],
#                 "status":item['status'],
#                 "total_money":item['total_money'],
#                 "already_paid_money":item['already_paid_money'],
#                 "start_time":__date2time(item['start_time']),
#                 "end_time":__date2time(item['end_time']),
#             }
#             tmp["actions"] = __get_actions(item['status'])
#             actual_list.append(tmp)
#         print("actual_data: {}".format(actual_list))
#         bdd_util.assert_list(expected,actual_list)


# @when(u"{user}编辑团购活动'{group_name}'")
# def step_impl(context,user,group_name):
#     expect = json.loads(context.text)[0]
#     group_page_id,group_id = __group_name2id(group_name)#纯数字
#     __Update_Group(context,expect,group_page_id,group_id)



# @when(u"{user}删除团购活动'{group_name}'")
# def step_impl(context,user,group_name):
#     group_page_id,group_id = __group_name2id(group_name)#纯数字
#     del_response = __Delete_Group(context,group_id)
#     bdd_util.assert_api_call_success(del_response)


# @when(u"{user}关闭团购活动'{group_name}'")
# def step_impl(context,user,group_name):
#   group_page_id,group_id = __group_name2id(group_name)#纯数字
#   stop_response = __Stop_Group(context,group_id)
#   bdd_util.assert_api_call_success(stop_response)


# @when(u"{user}查看团购活动'{group_name}'")
# def step_impl(context,user,group_name):
#   group_page_id,group_id = __group_name2id(group_name)#纯数字
#   url ='/apps/group/api/group_participances/?_method=get&id=%s' % (group_id)
#   url = bdd_util.nginx(url)
#   response = context.client.get(url)
#   context.participances = json.loads(response.content)
#   context.group_id = "%s"%(group_id)

# @then(u"{webapp_user_name}获得团购活动'{power_me_rule_name}'的结果列表")
# def step_tmpl(context, webapp_user_name, power_me_rule_name):
#   if hasattr(context,"search_group_result"):
#       participances = context.search_group_result
#   else:
#       participances = context.participances['data']['items']
#   actual = []
#   print(participances)
#   for p in participances:
#       p_dict = OrderedDict()
#       p_dict[u"rank"] = p['ranking']
#       p_dict[u"member_name"] = p['username']
#       p_dict[u"group_value"] = p['power']
#       p_dict[u"parti_time"] = bdd_util.get_date_str(p['created_at'])
#       actual.append((p_dict))
#   print("actual_data: {}".format(actual))
#   expected = []
#   if context.table:
#       for row in context.table:
#           cur_p = row.as_dict()
#           if cur_p[u'parti_time']:
#               cur_p[u'parti_time'] = bdd_util.get_date_str(cur_p[u'parti_time'])
#           expected.append(cur_p)
#   else:
#       expected = json.loads(context.text)
#   print("expected: {}".format(expected))

#   bdd_util.assert_list(expected, actual)

# @when(u"{user}设置团购活动列表查询条件")
# def step_impl(context,user):
#     expect = json.loads(context.text)
#     if 'start_date' in expect:
#         expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
#         del expect['start_date']

#     if 'end_date' in expect:
#         expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
#         del expect['end_date']

#     search_dic = {
#         "name": expect.get("name",""),
#         "start_time": expect.get("start_time",""),
#         "end_time": expect.get("end_time",""),
#         "status": expect.get("status",u"全部")
#     }
#     search_response = __Search_Powerme(context,search_dic)
#     group_array = json.loads(search_response.content)['data']['items']
#     context.search_group = group_array

# @when(u"{user}访问团购活动列表第'{page_num}'页")
# def step_impl(context,user,page_num):
#     count_per_page = context.count_per_page
#     context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}访问团购活动列表下一页")
# def step_impl(context,user):
#     paging_dic = context.paging
#     count_per_page = paging_dic['count_per_page']
#     page_num = int(paging_dic['page_num'])+1
#     context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}访问团购活动列表上一页")
# def step_impl(context,user):
#     paging_dic = context.paging
#     count_per_page = paging_dic['count_per_page']
#     page_num = int(paging_dic['page_num'])-1
#     context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}设置团购活动结果列表查询条件")
# def step_impl(context,user):
#   expect = json.loads(context.text)

#   if 'parti_start_time' in expect:
#       expect['start_time'] = __date2time(expect['parti_start_time']) if expect['parti_start_time'] else ""
#       del expect['parti_start_time']

#   if 'parti_end_time' in expect:
#       expect['end_time'] = __date2time(expect['parti_end_time']) if expect['parti_end_time'] else ""
#       del expect['parti_end_time']

#   id = context.group_id
#   participant_name = expect.get("member_name","")
#   start_time = expect.get("start_time","")
#   end_time = expect.get("end_time","")

#   search_dic = {
#       "id":id,
#       "participant_name":participant_name,
#       "start_time":start_time,
#       "end_time":end_time
#   }
#   search_response = __Search_Powerme_Result(context,search_dic)
#   group_result_array = json.loads(search_response.content)['data']['items']
#   context.search_group_result = group_result_array

# @then(u"{user}能批量导出团购活动'{group_name}'")
# def step_impl(context,user,group_name):
#   group_page_id,group_id = __group_name2id(group_name)#纯数字
#   url ='/apps/group/api/group_participances_export/?_method=get&export_id=%s' % (group_id)
#   url = bdd_util.nginx(url)
#   response = context.client.get(url)
#   bdd_util.assert_api_call_success(response)