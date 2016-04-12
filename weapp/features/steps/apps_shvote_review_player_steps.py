#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

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


def __get_shvotePageJson(args):
    """
    传入参数，获取模板
    """
    __page_temple = {}
    __shvote_temple = {}


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
        "site_title": "团购活动",
        "background": ""
    },
    "components": [
        {
            "type": "appkit.shvotedescription",
            "cid": 2,
            "pid": 1,
            "auto_select": False,
            "selectable": "yes",
            "force_display_in_property_view": "no",
            "has_global_content": "no",
            "need_server_process_component_data": "no",
            "property_view_title": "团购活动",
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
                "start_time":  args.get("start_time"),
                "end_time": args.get("end_time"),
                "valid_time": args.get("valid_time"),
                "product": {
                    "productId": args.get('product_id'),
                    "productImg": args.get('product_img'),
                    "productName": args.get('product_name'),
                    "productPrice": float(args.get('product_price')),
                    "productSocks": args.get('product_socks'),
                    "productUsercode": args.get('product_usercode')
                },
                "shvote_title": "",
                "shvote_items": [],
                "rule_title": "",
                "rules": args.get('rules'),
                "material_image": args.get('material_image'),
                "share_description": args.get('share_description'),
                "timing_value": {
                    "day": "null",
                    "hour": "null",
                    "minute": "null",
                    "second": "null"
                }
            },
            "components": []
        },
        {
            "type": "appkit.submitbutton",
            "cid": 3,
            "pid": 1,
            "auto_select": False,
            "selectable": "no",
            "force_display_in_property_view": "no",
            "has_global_content": "no",
            "need_server_process_component_data": "no",
            "property_view_title": "",
            "model": {
                "id": "",
                "class": "",
                "name": "",
                "index": 99999,
                "datasource": {
                    "type": "api",
                    "api_name": ""
                },
                "text": "提交"
            },
            "components": []
        },
        {
            "type": "appkit.componentadder",
            "cid": 4,
            "pid": 1,
            "auto_select": False,
            "selectable": "yes",
            "force_display_in_property_view": "no",
            "has_global_content": "no",
            "need_server_process_component_data": "no",
            "property_view_title": "添加模块",
            "model": {
                "id": "",
                "class": "",
                "name": "",
                "index": 3,
                "datasource": {
                    "type": "api",
                    "api_name": ""
                },
                "components": ""
            },
            "components": []
        }
    ]
    }

    __shvote_temple =  {
                    "type": "appkit.shvoteitem",
                    "cid": '',
                    "pid": 2,
                    "auto_select": False,
                    "selectable": "no",
                    "force_display_in_property_view": "no",
                    "has_global_content": "no",
                    "need_server_process_component_data": "no",
                    "is_new_created": True,
                    "property_view_title": "",
                    "model": {
                        "id": "",
                        "class": "",
                        "name": "",
                        "index": 5,
                        "datasource": {
                            "type": "api",
                            "api_name": ""
                        },
                        "shvote_type": "",
                        "shvote_days": "",
                        "shvote_price": ""
                    },
                    "components": []
                }


    shvote_dict = args.get("shvote_dict",{})
    shvote_components = []
    shvote_items = []
    if shvote_dict:
        if '0' in shvote_dict:
            shvote_d = shvote_dict["0"]
            shvote_tmp = copy.deepcopy(__shvote_temple)
            shvote_tmp["model"]["shvote_type"] = shvote_d["shvote_type"]
            shvote_tmp["model"]["shvote_days"] = shvote_d["shvote_days"]
            shvote_tmp["model"]["shvote_price"] = shvote_d["shvote_price"]
            shvote_tmp['cid'] = 5
            shvote_tmp['model']["index"] = 5
            shvote_components.append(shvote_tmp)
            shvote_items.append(5)
        if '1' in shvote_dict:
            shvote_d = shvote_dict["1"]
            shvote_tmp2 = copy.deepcopy(__shvote_temple)
            shvote_tmp2["model"]["shvote_type"] = shvote_d["shvote_type"]
            shvote_tmp2["model"]["shvote_days"] = shvote_d["shvote_days"]
            shvote_tmp2["model"]["shvote_price"] = shvote_d["shvote_price"]
            shvote_tmp2['cid'] = 6
            shvote_tmp2['model']["index"] = 6
            shvote_components.append(shvote_tmp2)
            shvote_items.append(6)

    __page_temple['components'][0]["model"]["shvote_items"] = shvote_items
    __page_temple['components'][0]["components"]= shvote_components

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
    p_date = bdd_util.get_date_str(cr_date)
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
    给团购项目的名字，返回id元祖
    返回（related_page_id,shvote_shvote中id）
    """
    obj = shvote_models.Shvote.objects.get(name=name)
    return (obj.related_page_id,obj.id)

# def __status2name(status_num):
#     """
#     团购：状态值 转 文字
#     """
#     status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
#     return status2name_dic[status_num]

