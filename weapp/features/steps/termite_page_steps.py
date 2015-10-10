# -*- coding: utf-8 -*-
#_author_: liupeiyu

import json
from behave import *
from django.test.client import Client
from webapp import models as webapp_models
from test import bdd_util

CONSTANT_CID = 0

@Given(u"{user}已添加微页面")
def step_impl(context, user):
	user = context.client.user

	pages = json.loads(context.text)
	for page in pages:
		page_json = {
			"title":{
				"name": page.get('name')
			}
		}
		context.project_id = _get_new_project_id(context)
		_save_page(context, user, page_json)
		create_time = page.get('create_time', "")
		if create_time:
			webapp_models.Project.objects.filter(id=context.project_id).update(created_at=create_time)


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

@When(u"{user}删除微页面'{page_name}'")
def step_impl(context, user, page_name):
	user = context.client.user
	project = webapp_models.Project.objects.get(owner=user, site_title=page_name)

	context.client.post("/termite2/api/project/?_method=delete",{"id": project.id})


@When(u"{user}修改微页面标题'{page_name}'")
def step_impl(context, user, page_name):
	user = context.client.user
	project = webapp_models.Project.objects.get(owner=user, site_title=page_name)
	new_name = json.loads(context.text)["name"]

	data = {
		"field": "site_title", 
		"id": project.id,
		"value": new_name
	}
	context.client.post("/termite2/api/project/", data)


@When(u"{user}设置主页'{page_name}'")
def step_impl(context, user, page_name):
	user = context.client.user
	project = webapp_models.Project.objects.get(owner=user, site_title=page_name)

	data = {"id": project.id}
	context.client.post("/termite2/api/active_project/?_method=put", data)


@Then(u"{user}能获取微页面列表")
def step_impl(context, user):
	user = context.client.user
	response = context.client.get("/termite2/api/pages/")
	data = json.loads(response.content)["data"]["items"]

	actual_datas = []
	for page in data:
		if page['siteTitle'] == u'空白页面':
			actual_datas.append({
				"name": page["siteTitle"]
			})
		else:
			actual_datas.append({
				"name": page["siteTitle"],
				"create_time": page['createdAt']
			})

	expected_datas = json.loads(context.text)
	bdd_util.assert_list(expected_datas, actual_datas)	


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
	data = __process_activity_data(context, page, user)

	url = "/termite2/api/project/?project_id={}".format(context.project_id)
	response = context.client.post(url, data)

	url = "/termite2/api/project/?project_id={}".format(context.project_id)
	data = {
		"field": 'is_enable',
		"id": context.project_id
	}
	response = context.client.post(url, data)


def __process_activity_data(context, page, user):
	project_id = context.project_id
	page_json = _get_page_json(context, project_id)[0]

	if page.has_key("title"):
		page_json['model']['site_title'] = page['title'].get('name', "")
		page_json['model']['site_description'] = page['title'].get('description', "")

	page_json['components'] = [page_json['components'][0]]

	# 给global CONSTANT_CID赋值
	global CONSTANT_CID
	CONSTANT_CID = page_json['cid']

	__add_templet_title(page, page_json)
	__add_notice_text(page, page_json)
	__add_richtext(page, page_json)
	__add_textnav_group(page, page_json, user)

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
			actual_component = {
				"notice_text": model['title']
			}

		# 富文本
		if component['type'] == "wepage.richtext":
			actual_component = {
				"multy_text_content": model['content']
			}

		# 文本导航
		if component['type'] == "wepage.textnav_group":
			actual_component = {
				"navigation": []
			}
			for item in component['components']:
				data = {
					"navigation_name": item['model']['title'],
					"navigation_link": json.loads(item['model']['target'])['data_item_name']
				}
				actual_component["navigation"].append(data)

		actual.update(actual_component)
	return actual


def __get_cid_and_pid(parent_json):	
	global CONSTANT_CID
	CONSTANT_CID = CONSTANT_CID + 1

	pid = parent_json['cid']
	cid = CONSTANT_CID
	return cid, pid


def __add_templet_title(page, page_json):
	cid, pid = __get_cid_and_pid(page_json)

	if page.has_key("templet_title"):
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
	cid, pid = __get_cid_and_pid(page_json)

	default = u'请填写内容，如果过长，将会在手机上滚动显示'
	if page.has_key("notice_text"):
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
				"title": page['notice_text'] if page['notice_text'] else default
			}
		}
		page_json['components'].append(wepage_notice)


def __add_richtext(page, page_json):
	cid, pid = __get_cid_and_pid(page_json)

	if page.has_key("multy_text_content"):
		wepage_notice = {
			"type":"wepage.richtext",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "no",
			"is_new_created": True,
			"property_view_title": u"富文本",
			"model": { "id":"", "class":"", "name":"", "index":5,
				"datasource":{"type":"api","api_name":""},
				"content": page['multy_text_content']
			}
		}
		page_json['components'].append(wepage_notice)


def __add_textnav_group(page, page_json, user):	
	cid, pid = __get_cid_and_pid(page_json)

	if page.has_key("navigation"):
		textnav_group = {
			"type":"wepage.textnav_group",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "no",
			"is_new_created": True,
			"property_view_title": u"文本导航",
			"model": { "id":"", "class":"", "name":"", "index":6,
				"datasource":{"type":"api","api_name":""},
				"items":[]
			},
			"components":[]
		}
		for textnav in page.get("navigation"):
			textnav_json = __get_textnav_json(textnav_group, textnav, user)
			# 加 文本导航的内部数据 
			textnav_group["components"].append(textnav_json)
			textnav_group["model"]["items"].append(textnav_json['cid'])

		page_json['components'].append(textnav_group)


def __get_textnav_json(parent_json, textnav_data, user):
	cid, pid = __get_cid_and_pid(parent_json)
	
	home_page = {"workspace":3,"workspace_name":u"店铺主页","data_category":u"店铺主页","data_item_name":u"店铺主页","data_path":u"店铺主页","data":"./?workspace_id=home_page&webapp_owner_id={}&project_id=0".format(user.id)}
	user_center = {"workspace":4,"workspace_name":u"会员主页","data_category":u"会员主页","data_item_name":u"会员主页","data_path":u"会员主页","data":"./?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id={}".format(user.id)}

	links = {
		u"店铺主页": json.dumps(home_page),
		u"会员主页": json.dumps(user_center)
	}

	textnav = {
		"type":"wepage.textnav",
		"cid": cid,
		"pid": pid,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": u"文本导航",
		"model": { "id":"", "class":"", "name":"", "index":1,
			"datasource":{"type":"api","api_name":""},
			"title": textnav_data['navigation_name'],
			"target": links[textnav_data['navigation_link']],
			"image": ""
		},
		"components":[]
	}
	return textnav
