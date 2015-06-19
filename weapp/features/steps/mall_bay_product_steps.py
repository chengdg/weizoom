# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from tools.express import util as express_util
from core import dateutil


@given(u"{webapp_user_name}已有{user}发放的优惠券")
def step_impl(context, webapp_user_name, user):
	user = context.client.user
	profile = context.client.user.profile
	webapp_id = context.client.user.profile.webapp_id

	context.coupons = json.loads(context.text)
	for coupon in context.coupons:
		_save_coupon(user, coupon)

def _save_coupon(user, coupon_data):
	coupon_price = coupon_data.get('coupon_amount')
	rule = CouponRule.objects.create(
		owner=user,
		name=coupon_data.get('coupon_name'),
		valid_days=120,
		money=coupon_price,
		count=1,
		remained_count=1
	)
	Coupon.objects.create(
		owner=user,
		coupon_rule=rule,
		provided_time=datetime.now(),
		start_time=datetime.now(),
		expired_time=datetime.now() + timedelta(10),
		coupon_id=coupon_data.get('coupon_id'),
		money=coupon_price
	)