def __name2status(name):
    """
    团购： 文字 转 状态值
    """
    if name:
        name2status_dic = {u"全部":-1,u"未开启":0,u"进行中":1,u"已结束":2}
        return name2status_dic[name]
    else:
        return -1

def __get_actions(status,handle_status):
    """
    根据输入团购状态
    返回对于操作列表
    """
    actions_list = [u"参团详情"]
    if handle_status==0:
        if status == u"已结束":
            actions_list.append(u"删除")
        elif status == "未开启":
            actions_list.append(u"编辑")
            actions_list.append(u"开启")
        elif status=="进行中":
            actions_list.append(u"结束")
    else:
        if status == u"已结束":
            actions_list.append(u"删除")
        elif status == "未开启":
            actions_list.append(u"编辑")
            actions_list.append(u"结束")
        elif status=="进行中":
            actions_list.append(u"结束")
    return actions_list

def __Create_Shvote(context,text,user):
    """
    模拟用户登录页面
    创建团购项目
    写入mongo表：
        1.shvote_shvote表
        2.page表
    """

    design_mode = 0
    version = 1
    text = text

    name = text.get("shvote_name","")

    cr_start_date = text.get('start_date', u'今天')
    start_date = bdd_util.get_date_str(cr_start_date)
    start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

    cr_end_date = text.get('end_date', u'1天后')
    end_date = bdd_util.get_date_str(cr_end_date)
    end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

    valid_time = "%s~%s"%(start_time,end_time)

    shvote_dict = text.get('shvote_dict','')

    product_name = text.get('product_name',"")
    product_dict = get_product_list(context,product_name)[0]

    product_id = ""
    product_img = ""
    product_name = ""
    product_price = ""
    product_socks = ""
    product_usercode = ""
    if product_dict:
        product_id = product_dict['id']
        product_img = product_dict['thumbnails_url']
        product_name = product_dict['name']
        product_price = product_dict['display_price']
        product_socks = product_dict['stocks']
        product_usercode = product_dict['user_code']

    rules = text.get("rules","")
    material_image = text.get("material_image","")
    share_description = text.get("share_description","")



    page_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "shvote_dict":shvote_dict,
        "product_id":product_id,
        "product_img":product_img,
        "product_name":product_name,
        "product_price":product_price,
        "product_socks":product_socks,
        "product_usercode":product_usercode,
        "rules":rules,
        "material_image":material_image,
        "share_description":share_description
    }

    #step1：登录页面，获得分配的project_id
    print context
    get_pw_response = context.client.get("/apps/shvote/shvote/")
    pw_args_response = get_pw_response.context
    project_id = pw_args_response['project_id']#(str){new_app:shvote:0}

    #step2: 编辑页面获得右边的page_json
    dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    dynamic_response = context.client.get(dynamic_url)
    dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

    #step3:发送Page
    page_json = __get_shvotePageJson(page_args)

    termite_post_args = {
        "field":"page_content",
        "id":project_id,
        "page_id":"1",
        "page_json": page_json
    }
    termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    post_termite_response = context.client.post(termite_url,termite_post_args)
    related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

    # #step4:发送shvote_args

    post_shvote_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "shvote_dict":json.dumps(shvote_dict),
        "product_id":product_id,
        "product_img":product_img,
        "product_name":product_name,
        "product_price":product_price,
        "product_socks":product_socks,
        "product_usercode":product_usercode,
        "rules":rules,
        "material_image":material_image,
        "share_description":share_description,
        "related_page_id":related_page_id
    }
    shvote_url ="/apps/shvote/api/shvote/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
    post_shvote_response = context.client.post(shvote_url,post_shvote_args)

