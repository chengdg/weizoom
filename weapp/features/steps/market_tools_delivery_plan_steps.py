# -*- coding: utf-8 -*-
import json
import time
from test import bdd_util
from django.contrib.auth.models import User
from market_tools.tools.test_game.models import *
from market_tools.tools.delivery_plan.models import *
from webapp.models import Workspace
from mall.models import Product


def __add_delivery_plan(context, delivery_plan, user):
	user = User.objects.get(username=user)
	if(delivery_plan['type']==u'月'):
		delivery_plan['type'] = 2
	elif(delivery_plan['type']==u'周'):
		delivery_plan['type'] = 1
	else:
		delivery_plan['type'] = 0
	delivery_plan['product_id']  = 	Product.objects.get(name=delivery_plan['product'], owner=user).id
	context.client.post("/market_tools/delivery_plan/deliver_plan/create/", delivery_plan)


@when(u"{user}添加配送套餐")
def step_impl(context, user):
	client = context.client
	context.delivery_plans = json.loads(context.text)
	for delivery_plan in context.delivery_plans:
		__add_delivery_plan(context, delivery_plan, user)
		time.sleep(1)

@given(u"{user}添加配送套餐")
def step_impl(context, user):
	client = context.client
	context.delivery_plans = json.loads(context.text)
	for delivery_plan in context.delivery_plans:
		__add_delivery_plan(context, delivery_plan, user)
		time.sleep(1)

@then(u"{user}能获得配送套餐'{test_delivery_plan}'")
def step_impl(context, user, test_delivery_plan):
	existed_delivery_plans = DeliveryPlan.objects.get(name=test_delivery_plan)

	expected = json.loads(context.text)
	response = context.client.get('/market_tools/delivery_plan/delivery_plan/update/%d/' % existed_delivery_plans.id)
	delivery_plan = response.context['delivery_plan']

	product_name = Product.objects.get(id=existed_delivery_plans.product_id).name
	if(delivery_plan.type==2):
		delivery_plan.type = u'月'
	elif(delivery_plan.type==1):
		delivery_plan.type = u'周'
	else:
		delivery_plan.type = u'天'
	
	actual = {
		"name": delivery_plan.name,
		"product": product_name,
		"type": delivery_plan.type,
		"frequency": str(delivery_plan.frequency),
		"times": str(delivery_plan.times),
		"price": str(int(delivery_plan.price))
	}
	expected['product'] = expected['name']
	bdd_util.assert_dict(expected, actual)

@then(u"{user}能获得配送套餐列表")
def step_impl(context, user):
	user = User.objects.get(username=user)
	delivery_plans = DeliveryPlan.objects.filter(owner=user)
	expected = json.loads(context.text)
	response = context.client.get('/market_tools/delivery_plan/')
	response_delivery_plans = response.context['delivery_plans']
	actual = []
	for delivery_plan in response_delivery_plans:
		actual.append({
			"name": delivery_plan.name
		})
	bdd_util.assert_list(expected, actual)

@when(u"{user}删除配送套餐'{test_delivery_plan}'")
def step_impl(context, user, test_delivery_plan):
	user = User.objects.get(username=user)
	delivery_plan_id = DeliveryPlan.objects.get(owner=user, name=test_delivery_plan).id
	response = context.client.get('/market_tools/delivery_plan/delete/%d/' % delivery_plan_id)

