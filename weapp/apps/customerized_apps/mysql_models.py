# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import mongoengine as mongo_models

#记录领取优惠券的log信息
class ConsumeCouponLog(mongo_models.Document):
    user_id = mongo_models.LongField() #活动所属者id
    app_name = mongo_models.StringField(default="") #活动所属app的名称
    app_id = mongo_models.StringField(default="", max_length=100) #活动id
    member_id = mongo_models.IntField(default=0)#领取人的id
    coupon_id  = mongo_models.IntField(default=0) #优惠券id
    coupon_msg = mongo_models.StringField(default="") #领取优惠记录的信息
    created_at = mongo_models.DateTimeField() #创建时间

    meta = {
		'collection': 'consume_coupon_log'
	}