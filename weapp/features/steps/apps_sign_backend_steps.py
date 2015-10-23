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


def __get_coupon_rule_id(coupon_rule_name):
    coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
    return coupon_rule.id

default_date = '2000-01-01'
def __get_date(date):
    date = bdd_util.get_date_str(date)
    if date == default_date:
        date = ''
    return date

@give(u'{user}登录系统')
def step_impl(context,user):
	context.client - bdd_util.login(user,password="test",context=context)

@when(u'{user}参加抽奖活动')


#问题
#1.引号的数据是期望数据，还是填入数据，when，given，then
#2.steps是如何找到feature的，神奇的，怎么关联的，weapp里面是不是有一个东西勾住了
#3.steps通过import来导入系统操作与否
#4.每个函数就是来，判断结果是否正确
#5.content是全局变量传递么

#6.print和打断点

#7.多feathure一个steps？？

#8.同样是登录系统，别人实现过了，我要重写么，不写？彻底全局？？given不写了？
#9.函数的名字，一定是step_impl么，参数有限制么？

#10.完成自己的就行

#11.weapp里面，大量的哪地方是全局，上下文怎么着