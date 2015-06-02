# -*- coding: utf-8 -*-
"""@package features.steps.services_steps
有关services的step实现

"""
import json

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from webapp.modules.mall.models import *

__author__ = "Victor"


@then(u'{user}获得未读订单提示数量为{count}')
def step_impl(context, user, count):
	if hasattr(context, 'client'):
		context.client.logout()
	#print("login as user " + user)
	context.client = bdd_util.login(user)
	client = context.client
	url = '/webapp/api/unread_count_notify/get/'
	# API源码地址: get_unread_count_notify(),  in `webapp/api_views.py`
	context.response = client.get(url, follow=True)
	response_json = json.loads(context.response.content)
	assert response_json.get('success')
	data = response_json['data']
	"""
	举例:
	~~~~~~~~~
	"data": {"unread_realtime_count": 0, "unread_notice_count": 0, "unread_order_count": 0}
	~~~~~~~~~
	"""
	#print("response: {}".format(response_json))
	context.tc.assertEquals(int(count), data['unread_order_count'])


"""
@when(u"系统向service '{service_name}' 发消息")
def step_impl(context, service_name):
	print("deprecated")
	print("service_name: {}".format(service_name))
	args = json.loads(context.text)  # 读入JSON格式的消息
	assert hasattr(context, 'webapp_owner_id')
	args['webapp_owner_id'] = context.webapp_owner_id
	assert hasattr(context, 'created_order_id')
	assert context.created_order_id != -1
	args['order_id'] = context.created_order_id  # 近期的订单
	print("args: {}".format(args))

	from webapp.handlers import event_handler_util
	request = DummyRequest(args)
	event_handler_util.handle(request, service_name)
	#assert False
"""
