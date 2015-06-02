# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.models import *

ID = 0

def __process_menu(menu):
	global ID
	ID += 1
	data = {
		"type": "menu",
		"id": ID,
		"index": ID,
		"name": menu['name'],
		"items": [],
		"answer": {
			"workspace":"5",
			"workspace_name":"文章管理",
			"data_category":"文章分类",
			"data_item_name":"全部",
			"data_path":"文章管理-文章分类-全部",
			"data": menu["url"] if "url" in menu else ""
		}
	}

	if 'items' in menu:
		data['answer'] = {"type": "text", "content":""}
		ID += 1
		for menuitem in menu['items']:
			data['items'].append({
				"type": "menuitem",
				"id": ID,
				"index": ID,
				"name": menuitem['name'],
				"answer": {
					"workspace":"5",
					"workspace_name":"文章管理",
					"data_category":"文章分类",
					"data_item_name":"全部",
					"data_path":"文章管理-文章分类-全部",
					"data":menuitem["url"]
				}
			})

	return data


#######################################################################
# __process_navbar_data: 转换navbar的数据
#######################################################################
def __process_navbar_data(navbar):
	global ID
	ID = 0
	navs = []
	for menu in navbar:
		navs.append(__process_menu(menu))

	return json.dumps(navs)


@given(u"{user}添加了webapp的全局导航")
def step_impl(context, user):
	user = UserFactory(username=user)
	context.products = json.loads(context.text)
	if hasattr(context, 'client') is False:
		context.client = bdd_util.login(user, password=None, context=context)
	for product in context.products:
		__add_product(context, product)

		new_product = Product.objects.all().order_by('-id')[0]
		new_created_at = datetime.strptime('2014-06-01 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(seconds=new_product.id)
		new_product.created_at = new_created_at
		new_product.display_index = new_product.id
		new_product.save()


@when(u"{user}添加webapp的全局导航")
def step_impl(context, user):
	client = context.client
	navbar = json.loads(context.text)

	data = {
		"is_enable": "1",
		"data": __process_navbar_data(navbar)
	}

	response = context.client.post('/webapp/api/global_navbar/update/', data)
	bdd_util.assert_api_call_success(response)


@then(u"{user}能获得webapp的全局导航")
def step_impl(context, user):
	expected = json.loads(context.text)

	response = context.client.get('/webapp/api/global_navbar/get/')
	menus = json.loads(response.content)['data']['menus']
	menus.sort(lambda x,y: cmp(x['index'], y['index']))

	actual = []
	for menu in menus:
		print 'haha'
		if len(menu['items']) > 0:
			nav = {
				"name": menu['name'],
				"items": []
			}
			items = menu['items']
			items.sort(lambda x,y: cmp(x['index'], y['index']))			
			for menuitem in items:
				nav['items'].append({
					"name": menuitem['name'],
					"url": menuitem['answer']['data']
				})
			actual.append(nav)
		else:
			actual.append({
				"name": menu['name'],
				"url": menu['answer']['data']
			})

	bdd_util.assert_list(expected, actual)


@then(u"{webapp_user_name}能看到{webapp_owner_name}的webapp中的全局导航")
def step_impl(context, webapp_user_name, webapp_owner_name):
	pass