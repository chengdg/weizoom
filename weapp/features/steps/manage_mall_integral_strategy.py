# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *

@given(u"{user}设定会员积分策略")
def step_impl(context, user):
	info = json.loads(context.text)

	data = {
		"integral_each_yuan": info.get(u"integral_each_yuan", 0),
		"be_member_increase_count": info.get(u"be_member_increase_count", 0),
		"click_shared_url_increase_count": info.get(u"click_shared_url_increase_count", 0),
		"buy_award_count_for_buyer": info.get(u"buy_award_count_for_buyer", 0),
		"order_money_percentage_for_each_buy": info.get(u"order_money_percentage_for_each_buy", 0),
		"buy_via_shared_url_increase_count_for_author": info.get(u"buy_via_shared_url_increase_count_for_author", 0),
		"buy_via_offline_increase_count_for_author": info.get(u"buy_via_offline_increase_count_for_author", 0),
		"buy_via_offline_increase_count_percentage_for_author": info.get(u"buy_via_offline_increase_count_percentage_for_author", 0),
		"buy_increase_count_for_father": info.get(u"buy_increase_count_for_father", 0),
		"use_ceiling": info.get(u"use_ceiling", 0),
		"review_increase": info.get(u"review_increase", 0),
		"use_condition": info.get("use_condition", 'off'),
		#"buy_via_offline_increase_count_percentage_for_author":info.get("buy_via_offline_increase_count_percentage_for_author", 0),
	}

	url = '/mall2/integral_strategy/'
	response = context.client.post(url, data)
	# TODO open
	# response = json.loads(response.content)
	# context.tc.assertEquals(200, response['code'])
