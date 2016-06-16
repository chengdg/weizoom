#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

import json
import copy
from behave import *
from test import bdd_util
from mall import models as mall_models
from apps.customerized_apps.evaluate.models import ProductEvaluates

import apps_step_utils


def name2selection_type(name):
	name_dic = {u"单选":"single",u"多选":"multi"}
	if name:
		return name_dic[name]
	else:
		return None

def __bool2Bool(bo):
	"""
	JS字符串布尔值转化为Python布尔值
	"""
	bool_dic = {'true':True,'false':False,'True':True,'False':False}
	if bo:
		result = bool_dic[bo]
	else:
		result = None
	return result

def __name2Bool(name):
	"""
	"是"--> true
	"否"--> false
	"""
	name_dic = {u'是':"true",u'否':"false"}
	if name:
		return name_dic[name]
	else:
		return None

def __name2textlist(itemName):
	itemName_dic={u"姓名":'name',u"手机":'phone',u"邮箱":'email',u"QQ号":'qq',u"QQ":'qq',u"qq":'qq',u"职位":"job",u"住址":"addr"}
	if itemName:
		return itemName_dic[itemName]
	else:
		return ""

def __get_page_json(args):
	pid = "null"
	cid = 1
	index = 1

	next_pid = pid
	next_cid = cid
	next_index = index

	cur_pid = ""
	cur_cid = ""
	cur_index = ""

	#1.主模板 pid:1
	page_temple = {
		"type": "appkit.page",
		"cid": 1,
		"pid": "null",
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "背景",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": 1,
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"content_padding": "15px",
			"title": "index",
			"event:onload": "",
			"uploadHeight": "568",
			"uploadWidth": "320",
			"site_title": "商品评价",
			"background": ""
		},
		"components":[
			{
				"type": "appkit.evaluatedescription",
				"cid": 2,
				"pid": 1,
				"auto_select": False,
				"selectable": "no",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "商品评价",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 1
				},
				"components": []
			},
			{
				"type": "appkit.componentadder",
				"cid": 3,
				"pid": 1,
				"auto_select": False,
				"selectable": "yes",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "添加模块",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 3,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"components": ""
				},
				"components": []
			}
		]
	}

	cur_cid = 4
	cur_index = 4

	next_pid = 1
	next_cid = cur_cid+1
	next_index = cur_index+1

	#5.问答组件(用户自定义)  pid:5开始
	__qa_temple = {
		"type": "appkit.qa",
		"cid": '',
		"pid": 1,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "问答",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": "",
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"title": "",
			"is_mandatory": ""
		},
		"components": []
	}



	qa_arr = args['qa']
	next_index = next_index-2 #校准

	for qa in qa_arr:
		qa_title = qa['title']
		qa_required = __name2Bool(qa['is_required'])

		cur_pid = next_pid #1
		cur_cid = next_cid #5...
		cur_index = next_index #3...

		next_pid = cur_pid #1
		next_cid = cur_cid+1 #6...
		next_index = cur_index+1 #4...

		qa_temple =  copy.deepcopy(__qa_temple)
		qa_temple['cid'] = cur_cid
		qa_temple['model']['index'] = cur_index #校准顺序后4...
		qa_temple['model']['title'] = qa_title #校准顺序后4...
		qa_temple['model']['is_mandatory'] = qa_required #校准顺序后4...
		qa_temple['components']=[]

		page_temple['components'].append(qa_temple)


	#选择模块(据有内置模块)

	__selection_temple = {
		"type": "appkit.selection",
		"cid": "",
		"pid": 1,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": "",
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"title": "",
			"type": "",
			"is_mandatory": "true",
			"items": ""
		},
		"components": ""
	}

	__selectitem_temple = {
		"type": "appkit.selectitem",
		"cid": '',
		"pid": '',
		"auto_select": False,
		"selectable": "no",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": "",
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"title": ""
		},
		"components": []
	}


	selection_arr = args['selection']

	for selection in selection_arr:

		selection_title = selection['title']
		selection_type = name2selection_type(selection['type'])
		selection_required = __name2Bool(selection['is_required'])


		cur_pid = next_pid #1
		cur_cid = next_cid #7...
		cur_index = next_index #5...

		next_pid = cur_cid #1
		next_cid = cur_cid+1 #8...
		next_index = cur_index+1 #6...

		selection_temple = copy.deepcopy(__selection_temple)
		selection_temple['cid'] = cur_cid
		selection_temple['model']['index'] = cur_index
		selection_temple['model']['title'] = selection_title
		selection_temple['model']['type'] = selection_type
		selection_temple['model']['is_mandatory'] = selection_required
		selection_temple['model']['items']=[]#内部组件
		selection_temple['components']=[]#内部组件

		#内部拓展
		selectitem_arr = selection['option']
		for selectitem in selectitem_arr:

			selectitem_title = selectitem['options']

			#内部的id处理
			sub_cur_pid = cur_cid #1
			cur_cid = next_cid #7...
			# cur_index = next_index

			# next_pid = cur_cid #1
			next_cid = cur_cid+1 #8...
			# next_index = cur_index+1 #6...


			selectitem_temple = copy.deepcopy(__selectitem_temple)
			selectitem_temple['pid'] = sub_cur_pid
			selectitem_temple['cid'] = cur_cid
			selectitem_temple['model']['index'] = cur_cid #与父同，内部组件

			selectitem_temple['model']['title'] = selectitem_title
			selectitem_temple['components']=[]

			selection_temple['model']['items'].append(cur_cid)
			selection_temple['components'].append(selectitem_temple)

		page_temple['components'].append(selection_temple)


	#快捷模块(用户自定义)

	__textlist_temple = {
		"type": "appkit.textlist",
		"cid": "",
		"pid": 1,
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": '',
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"title": "",
			"modules":{},
			"items": []
		},
		"components": []
	}
	__itemadd_temple= {
		"type": "appkit.textitem",
		"cid": "",
		"pid": "",
		"auto_select": False,
		"selectable": "no",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": "",
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"title": "",
			"is_mandatory": "true"
		},
		"components": []
	}
	textlist_arr = args['textlist']
	for textlist in textlist_arr:

		items_arr = textlist['items_select']
		itemsadd_arr = textlist['items_add']

		cur_pid = next_pid #1
		cur_cid = next_cid #12...
		cur_index = next_index #6...

		next_pid = cur_cid #1
		next_cid = cur_cid+1 #13...
		next_index = cur_index+1 #7...

		textlist_temple = copy.deepcopy(__textlist_temple)
		textlist_temple['cid'] = cur_cid
		textlist_temple['model']['index'] = cur_index
		textlist_temple['model']['items'] = [] #内序列
		textlist_temple['components'] = [] #内部组件


		modules = {}
		for item in items_arr:
			item_name = __name2textlist(item['item_name'])
			is_selected = __bool2Bool(item['is_selected'])
			modules[item_name] = {'select':is_selected}

		textlist_temple['model']['modules']=modules

		for itemadd in itemsadd_arr:

			itemadd_name = itemadd['item_name']
			is_required = __name2Bool(itemadd['is_required'])

			#内部的id处理
			sub_cur_pid = cur_cid #1
			cur_cid = next_cid #7...

			next_cid = cur_cid+1 #8...

			itemadd_temple = copy.deepcopy(__itemadd_temple)

			itemadd_temple['pid'] = sub_cur_pid
			itemadd_temple['cid'] = cur_cid
			itemadd_temple['model']['index'] = cur_cid
			itemadd_temple['model']['title'] = itemadd_name
			itemadd_temple['model']['is_mandatory'] = is_required
			itemadd_temple['model']['items'] = []
			itemadd_temple['components'] = []

			textlist_temple['model']['items'].append(cur_cid)
			textlist_temple['components'].append(itemadd_temple)

		page_temple['components'].append(textlist_temple)

	return json.dumps(page_temple)

