# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *


@then(u"{webapp_user_name}能获得webapp优惠券列表")
def step_impl(context, webapp_user_name):
	url = '/workbench/jqm/preview/?module=market_tool:coupon&model=usage&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%d&project_id=0&fmt=%s' % (context.webapp_owner_id, context.member.token)
	response = context.client.get(bdd_util.nginx(url))
	coupons = response.context['coupons']

	for coupon in coupons:
		if coupon.status == 0:
			coupon.status = u'未使用'
		else:
			coupon.status = u'unknown'

		coupon.money = coupon.money

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, coupons)
	