def __Update_Shvote(context,text,page_id,shvote_id):
    """
    模拟用户登录页面
    编辑团购项目
    写入mongo表：
        1.shvote_shvote表
        2.page表
    """

    design_mode=0
    version=1
    project_id = "new_app:shvote:"+page_id

    text = text

    name = text.get("shvote_name","")

    cr_start_date = text.get('start_date', u'今天')
    start_date = bdd_util.get_date_str(cr_start_date)
    start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

    cr_end_date = text.get('end_date', u'1天后')
    end_date = bdd_util.get_date_str(cr_end_date)
    end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

    valid_time = "%s~%s"%(start_time,end_time)

    shvote_dict = text.get('shvote_dict','')

    product_name = text.get('product_name',"")
    product_dict = get_product_list(context,product_name)[0]
    product_id = ""
    product_img = ""
    product_name = ""
    product_price = ""
    product_socks = ""
    product_usercode = ""
    if product_dict:
        product_id = product_dict['id']
        product_img = product_dict['thumbnails_url']
        product_name = product_dict['name']
        product_price = product_dict['display_price']
        product_socks = product_dict['stocks']
        product_usercode = product_dict['user_code']

    rules = text.get("rules","")
    material_image = text.get("material_image","")
    share_description = text.get("share_description","")

    page_args = {
        "name":name,
        "start_time":start_time,
        "end_time":end_time,
        "valid_time":valid_time,
        "shvote_dict":shvote_dict,
        "product_id":product_id,
        "product_img":product_img,
        "product_name":product_name,
        "product_price":product_price,
        "product_socks":product_socks,
        "product_usercode":product_usercode,
        "rules":rules,
        "material_image":material_image,
        "share_description":share_description
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
        "shvote_dict":json.dumps(shvote_dict),
        "product_id":product_id,
        "product_img":product_img,
        "product_name":product_name,
        "product_price":product_price,
        "product_socks":product_socks,
        "product_usercode":product_usercode,
        "rules":rules,
        "material_image":material_image,
        "share_description":share_description,
        "id":shvote_id#updated的差别
    }


    #page 更新Page
    update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    update_page_response = context.client.post(update_page_url,update_page_args)

    #step4:更新Shvote
    update_shvote_url ="/apps/shvote/api/shvote/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
    update_shvote_response = context.client.post(update_shvote_url,update_shvote_args)



def __Open_Shvote(context,shvote_id):
    """
    开启团购活动
    写入mongo表：
        1.shvote_shvote表

    注释：page表在原后台，没有被删除
    """
    design_mode = 0
    version = 1
    open_shvote_url = "/apps/shvote/api/shvote_status/?design_mode={}&version={}".format(design_mode,version)
    open_args ={
        "id":shvote_id,
        "target":"running"

    }
    open_shvote_response = context.client.post(open_shvote_url,open_args)
    return open_shvote_response


def __Delete_Shvote(context,shvote_id):
    """
    删除团购活动
    写入mongo表：
        1.shvote_shvote表

    注释：page表在原后台，没有被删除
    """
    design_mode = 0
    version = 1
    del_shvote_url = "/apps/shvote/api/shvote/?design_mode={}&version={}&_method=delete".format(design_mode,version)
    del_args ={
        "id":shvote_id
    }
    del_shvote_response = context.client.post(del_shvote_url,del_args)
    return del_shvote_response

def __Stop_Shvote(context,shvote_id):
  """
  关闭团购活动
  """

  design_mode = 0
  version = 1
  stop_shvote_url = "/apps/shvote/api/shvote_status/?design_mode={}&version={}".format(design_mode,version)
  stop_args ={
      "id":shvote_id,
      "target":'stoped',
      "is_test": True
  }
  stop_shvote_response = context.client.post(stop_shvote_url,stop_args)
  return stop_shvote_response

def __Search_Shvote(context,search_dic):
    """
    搜索团购活动

    输入搜索字典
    返回数据列表
    """

    design_mode = 0
    version = 1
    page = 1
    enable_paginate = 1
    count_per_page = 10

    shvote_name = unicode(search_dic["shvote_name"])
    product_name = unicode(search_dic["product_name"])
    start_time = search_dic["start_time"]
    end_time = search_dic["end_time"]
    status = __name2status(search_dic["status"])



    search_url = "/apps/shvote/api/shvotes/?design_mode={}&version={}&shvote_name={}&product_name={}&status={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
            design_mode,
            version,
            shvote_name,
            product_name,
            status,
            start_time,
            end_time,
            count_per_page,
            page,
            enable_paginate)

    print 111111111111111111111
    print search_url
    search_response = context.client.get(search_url)
    bdd_util.assert_api_call_success(search_response)
    return search_response

# def __Search_Shvote_Result(context,search_dic):
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



#   search_url = "/apps/shvote/api/shvote_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
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


