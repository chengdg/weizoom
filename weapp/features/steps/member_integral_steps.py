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
		"integral_each_yuan": info.get(u"一元等价的积分数量", 5),
		"be_member_increase_count": info.get(u"成为会员赠送积分", 20),
		"click_shared_url_increase_count": info.get(u"分享链接给好友点击", 25),
		"buy_award_count_for_buyer": info.get(u"购物返积分额度", 21),
		"order_money_percentage_for_each_buy": info.get(u"每次购物后，额外积分（以订单金额的百分比计算）", "0.0"),
		"buy_via_shared_url_increase_count_for_author": info.get(u"通过分享链接购买为分享者增加的额度", 11),
		"buy_via_offline_increase_count_for_author": info.get(u"线下会员购买为推荐者增加的额度", 30),
		"buy_via_offline_increase_count_percentage_for_author": info.get(u"线下会员购买为推荐者增加的额度", 30),
		"buy_increase_count_for_father": info.get(u"线下会员购买为推荐者额外增加的额度", "0.0"),
		"use_ceiling": info.get(u"订单积分抵扣上限", 0),
		"review_increase": info.get(u"review_increase", 0)
	}

	url = '/mall2/integral_strategy/'
	response = context.client.post(url, data)
	# TODO open
	# response = json.loads(response.content)
	# context.tc.assertEquals(200, response['code'])