def get_product_review(order_code, product_name):
	product_id = mall_models.Product.objects.get(name=product_name).id
	product_review = ProductEvaluates.objects().get(product_id=product_id, order_id=order_code)

	return product_review


@when(u'{user}配置商品评论自定义模板')
def step_impl(context, user):
	given_data = json.loads(context.text)
	#访问页面，获得分配的project_id
	get_response = context.client.get("/apps/evaluate/evaluate/")
	project_id = get_response.context['project_id']
	design_mode = 0
	version = 1
	#编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	context.client.get(dynamic_url)

	page_json = __get_page_json({
		'qa': given_data.get('answer', ''),
		'selection': given_data.get('choose', ''),
		'textlist': given_data.get('participate_info', '')
	})

	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_termite_response = context.client.post(termite_url, {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	})
	related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

	post_evaluate_args = {
		"template_type": given_data.get('type', 'ordinary'),
		"related_page_id":related_page_id
	}
	evaluate_url ="/apps/evaluate/api/evaluate/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
	resp = context.client.post(evaluate_url, post_evaluate_args)
	bdd_util.assert_api_call_success(resp)

@then(u'{user}能获得商品评价评论模板')
def step_impl(context, user):
	expected_data = json.loads(context.text)
	get_response = context.client.get("/apps/evaluate/evaluate/")
	project_id = get_response.context['project_id']
	design_mode = 0
	version = 1
	#编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	resp = context.client.get(dynamic_url)
	returned_components = json.loads(resp.content)['data'][0]['components']

	apps_step_utils.debug_print(returned_components)
	#TODO 验证page数据

