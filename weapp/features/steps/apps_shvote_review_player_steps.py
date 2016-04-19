#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.shvote.models import Shvote, ShvoteParticipance, ShvoteControl,MEMBER_STATUS
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member
import apps_step_utils as app_utils


def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_date = bdd_util.get_date_str(cr_date)
	p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
	return p_time

def __status2name(status_num):
	"""
	微助力：状态值 转 文字
	"""
	status2name_dic = {-1:u"全部",0:u"待审核",1:u"审核通过"}
	return status2name_dic[status_num]

def __name2status(name):
	"""
	微助力： 文字 转 状态值
	"""
	if name:
		name2status_dic = {u"全部":-1,u"待审核":0,u"审核通过":1}
		return name2status_dic[name]
	else:
		return -1

def __get_actions(status):
	"""
	根据输入微助力状态
	返回对于操作列表
	"""
	actions_list = [u"查看"]
	if status == u"待审核":
		actions_list = ["审核通过","删除"]+actions_list
	elif status=="审核通过":
		pass
	return actions_list

def __ReviewShvoteApply(context,player):
	'''
	审核通过
	'''
	design_mode = 0
	version = 1
	webapp_owner_id = str(context.webapp_owner_id)
	shvote = Shvote.objects.get(owner_id=context.webapp_owner_id)
	shvote_id = str(shvote.id)

	params = {
		"belong_to":shvote_id,
		"name":player
	}
	# update_data = {}
	# update_data['set__status'] = MEMBER_STATUS['PASSED']
	# shvote_participance = ShvoteParticipance.objects(**params).update(**update_data)
	one_shvote_participance = ShvoteParticipance.objects.get(**params)
	participance_id = str(one_shvote_participance.id)




	review_url = "/apps/shvote/api/shvote_registrators/?_method=post&design_mode={}&version={}".format(design_mode,version)
	review_args = {
		"id":participance_id
	}

	return context.client.post(review_url,review_args)

def __DeleteShvoteApply(context,player):
	'''
	审核不通过
	'''
	design_mode = 0
	version = 1
	webapp_owner_id = str(context.webapp_owner_id)
	shvote = Shvote.objects.get(owner_id=context.webapp_owner_id)
	shvote_id = str(shvote.id)

	params = {
		"belong_to":shvote_id,
		"name":player
	}
	# update_data = {}
	# update_data['set__status'] = MEMBER_STATUS['PASSED']
	# shvote_participance = ShvoteParticipance.objects(**params).update(**update_data)
	one_shvote_participance = ShvoteParticipance.objects(**params)[0]
	participance_id = str(one_shvote_participance.id)




	review_url = "/apps/shvote/api/shvote_registrators/?_method=delete&design_mode={}&version={}".format(design_mode,version)
	review_args = {
		"id":participance_id
	}

	return context.client.post(review_url,review_args)


@When(u"{webapp_user_name}于高级微信投票活动审核通过'{player}'")
def step_impl(context,webapp_user_name,player):
	review_response = __ReviewShvoteApply(context,player)
	bdd_util.assert_api_call_success(review_response)

@When(u"{webapp_user_name}于高级微信投票活动删除'{player}'")
def step_impl(context,webapp_user_name,player):
	review_response = __DeleteShvoteApply(context,player)
	bdd_util.assert_api_call_success(review_response)