def get_product_list(context,name=""):
    '''
    获取商品信息
    '''
    name_tag = "&name="
    if name:
        name_tag = "&name={}".format(name)
    rec_product_url ="/mall2/api/shvote_product_list/?project_id=new_app:shvote:0{}&count_per_page=5&page=1&enable_paginate=1".format(name_tag)
    rec_product_response = context.client.get(rec_product_url)
    rec_product_list = json.loads(rec_product_response.content)['data']['items']#[::-1]
    return rec_product_list


@when(u'{user}新建团购活动时设置参与活动的商品查询条件')
def step_impl(context,user):
    text_list = json.loads(context.text)
    search_name = text_list['name']
    rec_product_list = get_product_list(context,search_name)
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
def create_Shvote(context,user):
    text_list = json.loads(context.text)
    for text in text_list:
        __Create_Shvote(context,text,user)

# @when(u'{user}新建普通红包活动')
# def step_impl(context,user):
#     create_Shvote(context,user)

@then(u'{user}获得团购活动列表')#########
def step_impl(context,user):
    design_mode = 0
    count_per_page = 10
    version = 1
    page = 1
    enable_paginate = 1

    actual_list = []
    expected = json.loads(context.text)

#     #搜索查看结果
    if hasattr(context,"search_shvote"):
        pass
        rec_search_list = context.search_shvote
        for item in rec_search_list:
            tmp = {
                "id":item['id'],
                "name":item['name'],
                "product_name":item["product_name"],
                "product_img":item["product_img"],
                "product_id":item["product_id"],
                "status":item['status'],
                "shvote_item_count":item['shvote_item_count'],
                "shvote_visitor_count":item['shvote_visitor_count'],
                "shvote_customer_count":item['shvote_customer_count'],
                "handle_status":item['handle_status'],
                "related_page_id":item['related_page_id'],
                "start_time":"%s %s"%(item['start_time_date'].replace('/','-'),item["start_time_time"]),
                "end_time":"%s %s"%(item['end_time_date'].replace('/','-'),item["end_time_time"]),
                "created_at":item["created_at"]
            }
            tmp["actions"] = __get_actions(item['status'],item['handle_status'])
            actual_list.append(tmp)

        for expect in expected:
            if 'start_date' in expect:
                expect['start_time'] = __date2time(expect['start_date'])
                del expect['start_date']
            if 'end_date' in expect:
                expect['end_time'] = __date2time(expect['end_date'])
                del expect['end_date']
        print("expected: {}".format(expected))

        bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
    #其他查看结果
    else:
        #分页情况，更新分页参数
        if hasattr(context,"paging"):
            pass
            paging_dic = context.paging
            count_per_page = paging_dic['count_per_page']
            page = paging_dic['page_num']

        for expect in expected:
            if 'start_date' in expect:
                expect['start_time'] = __date2time(expect['start_date'])
                del expect['start_date']
            if 'end_date' in expect:
                expect['end_time'] = __date2time(expect['end_date'])
                del expect['end_date']


        print("expected: {}".format(expected))

        rec_shvote_url ="/apps/shvote/api/shvotes/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
        rec_shvote_response = context.client.get(rec_shvote_url)
        rec_shvote_list = json.loads(rec_shvote_response.content)['data']['items']#[::-1]

        for item in rec_shvote_list:
            tmp = {
                "name":item['name'],
                "openshvote_num":item['shvote_item_count'],
                "consumer_num":item['shvote_customer_count'],
                "visitor_num":item['shvote_visitor_count'],
                "status":item['status'],
                "start_time":"%s %s"%(item['start_time_date'].replace('/','-'),item['start_time_time']),
                "end_time":"%s %s"%(item['end_time_date'].replace('/','-'),item['end_time_time']),
            }
            actions_array = __get_actions(item['status'],item['handle_status'])
            tmp["actions"] = actions_array
            actual_list.append(tmp)
        print("actual_data: {}".format(actual_list))
        bdd_util.assert_list(expected,actual_list)






@when(u"{user}编辑团购活动'{shvote_name}'")
def step_impl(context,user,shvote_name):
    expect = json.loads(context.text)[0]
    shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
    __Update_Shvote(context,expect,shvote_page_id,shvote_id)



@when(u"{user}删除团购活动'{shvote_name}'")
def step_impl(context,user,shvote_name):
    shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
    del_response = __Delete_Shvote(context,shvote_id)
    bdd_util.assert_api_call_success(del_response)


