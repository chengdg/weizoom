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

def __get_coupon_rule_id(coupon_rule_name):
    coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
    return coupon_rule.id

#### 获取新的 project_id
def _get_new_project_id(context):
    response = context.client.post("/termite2/api/project/?_method=put", {"source_template_id": -1})
    data = json.loads(response.content)["data"]
    return data['project_id']


#### 获取 project_id 对应的json数据
def _get_page_json(context, project_id):
    url = "/termite2/api/pages_json/?project_id={}".format(project_id)
    response = context.client.get(url)
    data = json.loads(response.content)["data"]
    return json.loads(data)


#### 保存page
def _save_page(context, user, page):
    page = __supplement_page(page)
    data = __process_activity_data(context, page, user)

    url = "/termite2/api/project/?project_id={}".format(context.project_id)
    response = context.client.post(url, data)

    url = "/termite2/api/project/?project_id={}".format(context.project_id)
    data = {
        "field": 'is_enable',
        "id": context.project_id
    }
    response = context.client.post(url, data)



@when(u'{user}添加签到活动"{sign_name}",并且保存')
def step_impl(context,user,sign_name):
    #测试数据处理
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

    ###Step1模拟登陆Sign页面 Fin ########################################
    sign_response = context.client.get("/apps/sign/sign/")
    sign_page_response = sign_response.context

    sign  = sign_page_response['sign']
    is_create_new_data = sign_page_response['is_create_new_data']
    project_id = sign_page_response['project_id']
    webapp_owner_id = sign_page_response['webapp_owner_id']
    keywords = sign_page_response['keywords']

    # print "sign_response",sign_response
    # print "sign",sign
    # print "is_create_new_data",is_create_new_data
    # print "project_id",project_id
    # print "webapp_owner_id",webapp_owner_id
    # print "keywords",keywords

    ##上面获得全部参数


    ###step1 end##################


    ##step2  访问后台Phone页面##No
    # termite_response = context.client.get('/termite2/webapp_design_page/?project_id=%s&design_mode=%d'%("new_app:sign:0",0))
    # bdd_util.assert_api_call_success(termite_response)
    ##step2 end


    # ##step3 Page右边个人配置JSON的数据块OK
    dynamicPage_response = context.client.get('/apps/api/dynamic_pages/get/',{'project_id':project_id,"design_mode":0,"version":1})
    bdd_util.assert_api_call_success(dynamicPage_response)
    # ##step3 end

    # ##step4 获得关键字OK
    keyword_response = context.client.get('/apps/sign/api/sign/')
    bdd_util.assert_api_call_success(keyword_response)
    # #end step4

    # #step5 POST请求no
    # # var pageJson = JSON.stringify(page.toJSON());
    termite_post_args={
        "field":"page_content",
        "id":project_id,
        "page_id":"1"
        "page_json":page_json,
    }
    termite_post_response = context.client.post('/termite2/api/project/',{})
    # bdd_util.assert_api_call_success(termite_post_response)
    print project_id

    # print '+++++++++++++++++++++++++++++++++++++++==========START++++'
    # if sign and sign.id:
    #     print sign.id
    # #page_json: pageJson
    # # print termite_post_response
    # print '+++++++++++++++++++++++++++XXXXX++++++++++++++END+++++++++'






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


########### 堆栈
    # activityId = ""
    # if sign and sign.id:
    #     activityId = sign.id

    # params = {
    #     "related_page_id":project_id,#这个不对，得生一个Page获得
    #     "status":status,

    #     "name":name,
    #     "prize_settings":json.dumps(prize_settings),
    #     "reply":json.dumps(reply),
    #     "share":json.dumps(share)
    #  }


    # if is_create_new_data:
    #     response = context.client.post("/apps/sign/api/sign/?_method=put",params)
    # else:
    #     params['id'] = activityId
    #     params['signId'] = activityId
    #     response = context.client.post("/apps/sign/api/sign/?_method=post",params)

    # bdd_util.assert_api_call_success(response)



#提交Page
#http://dev.weapp.com/termite2/api/project/?design_mode=0&project_id=new_app:sign:56331b5ff44ad90d64ba88b3&version=1

#提交 JSON数据
#http://dev.weapp.com/apps/sign/api/sign/?design_mode=0&project_id=new_app:sign:56331b5ff44ad90d64ba88b3&version=1
