# -*- coding: utf-8 -*-
#_author_: liupeiyu

import json
from behave import *
from django.test.client import Client

@When(u"{user}创建微页面")
def step_impl(context, user):
	user = context.client.user

	pages = json.loads(context.text)
	for page in pages:
		project_id = _get_new_project_id(context)
		_save_page(context, user, project_id, page)

#### 获取新的 project_id
def _get_new_project_id(context):	
	response = context.client.post("/termite2/api/project/?_method=put", {"source_template_id": -1})
	data = json.loads(response.content)["data"]
	return data['project_id']


#### 获取 project_id 对应的json数据
def _get_page_json(context, project_id):
	url = "/termite2/api/pages_json/?project_id={}".format(project_id)
	response = context.client.get(url)
	data = json.loads(response.content)["data"]
	return json.loads(data)


#### 保存page
def _save_page(context, user, project_id, page):
	page = __supplement_page(page)
	page_json = _get_page_json(context, project_id)
	print '+++++++++++++++++++++++++'
	print type(page_json)
	print page_json[0]["components"]
	page_json = __process_activity_data(page)
	url = "/termite2/api/project/?project_id={}".format(project_id)
	context.client.post(url, page_json)


def __supplement_page(page):
	page_prototype = {
		"title":{
			"name": "",
			"description": ""
		}
	}

	templet_title = {	
		"templet_title":{
			"title": "",
			"subtitle": "",
			"time": "",
			"color": ""
		}
	}

	if hasattr(page, 'templet_title'):
		page_prototype.update(templet_title)
		
	page_prototype.update(page)
	return page_prototype