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


@when(u'{user}添加积分')
def step_impl(context,user):
    #:24
    pass
@when(u'{user}添加签到活动"{sign_name}",并且保存')
def step_impl(context,user,sign_name):
    #40
    pass

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
