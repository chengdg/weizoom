#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.powerme.models import PowerMe, PowerMeParticipance, PowerMeControl
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

def __get_power_me_rule_name(title):
	material_url = material_models.News.objects.get(title=title).url
	power_me_rule_name = material_url.split('-')[1]
	return power_me_rule_name

def __get_power_me_rule_id(power_me_rule_name):
	return PowerMe.objects.get(name=power_me_rule_name).id

@When(u'{webapp_user_name}点击图文"{title}"进入微助力活动页面')
def step_impl(context, webapp_user_name, title):
	power_me_rule_name = __get_power_me_rule_name(title)
	power_me_rule_id = __get_power_me_rule_id(power_me_rule_name)
	url = '/m/apps/powerme/m_powerme/?webapp_owner_id=%s&id=%s' % (context.webapp_owner_id,power_me_rule_id)
	url = bdd_util.nginx(url)
	context.red_envelope_url = url
	response = context.client.get(url)
	print('response!!!!!!!')
	print(response)
	
@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中拥有{integral_count}助力值")
def step_tmpl(context, webapp_user_name, webapp_owner_name, integral_count):
	webapp_owner_id = context.webapp_owner_id
	appRecordId = __get_power_me_rule_id(power_me_rule_name)
	url = '/m/apps/powerme/api/powerme_participance/?_method=get?id=%s' % (appRecordId)
	print('!url!!!!!!!!!!!!')
	print(url)
	response = context.client.get(bdd_util.nginx(url))
	print('!response!!!!!!!!!!!!')
	print(response)
	member = response.context['member']
	actual = member.integral
	expected = int(integral_count)
	context.tc.assertEquals(expected, actual)