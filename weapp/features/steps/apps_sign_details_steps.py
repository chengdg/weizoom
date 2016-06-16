#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cl'

from behave import *
from test import bdd_util
from collections import OrderedDict
from features.testenv.model_factory import *
import steps_db_util
#from mall import module_api as mall_api
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule
from weixin.message.material import models as material_models
from apps.customerized_apps.sign import models as sign_models
import termite.pagestore as pagestore_manager
from apps.customerized_apps.sign.models import Sign,SignParticipance
import json
from modules.member import models as member_models
from utils.string_util import byte_to_hex

@then(u"{user}获得'{member_name}'参加'{sign_name}'的签到详情列表")
def step_impl(context, user,member_name,sign_name):
	design_mode = 0
	count_per_page = 15
	version = 1
	page = 1
	enable_paginate = 1
	belong_to = Sign.objects.get(name=sign_name).id
	member_id = member_models.Member.objects.get(username_hexstr=byte_to_hex(member_name)).id
	params = {
		"member_id": member_id,
		"belong_to": belong_to,
		"count_per_page": 15,
		"page": 1
	}
	response = context.client.get('/apps/sign/api/sign_participance_details/?_method=put', params)
	participance_detatils = json.loads(response.content)['data']['items']
	actual = []
	for detail in participance_detatils:
		p_dict = OrderedDict()
		p_dict[u"sign_time"] = bdd_util.get_date_str(detail['created_at_f'])
		p_dict[u"get_reward"] = detail['prize'].replace('<br/>','')
		p_dict[u"sign_state"] = detail['status']
		actual.append((p_dict))
	print("actual_data: {}".format(actual))
	expected = []
	if context.table:
		for row in context.table:
			cur_p = row.as_dict()
			if cur_p[u'sign_time']:
				cur_p[u'sign_time'] = bdd_util.get_date_str(cur_p[u'sign_time'])
			expected.append(cur_p)
	else:
		for p in json.loads(context.text):
			if p[u'sign_time']:
				p[u'sign_time'] = bdd_util.get_date_str(p[u'sign_time'])
			expected.append(p)
	print("expected: {}".format(expected))

	bdd_util.assert_list(expected, actual)
