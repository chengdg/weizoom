# -*- coding: utf-8 -*-
#_author_: liupeiyu

import json
from behave import *
from django.test.client import Client
from webapp import models as webapp_models
from mall import models as mall_models
from test import bdd_util
from termite2 import pagerender

CONSTANT_CID = 0
display2mode = {u"轮播图": "swipe", u"分开显示": "sequence"}
display2name = {"swipe": u"轮播图", "sequence": u"分开显示"}

image_display2mode = {u"默认": "default", u"3列": "three"}
image_display2name = {"default": u"默认", "three": u"3列"}

product_modes = [u"大图", u"小图", u"一大两小", u"列表"]
product_types = [u"默认样式", u"简洁样式"]

class Request(object):
	def __init__(self, user):
		self.in_design_mode = True
		self.user_profile = user.get_profile()

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

	actual = __actual_page(page_json, user)
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

	_add_templet_title(page, page_json)
	_add_notice_text(page, page_json)
	_add_richtext(page, page_json)
	_add_textnav_group(page, page_json, user)
	_add_imagenav_group(page, page_json, user)
	_add_image_group(page, page_json, user)
	_add_image_display(page, page_json, user)
	_add_product_group(page, page_json, user)
	print '3242342'

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


def __actual_page(page_json, user):
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

		# 图片导航
		if component['type'] == "wepage.imagenav_group":
			actual_component = {
				"picture_ids": []
			}
			for item in component['components']:
				data = {
					"path": item['model']['image'],
					"title": item['model']['title'],
					"link": json.loads(item['model']['target'])['data_item_name']
				}
				actual_component["picture_ids"].append(data)

		# 图片广告
		if component['type'] == "wepage.image_group":
			actual_component = {
				"picture_ads": {
					"display_mode": display2name[component['model']['displayMode']],
					"values": []
				}
			}
			for item in component['components']:
				data = {
					"path": item['model']['image'],
					"title": item['model']['title'],
					"link": json.loads(item['model']['target'])['data_item_name']
				}
				actual_component["picture_ads"]["values"].append(data)

		# 橱窗
		if component['type'] == "wepage.image_display":
			model = component['model']
			actual_component = {
				"display_window": {
					"display_window_title": model['title'],
					"content_title": model['contentTitle'],
					"display_mode": image_display2name[model['displayMode']],
					"content_explain": model['content'],
					"values": []
				}
			}
			for item in component['components']:
				data = {
					"path": item['model']['image'],
					"picture_link": json.loads(item['model']['target'])['data_item_name']
				}
				actual_component["display_window"]["values"].append(data)

		# 商品
		if component['type'] == "wepage.item_group":
			model = component['model']
			actual_component = {
				"products": {
					"list_style1": product_modes[int(model['type'])],
					"list_style2": product_types[int(model['card_type'])],
					"show_product_name": 'true' if model['itemname'] else 'false',
					"show_price": 'true' if model['price'] else 'false',
					"items": []
				}
			}

			request = Request(user)
			pagerender.process_item_group_data(request, component)
			for item in component['components']:
				product = item['runtime_data'].get('product', None)
				if product:
					data = {
						"name": product['name'],
						"price": product['display_price']
					}
					actual_component["products"]["items"].append(data)
			print actual_component
			print '444444444444444'
		actual.update(actual_component)
	return actual


def __get_cid_and_pid(parent_json):	
	global CONSTANT_CID
	CONSTANT_CID = CONSTANT_CID + 1

	pid = parent_json['cid']
	cid = CONSTANT_CID
	return cid, pid

# 标题
def _add_templet_title(page, page_json):
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


# 公告
def _add_notice_text(page, page_json):
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

# 富文本
def _add_richtext(page, page_json):
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

# 文本导航
def _add_textnav_group(page, page_json, user):	
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

# 文本导航 二级
def __get_textnav_json(parent_json, textnav_data, user):
	cid, pid = __get_cid_and_pid(parent_json)
	
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
			"target": __get_target_link(textnav_data['navigation_link'], user),
			"image": ""
		},
		"components":[]
	}
	return textnav

