# -*- coding: utf-8 -*-
#_author_: liupeiyu

import json
from behave import *
from django.test.client import Client
from webapp import models as webapp_models
from test import bdd_util

@When(u"{user}创建微页面")
def step_impl(context, user):
	user = context.client.user

	pages = json.loads(context.text)
	for page in pages:
		context.project_id = _get_new_project_id(context)
		_save_page(context, user, page)


@Then(u"{user}能获取'{page_name}'")
def step_impl(context, user, page_name):
	user = context.client.user
	project = webapp_models.Project.objects.get(owner=user, site_title=page_name)
	project_id = project.id

	page_json = _get_page_json(context, project_id)[0]

	actual = __actual_page(page_json)
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@When(u"{user}编辑微页面'{page_name}'")
def step_impl(context, user, page_name):
	user = context.client.user
	project = webapp_models.Project.objects.get(owner=user, site_title=page_name)
	context.project_id = project.id

	page = json.loads(context.text)
	_save_page(context, user, page)


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
def _save_page(context, user, page):
	page = __supplement_page(page)
	data = __process_activity_data(context, page)

	url = "/termite2/api/project/?project_id={}".format(context.project_id)
	response = context.client.post(url, data)

	url = "/termite2/api/project/?project_id={}".format(context.project_id)
	data = {
		"field": 'is_enable',
		"id": context.project_id
	}
	response = context.client.post(url, data)



def __process_activity_data(context, page):
	project_id = context.project_id
	page_json = _get_page_json(context, project_id)[0]

	if page.has_key("title"):
		page_json['model']['site_title'] = page['title'].get('name', "")
		page_json['model']['site_description'] = page['title'].get('description', "")

	page_json['components'] = [page_json['components'][0]]

	__add_templet_title(page, page_json)
	__add_notice_text(page, page_json)

	data = {
		"field": "page_content",
		"id": project_id,
		"page_id": 1,
		"page_json": json.dumps(page_json)
	}
	return data

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
			"time": "2015-10-08 00:00",
			"align": "left",
			"background_color": "#FFF"
		}
	}

	if page.has_key('templet_title'):
		page_prototype.update(templet_title)
		
	page_prototype.update(page)
	return page_prototype


def __add_templet_title(page, page_json):
	pid = page_json['cid']
	cid = page_json['components'][0]['cid']
	if page.has_key("templet_title"):
		cid = cid + 1
		wepage_title = {
			"type":"wepage.title",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable":"yes",
			"force_display_in_property_view":"no",
			"has_global_content":"no",
			"need_server_process_component_data":"no",
			"is_new_created": True,
			"property_view_title": u"标题",
			"model": { "id":"","class":"","name":"","index":3,
				"datasource":{"type":"api","api_name":""},
				"title": "","subtitle":"","time":"2015-10-08 00:00",
				"align":"left","background_color": u"#FFF"},
			"components":[]
		}
		wepage_title['model'].update(page['templet_title'])
		page_json['components'].append(wepage_title)


def __add_notice_text(page, page_json):
	pid = page_json['cid']
	cid = page_json['components'][0]['cid']
	if page.has_key("notice_text"):
		cid = cid + 1
		wepage_notice = {
			"type":"wepage.notice",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "no",
			"is_new_created": True,
			"property_view_title": u"公告",
			"model": { "id":"", "class":"", "name":"", "index":4,
				"datasource":{"type":"api","api_name":""},
				"title": page['notice_text']
			}
		}
		page_json['components'].append(wepage_notice)



def __actual_page(page_json):
	actual = {
		"title": {
			"name": page_json['model']['site_title'],
			"description": page_json['model']['site_description']
		}
	}

	for component in page_json["components"]:
		actual_component = {}
		model = component['model']
		# 标题
		if component['type'] == "wepage.title":
			actual_component = {
				"templet_title": {
					"title": model['title'],
					"subtitle": model['subtitle'],
					"time": model['time'],
					"align": model['align'],
					"background_color": model['background_color']
				}
			}

		# 公告
		if component['type'] == "wepage.notice":
			default = u'默认显示公告，请填写内容，如果过长，将会在手机上滚动显示'
			actual_component = {
				"notice_text": model['title'] if model['title'] else default
			}

		actual.update(actual_component)
	return actual