@then(u'{user}能获得订单"{order_id}"中的"{product_name}"评价详情')
def step_impl(context, user, order_id, product_name):
	product_review = get_product_review(order_id, product_name)

	design_mode = 0
	version = 1
	evaluate_url = "/apps/evaluate/api/evaluate_review/?design_mode={}&version={}&id={}".format(design_mode,version,product_review.id)
	evaluate_response = context.client.get(evaluate_url)

	evaluate_detail = json.loads(evaluate_response.content)['data']['items']

	actual = {}

	tag_list = []
	for tag in evaluate_detail['member_has_tags']:
		tag_list.append(tag['tag_name'])

	detail_list = []
	for detail in evaluate_detail['detail']:
		detail_list.append({
			'title': 'name' if detail['title'] == u'姓名' else detail['title'],
			'value': detail['answer']
		})

	actual['product_name'] = evaluate_detail['product_name']
	actual['order_no'] = evaluate_detail['order_num']
	actual['member'] = evaluate_detail['member_name']
	actual['member_rank'] = evaluate_detail['member_grade']
	actual['tags'] = tag_list
	actual['product_score'] = evaluate_detail['score']
	actual['picture_list'] = evaluate_detail['img']
	actual['comments'] = detail_list

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{webapp_owner}已完成对商品的评价信息审核")
def step_webapp_owner_verified_review(context, webapp_owner):
	"""
	 [{
		"member": "tom",
		"status": "-1",  -> ('-1', '已屏蔽'),  ('0', '待审核'),  ('1', '通过审核'),  ('1', '取消置顶'),  ('2', '通过并置顶')
		"product_name": "商品1",
		"order_no": "3"
	}, {
		"member": "bill",
		"status": "1",
		"product_name": "商品1",
		"order_no": "1"
	}]


	"""
	review_status = {
		u'已屏蔽': -1,
		u'待审核': 0,
		u'通过审核': 1,
		u'取消置顶': 1,
		u'通过并置顶': 2,
	}

	url = '/apps/evaluate/api/evaluate_review/?design_mode=0&version=1'
	context_dict = json.loads(context.text)
	for i in context_dict:
		product_name = i.get('product_name')
		order_code = i.get('order_no')
		product_review = get_product_review(order_code, product_name)

		args = {
			"product_review_id": product_review.id,
			"status": str(review_status[i.get("status")])
		}

		context.client.post(url, args)
		if 'time' in i and str(review_status[i.get("status")]) == "2":
			time = i['time']
			top_time = "{} 00:00".format(bdd_util.get_date_str(time))
			product_review.top_time = top_time
			product_review.save()

@when(u'{webapp_owner}已完成对商品的评价信息审核并置顶')
def step_impl(context, webapp_owner):
	assert False

@when(u'{webapp_owner}取消对商品的评价信息置顶')
def step_impl(context, webapp_owner):
	assert False

@when(u'{webapp_owner}屏蔽对商品的评价信息')
def step_impl(context, webapp_owner):
	assert False

@when(u'{webapp_owner}已完成对商品的评价信息置顶')
def step_impl(context, webapp_owner):
	assert False