def __get_target_link(name, user):
	user_id = user.id
	home_page = {"workspace":1,"workspace_name":u"店铺主页","data_category":u"店铺主页","data_item_name":u"店铺主页","data_path":u"店铺主页","data":"./?workspace_id=home_page&webapp_owner_id={}&project_id=0".format(user_id)}
	user_center = {"workspace":2,"workspace_name":u"会员主页","data_category":u"会员主页","data_item_name":u"会员主页","data_path":u"会员主页","data":"./?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id={}".format(user_id)}
	order_list = {"workspace":3,"workspace_name":u"我的订单","data_category":u"我的订单","data_item_name":u"我的订单","data_path":u"我的订单","data":"./?module=mall&model=order_list&action=get&workspace_id=mall&webapp_owner_id={}".format(user_id)}

	links = {
		u"店铺主页": json.dumps(home_page),
		u"会员主页": json.dumps(user_center),
		u"我的订单": json.dumps(order_list)
	}
	return links[name]

# 图片导航
def _add_imagenav_group(page, page_json, user):
	cid, pid = __get_cid_and_pid(page_json)
	
	if page.has_key("picture_ids"):
		imagenav_group = {
			"type":"wepage.imagenav_group",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "no",
			"is_new_created": True,
			"property_view_title": u"图片导航",
			"model": { "id":"", "class":"", "name":"", "index":7,
				"datasource":{"type":"api","api_name":""},
				"items":[]
			},
			"components":[]
		}
		for imagenav in page.get("picture_ids"):
			imagenav_json = __get_imagenav_json(imagenav_group, imagenav, user)
			# 加 图片导航的内部数据 
			imagenav_group["components"].append(imagenav_json)
			imagenav_group["model"]["items"].append(imagenav_json['cid'])

		page_json['components'].append(imagenav_group)

def __get_imagenav_json(parent_json, imagenav_data, user):
	cid, pid = __get_cid_and_pid(parent_json)
	
	imagenav = {
		"type":"wepage.image_nav",
		"cid": cid,
		"pid": pid,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": u"图片导航",
		"model": { "id":"", "class":"", "name":"", "index":1,
			"datasource":{"type":"api","api_name":""},
			"title": imagenav_data['title'],
			"target": __get_target_link(imagenav_data['link'], user),
			"image": imagenav_data['path']
		},
		"components":[]
	}
	return imagenav


# 图片广告
def _add_image_group(page, page_json, user):
	cid, pid = __get_cid_and_pid(page_json)

	if page.has_key("picture_ads"):
		image_group = {
			"type":"wepage.image_group",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "no",
			"is_new_created": True,
			"property_view_title": u"图片广告",
			"model": { "id":"", "class":"", "name":"", "index":8,
				"datasource":{"type":"api","api_name":""},
				"displayMode": display2mode[page['picture_ads']['display_mode']],
				"items":[]
			},
			"components":[]
		}
		for image in page.get("picture_ads").get("values", []):
			image_json = __get_image_json(image_group, image, user)
			# 加 图片广告的内部数据 
			image_group["components"].append(image_json)
			image_group["model"]["items"].append(image_json['cid'])

		page_json['components'].append(image_group)

def __get_image_json(parent_json, image_data, user):
	cid, pid = __get_cid_and_pid(parent_json)
	
	image = {
		"type":"wepage.imagegroup_image",
		"cid": cid,
		"pid": pid,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": u"一个广告",
		"model": { "id":"", "class":"", "name":"", "index":1,
			"datasource":{"type":"api","api_name":""},
			"title": image_data['title'],
			"target": __get_target_link(image_data['link'], user),
			"image": image_data['path']
		},
		"components":[]
	}
	return image

# 橱窗
def _add_image_display(page, page_json, user):
	cid, pid = __get_cid_and_pid(page_json)

	if page.has_key("display_window"):
		display_window = page['display_window']
		imagedisplay_group = {
			"type":"wepage.image_display",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "no",
			"is_new_created": True,
			"property_view_title": u"橱窗",
			"model": { "id":"", "class":"", "name":"", "index":9,
				"datasource":{"type":"api","api_name":""},
				"title": display_window['display_window_title'],
				"displayMode": image_display2mode[display_window['display_mode']],
				"contentTitle": display_window['content_title'],
				"content": display_window['content_explain'],
				"items":[]
			},
			"components":[]
		}
		for imagedisplay in display_window.get("values", []):
			imagedisplay_json = __get_imagedisplay_json(imagedisplay_group, imagedisplay, user)
			# 加 橱窗的内部数据 
			imagedisplay_group["components"].append(imagedisplay_json)
			imagedisplay_group["model"]["items"].append(imagedisplay_json['cid'])

		page_json['components'].append(imagedisplay_group)