@when(u"{user}开启团购活动'{shvote_name}'")
def step_impl(context,user,shvote_name):
    shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
    open_response = __Open_Shvote(context,shvote_id)
    bdd_util.assert_api_call_success(open_response)


@when(u"{user}关闭团购活动'{shvote_name}'")
def step_impl(context,user,shvote_name):
  shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
  stop_response = __Stop_Shvote(context,shvote_id)
  bdd_util.assert_api_call_success(stop_response)


# @when(u"{user}查看团购活动'{shvote_name}'")
# def step_impl(context,user,shvote_name):
#   shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
#   url ='/apps/shvote/api/shvote_participances/?_method=get&id=%s' % (shvote_id)
#   url = bdd_util.nginx(url)
#   response = context.client.get(url)
#   context.participances = json.loads(response.content)
#   context.shvote_id = "%s"%(shvote_id)

# @then(u"{webapp_user_name}获得团购活动'{power_me_rule_name}'的结果列表")
# def step_tmpl(context, webapp_user_name, power_me_rule_name):
#   if hasattr(context,"search_shvote_result"):
#       participances = context.search_shvote_result
#   else:
#       participances = context.participances['data']['items']
#   actual = []
#   print(participances)
#   for p in participances:
#       p_dict = OrderedDict()
#       p_dict[u"rank"] = p['ranking']
#       p_dict[u"member_name"] = p['username']
#       p_dict[u"shvote_value"] = p['power']
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

@when(u"{user}设置团购活动列表查询条件")
def step_impl(context,user):
    expect = json.loads(context.text)
    if 'start_date' in expect:
        expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
        del expect['start_date']

    if 'end_date' in expect:
        expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
        del expect['end_date']

    search_dic = {
        "shvote_name": expect.get("name",""),
        "product_name": expect.get("product_name",""),
        "start_time": expect.get("start_time",""),
        "end_time": expect.get("end_time",""),
        "status": expect.get("status",u"全部")
    }
    search_response = __Search_Shvote(context,search_dic)
    shvote_array = json.loads(search_response.content)['data']['items']
    context.search_shvote = shvote_array

@when(u"{user}访问团购活动列表第'{page_num}'页")
def step_impl(context,user,page_num):
    count_per_page = context.count_per_page
    context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问团购活动列表下一页")
def step_impl(context,user):
    paging_dic = context.paging
    count_per_page = paging_dic['count_per_page']
    page_num = int(paging_dic['page_num'])+1
    context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问团购活动列表上一页")
def step_impl(context,user):
    paging_dic = context.paging
    count_per_page = paging_dic['count_per_page']
    page_num = int(paging_dic['page_num'])-1
    context.paging = {'count_per_page':count_per_page,"page_num":page_num}

def __name2user(username):
    user = User.objects.get(username=username)
    return user
@when(u"{username}添加微信证书")
def step_impl(context,username):
    user = __name2user(username)
    WxCertSettings.objects.create(
        owner = user,
        cert_path ="path/to/cert",
        key_path = "path/to/key"
        )


# @when(u"{user}设置团购活动结果列表查询条件")
# def step_impl(context,user):
#   expect = json.loads(context.text)

#   if 'parti_start_time' in expect:
#       expect['start_time'] = __date2time(expect['parti_start_time']) if expect['parti_start_time'] else ""
#       del expect['parti_start_time']

#   if 'parti_end_time' in expect:
#       expect['end_time'] = __date2time(expect['parti_end_time']) if expect['parti_end_time'] else ""
#       del expect['parti_end_time']

#   id = context.shvote_id
#   participant_name = expect.get("member_name","")
#   start_time = expect.get("start_time","")
#   end_time = expect.get("end_time","")

#   search_dic = {
#       "id":id,
#       "participant_name":participant_name,
#       "start_time":start_time,
#       "end_time":end_time
#   }
#   search_response = __Search_Shvote_Result(context,search_dic)
#   shvote_result_array = json.loads(search_response.content)['data']['items']
#   context.search_shvote_result = shvote_result_array

# @then(u"{user}能批量导出团购活动'{shvote_name}'")
# def step_impl(context,user,shvote_name):
#   shvote_page_id,shvote_id = __shvote_name2id(shvote_name)#纯数字
#   url ='/apps/shvote/api/shvote_participances_export/?_method=get&export_id=%s' % (shvote_id)
#   url = bdd_util.nginx(url)
#   response = context.client.get(url)
#   bdd_util.assert_api_call_success(response)