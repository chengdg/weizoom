#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

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
import json

##  验证请求200

# def __assert_call_success(response):
#     """
#     验证请求调用成功
#     """
#     content = response.content
#     assert 200 == content['code'], "code != 200, call api FAILED!!!!"
#     return content

def __debug_print(content,type_tag=True):
    print '++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++'
    if type_tag:
        print "====== Type ======"
        print type(content)
        print "==================="
    print content
    print '++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++'

def __res2json(obj):
    return json.loads(obj.content)



def __get_page_json(args):
    page_temple = {
        "type": "appkit.page",
        "cid": 1,
        "pid": "",
        "auto_select": "false",
        "selectable": "yes",
        "force_display_in_property_view": "no",
        "has_global_content": "no",
        "need_server_process_component_data": "no",
        "is_new_created": "true",
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
            "site_title": "签到",
            "background": ""
        },
        "components": [
            {
                "type": "appkit.signdescription",
                "cid": 2,
                "pid": 1,
                "auto_select": "false",
                "selectable": "yes",
                "force_display_in_property_view": "no",
                "has_global_content": "no",
                "need_server_process_component_data": "no",
                "property_view_title": "签到",
                "model": {
                    "id": "",
                    "class": "",
                    "name": "",
                    "index": 2,
                    "datasource": {
                        "type": "api",
                        "api_name": ""
                    },
                    "undefined": "",
                    "title": args['sign_title'],
                    "description": args['sign_description'],
                    "image": args["share_pic"],
                    "share_description": args["share_description"],
                    "reply_keyword": args["reply_keyword"],
                    "reply_content": args["reply_content"],
                    "SignSettingGroupName": "",
                    "daily_group": "",
                    "daily_points": "1",
                    "daily_prizes": args['prizes']['prize_item1']['serial_count_prizes'],
                    "items": [
                        5,
                        6,
                        7
                    ]
                },
                "components": [
                    {
                        "type": "appkit.signitem",
                        "cid": 5,
                        "pid": 2,
                        "auto_select": "false",
                        "selectable": "no",
                        "force_display_in_property_view": "no",
                        "has_global_content": "no",
                        "need_server_process_component_data": "no",
                        "is_new_created": "true",
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
                            "serial_count": args['prizes']['prize_item2']['serial_count'],
                            "serial_count_points": args['prizes']['prize_item2']['serial_count_points'],
                            "serial_count_prizes":args['prizes']['prize_item2']['serial_count_prizes']
                        },
                        "components": []
                    },
                    {
                        "type": "appkit.signitem",
                        "cid": 6,
                        "pid": 2,
                        "auto_select": "false",
                        "selectable": "no",
                        "force_display_in_property_view": "no",
                        "has_global_content": "no",
                        "need_server_process_component_data": "no",
                        "is_new_created": "true",
                        "property_view_title": "",
                        "model": {
                            "id": "",
                            "class": "",
                            "name": "",
                            "index": 6,
                            "datasource": {
                                "type": "api",
                                "api_name": ""
                            },
                            "serial_count": args['prizes']['prize_item3']['serial_count'],
                            "serial_count_points": args['prizes']['prize_item3']['serial_count_points'],
                            "serial_count_prizes":args['prizes']['prize_item3']['serial_count_prizes']
                        },
                        "components": []
                    },
                    {
                        "type": "appkit.signitem",
                        "cid": 7,
                        "pid": 2,
                        "auto_select": "false",
                        "selectable": "no",
                        "force_display_in_property_view": "no",
                        "has_global_content": "no",
                        "need_server_process_component_data": "no",
                        "is_new_created": "true",
                        "property_view_title": "",
                        "model": {
                            "id": "",
                            "class": "",
                            "name": "",
                            "index": 7,
                            "datasource": {
                                "type": "api",
                                "api_name": ""
                            },
                            "serial_count": args['prizes']['prize_item4']['serial_count'],
                            "serial_count_points": args['prizes']['prize_item4']['serial_count_points'],
                            "serial_count_prizes":args['prizes']['prize_item4']['serial_count_prizes']
                        },
                        "components": []
                    }
                ]
            },
            {
                "type": "appkit.submitbutton",
                "cid": 3,
                "pid": 1,
                "auto_select": "false",
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
                "auto_select": "false",
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
    return json.dumps(page_temple)



##  获取优惠券id
def __get_coupon_rule_id(coupon_rule_name):
    coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
    return coupon_rule.id

## 获取新的 project_id
def _get_new_project_id(context):
    response = context.client.post("/termite2/api/project/?_method=put", {"source_template_id": -1})
    data = json.loads(response.content)["data"]
    return data['project_id']


@when(u'{user}添加签到活动"{sign_name}",并且保存')
def step_impl(context,user,sign_name):
    ##  获得feature数据
    sign_json = json.loads(context.text)

    status = sign_json['status']
    name = sign_json['name']
    share = {
        "img":sign_json["share_pic"],
        "desc":sign_json["share_describe"]
    }
    reply = {}
    keyword ={}
    keyword_reply = sign_json["keyword_reply"]
    for item in keyword_reply:
        rule = ""
        if item['rule']=="精确":
            rule = "accurate"
        elif item['rule']=="模糊":
            rule = "blur"
        keyword[item["key_word"]] = rule
    reply ={
        "keyword":keyword,
        "content":sign_json["share_describe"]
    }
    prize_settings = {}
    sign_settings = sign_json["sign_settings"]
    for item in sign_settings:
        prize_settings[item["sign_in"]]={
            "integral":item["integral"],
            "coupon":{
                "count":item["prize_counts"],
                "id":__get_coupon_rule_id(item["send_coupon"]),
                "name":item["send_coupon"]
            }
        }


    page_args ={
        "sign_title":"111活动名称",
        "sign_description":"1111签到活动说明",
        "share_pic":"/termite_static/img/component/sign/default_gift.png",
        "share_description":"1111分享描述",
        "reply_keyword":{
                            "11ka": "accurate",
                            "11kb": "blur"
                        },
        "reply_content": "1111回复内容",
        "prizes":{
            "prize_item1":{
                "serial_count":"1",
                "serial_count_points":"1",
                "serial_count_prizes":{
                    "id":405,
                    "name":"优惠券2",
                    "count":4
                }
            },
            "prize_item2":{
                "serial_count":"10",
                "serial_count_points":"100",
                "serial_count_prizes":{
                    "id":405,
                    "name":"优惠券2",
                    "count":4
                }
            },
            "prize_item3":{
                "serial_count":"20",
                "serial_count_points":"200",
                "serial_count_prizes":{
                    "id":404,
                    "name":"优惠券1",
                    "count":4
                }
            },
            "prize_item4":{
                "serial_count":"30",
                "serial_count_points":"300",
                "serial_count_prizes":{
                    "id":404,
                    "name":"优惠券1",
                    "count":4
                }
            }
        }
    }

    ##Step1模拟登陆Sign页面 Fin（初始页面所有HTML元素）
    get_sign_response = context.client.get("/apps/sign/sign/")
    sign_args_response = get_sign_response.context

    sign  = sign_args_response['sign']
    is_create_new_data = sign_args_response['is_create_new_data']
    project_id = sign_args_response['project_id']
    webapp_owner_id = sign_args_response['webapp_owner_id']
    keywords = sign_args_response['keywords']


    ##step2访问后台Phone页面 Fin(不是标准api请求，Phone页面HTML)
    url = "/termite2/webapp_design_page/?project_id={}&design_mode={}".format(project_id,1)
    get_termite_response = context.client.get(url)

    ##step3 获得Page右边个人配置JSON Fin(获得右边配置的空Json，这边主要是验证请求是否成功)
    get_dynamicPage_response = context.client.get('/apps/api/dynamic_pages/get/',{'project_id':project_id,"design_mode":0,"version":1})
    dynamicPage_data = get_dynamicPage_response

    bdd_util.assert_api_call_success(get_dynamicPage_response)

    ##step4 获得关键字OK
    keyword_response = context.client.get('/apps/sign/api/sign/')
    bdd_util.assert_api_call_success(keyword_response)

    #step5 POST,PageJSON到Mongo,返回Page_id(Fin)
    termite_url = "http://dev.weapp.com/termite2/api/project/?design_mode={}&project_id={}&version={}".format(0,project_id,1)
    termite_post_args={
        "field":"page_content",
        "id":project_id,
        "page_id":"1",
        "page_json": __get_page_json(page_args),
    }
    post_termite_response = context.client.post(termite_url,termite_post_args)
    bdd_util.assert_api_call_success(post_termite_response)

    page_related_id = __res2json(post_termite_response)['data']['project_id']

    #step6 POST,填写JSON至Mongo，返回JSON()
    sign_url = "http://dev.weapp.com/apps/sign/api/sign/?design_mode={}&project_id={}&version={}".format(0,project_id,1)
    post_sign_args = {
        "_method":"put",
        "name":name,
        "prize_settings":json.dumps(prize_settings),
        "reply":json.dumps(reply),
        "share":json.dumps(share),
        "status":"off",
        "related_page_id":page_related_id,
    }
    post_sign_response = context.client.post(sign_url,post_sign_args)
    bdd_util.assert_api_call_success(post_sign_response)





@then(u'{user}获得签到活动"{sign_name}"')
def step_impl(context,user,sign_name):
    #:88
    pass


@when(u'选择优惠券')
def step_impl(context):
    #331
    pass

@when(u'{user1}进入{user2}签到后台配置页面')
def step_impl(context,user1,user2):
    #341
    pass

@then(u'{user}获得优惠券列表,没有"{coupon}"')
def step_impl(context,user,coupon):
    #334
    pass

@when(u'{user}开启签到活动"{sign_name}"')
def step_impl(context,user,sign_name):
    #338
    pass


@then(u'{user}能获得签到活动{sign_name}的状态为{sign_tag}')
def step_impl(context,user,sign_name,sign_tag):
    #348
    pass