def __get_imagedisplay_json(parent_json, imagedisplay_data, user):
	cid, pid = __get_cid_and_pid(parent_json)

	imagedisplay = {
		"type":"wepage.imagedisplay_image",
		"cid": cid,
		"pid": pid,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": u"一个橱窗",
		"model": { "id":"", "class":"", "name":"", "index":1,
			"datasource":{"type":"api","api_name":""},
			"target": __get_target_link(imagedisplay_data['picture_link'], user),
			"image": imagedisplay_data['path']
		},
		"components":[]
	}
	return imagedisplay

# 商品
def _add_product_group(page, page_json, user):
	cid, pid = __get_cid_and_pid(page_json)

	if page.has_key("products"):
		products = page['products']

		product_group = {
			"type":"wepage.item_group",
			"cid": cid,
			"pid": pid,
			"auto_select": False,
			"selectable": "yes",
			"force_display_in_property_view": "no",
			"has_global_content": "no",
			"need_server_process_component_data": "yes",
			"is_new_created": True,
			"property_view_title": u"商品",
			"model": { "id":"", "class":"", "name":"", "index":10,
				"datasource":{"type":"api","api_name":""},
				"type": product_modes.index(products['list_style1']),
				"card_type": product_types.index(products['list_style2']),
				"itemname": True if products.get('show_product_name',"false") == "true" else False,
				"price": True if products.get('show_price',"false") == "true" else False,
				"items":[],
				"container":""
			},
			"components":[]
		}
		for product in products.get("items", []):
			product_json = __get_product_json(product_group, product, user)
			# 加 橱窗的内部数据 
			product_group["components"].append(product_json)
			product_group["model"]["items"].append(product_json['cid'])

		page_json['components'].append(product_group)

def __get_product_json(parent_json, product_data, user):
	cid, pid = __get_cid_and_pid(parent_json)

	product = mall_models.Product.objects.get(name=product_data['name'])

	target = {
		"meta": {
			"id": product.id
		},
		"data": "./?module=mall&model=product&action=get&rid={}&workspace_id=mall&webapp_owner_id={}".format(product.id, user.id)
	}

	product_json = {
		"type":"wepage.item",
		"cid": cid,
		"pid": pid,
		"auto_select": False,
		"selectable": "no",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": u"一个商品",
		"model": { "id":"", "class":"", "name":"", "index":1,
			"datasource":{"type":"api","api_name":""},
			"title": u"选择商品",
			"target": json.dumps(target),
			"components":[]
		}
	}
	return product_json




@When(u"{user}按商品名称搜索")
def step_impl(context, user):
	user = context.client.user
	context.search = json.loads(context.text).get('search', "")

def __get_products(context):	
	context.page = context.page if hasattr(context, "page") else 1
	context.search = context.search if hasattr(context, "search") else ""

	data = {
		"type": "product",
		"count_per_page": "8",
		"query": context.search,
		"page": context.page
	}
	response = context.client.get("/termite2/api/webapp_datas/",data)
	return json.loads(response.content)

@Then(u"{user}在微页面获取'在售'商品选择列表")
def step_impl(context, user):
	user = context.client.user

	data = __get_products(context)["data"]["items"]

	actual_datas = []
	for product in data:
		actual_datas.append({
			"name": product["name"]
		})
	expected_datas = json.loads(context.text)
	bdd_util.assert_list(expected_datas, actual_datas)

@Then(u"{user}商品模块商品选择列表显示'{page_count}'页")
def step_impl(context, user, page_count):
	user = context.client.user
	max_page = __get_products(context)["data"]["pageinfo"]["max_page"]	
	actual = {"page_count": max_page}
	expected = {"page_count": page_count}
	bdd_util.assert_dict(expected, actual)

@When(u"{user}访问商品选择列表第'{page}'页")
def step_impl(context, user, page):
	user = context.client.user
	context.page = page

@When(u"{user}在微页面浏览'{page_type}'商品")
def step_impl(context, user, page_type):
	user = context.client.user
	context.page = int(context.page if hasattr(context, "page") else 1)

	if page_type == u'上一页':
		context.page = context.page - 1
	elif page_type == u'下一页':
		context.page = context.page + 1

	context.page = 1 if context.page<= 0 else context.page

