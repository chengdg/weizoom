# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.mall.models import *
from modules.member.models import * 

@when(u"{webapp_user_name}获得{webapp_owner_name}的{integral_count}会员积分")
def step_impl(context, webapp_user_name, webapp_owner_name, integral_count):
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	Member.objects.filter(id=member.id).update(integral=int(integral_count))


@then(u"{webapp_user_name}在{webapp_owner_name}的webapp中拥有{integral_count}会员积分")
def step_impl(context, webapp_user_name, webapp_owner_name, integral_count):
	url = '/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%s' % context.webapp_owner_id
	response = context.client.get(bdd_util.nginx(url), follow=True)
	member = response.context['member']

	actual = member.integral
	expected = int(integral_count)
	context.tc.assertEquals(expected, actual)

@Then(u'{webapp_user_name}在{webapp_owner_name}的webapp中获得积分日志')
def step_impl(context, webapp_user_name, webapp_owner_name):
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	integral_logs = MemberIntegralLog.objects.filter(member=member).order_by('-id')
	json_data = json.loads(context.text)
	actual_list = []
	for data in integral_logs:
		actual_list.append({"content": data.event_type, "integral": data.integral_count})

	bdd_util.assert_list(actual_list, json_data)