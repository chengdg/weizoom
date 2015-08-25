#coding: utf8
"""
有关promotion_management的steps实现
"""

#import json
from behave import when

#from mall.promotion import models
#from modules.member.models import MemberGrade
#from features.testenv.model_factory import ProductFactory
from test import bdd_util


@when(u"{user}使优惠券失效")
def step_impl(context, user):
    print("disabled the coupons")
    assert False
