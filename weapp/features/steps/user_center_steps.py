#coding:utf8
"""@package features.steps.user_center_steps

"""


from behave import *

#from django.contrib.auth.models import User

from test import bdd_util
from features.testenv.model_factory import *


@when(u"{user}访问个人中心")
def step_impl(context, user):
	"""
	@note context字段参考 webapp/modules/user_center/request_util.py 中的 get_user_info()
	"""
	print("login as user " + user)
	webapp_owner_id = context.webapp_owner_id
	print("webapp_owner_id: %d" % webapp_owner_id)
	url = '/termite/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%d' % (webapp_owner_id)
	print("url: " + url)
	response = context.client.get(bdd_util.nginx(url), follow=True)
	
	# member类型是<class 'modules.member.models.Member'>
	member = response.context['member']
	
	#context.user_center_stats = _get_stats_from_user_center_page(response.content)
	context.user_center_stats = {
		u'全部订单': member.history_order_count,
		u'待支付': member.not_payed_order_count,
		u'待发货': member.not_ship_order_count,
		u'待收货': member.shiped_order_count,
		u'购物车': member.shopping_cart_product_count,
	}
	# dumping
	for k,v in context.user_center_stats.items():
		print("'%s': %d" % (k,v))


@then(u"'个人中心'中'{key}'数为{expected}")
def step_impl(context, key, expected):
	#print("expected order_count="+order_count)
	user_center_stats = context.user_center_stats
	print("key: %s, expected: %s" % (key, expected))
	for k,v in user_center_stats.items():
		print("'%s': %d" % (k,v))
	if user_center_stats is not None:
		context.tc.assertEquals(int(expected), user_center_stats[key])
	else:
		assert False

@then(u"'个人中心'中市场工具的数量为{expected}")
def step_impl(context, expected):
	#print("login as user " + user)
	webapp_owner_id = context.webapp_owner_id
	print("webapp_owner_id: %d" % webapp_owner_id)
	url = '/termite/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%d' % (webapp_owner_id)
	print("url: " + url)
	response = context.client.get(bdd_util.nginx(url), follow=True)
	
	# 源码在 request_util.get_user_info()中
	market_tools = response.context['market_tools']
	market_tools_count = len(market_tools)

	context.tc.assertEquals(int(expected), market_tools_count)
