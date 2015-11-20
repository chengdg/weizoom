#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from weixin.message.material import models as material_models
import termite.pagestore as pagestore_manager
import json
import datetime

def __debug_print(content,type_tag=True):
	"""
	debug工具函数
	"""
	if content:
		print '++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++'
		if type_tag:
			print "====== Type ======"
			print type(content)
			print "==================="
		print content
		print '++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++'
	else:
		pass



def __get_powermePageJson(args):
	__page_temple = {
			"type": "appkit.page",
			"cid": 1,
			"pid": None,
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
				"site_title": "微助力",
				"background": ""
			},
			"components": [
				{
					"type": "appkit.powermedescription",
					"cid": 2,
					"pid": 1,
					"auto_select": False,
					"selectable": "yes",
					"force_display_in_property_view": "no",
					"has_global_content": "no",
					"need_server_process_component_data": "no",
					"property_view_title": "微助力",
					"model": {
						"id": "",
						"class": "",
						"name": "",
						"index": 2,
						"datasource": {
							"type": "api",
							"api_name": ""
						},
						"title": args.get("title",""),
						"start_time": args.get("start_time",""),
						"end_time": args.get("end_time",""),
						"valid_time": args.get("valid_time",""),
						"timing": {
							"timing": {
								"select": args.get("timing_status","")
							}
						},
						"timing_value": {
							"day": args.get("timing_value_day",0),
							"hour": "00",
							"minute": "00",
							"second": "00"
						},
						"description": args.get("description",""),
						"reply_content": args.get("reply_content",""),
						"qrcode": args.get("qrcode",{"ticket":"","name":""}),
						"material_image": args.get("material_image",""),
						"background_image": args.get("background_image",""),
						"color": args.get("color",""),
						"rules": args.get("rules","")
					},
					"components": []
				},
				{
					"type": "appkit.submitbutton",
					"cid": 3,
					"pid": 1,
					"auto_select": False,
					"selectable": "no",
					"force_display_in_property_view": "no",
					"has_global_content": "no",
					"need_server_process_component_data": "no",
					"property_view_title": "",
					"model": {
						"id": "",
						"class": "",
						"name": "",
						"index": 99999,
						"datasource": {
							"type": "api",
							"api_name": ""
						},
						"text": "提交"
					},
					"components": []
				},
				{
					"type": "appkit.componentadder",
					"cid": 4,
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
	return json.dumps(__page_temple)



def __date_delta(start,end):
	"""
	格式：
		start:(str){2015-11-23}
		end :(str){2015-11-30}
	获得时间差，返回int型
	"""
	start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
	end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
	return (end-start).days


@when(u'{user}新建微助力活动')
def step_impl(context,user):
	design_mode = 0
	version = 1
	text = json.loads(context.text)
	__debug_print(text)

	title = text.get("name","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{}+00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{}+00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	timing_status = text.get("is_show_countdown","true")
	timing_value_day = __date_delta(start_date,end_date)

	description = text.get("desc","")
	reply_content = text.get("reply")
	qrcode = text.get("qr_code","")
	material_image = text.get("share_pic","")
	background_image = text.get("background_pic","")

	zh2color = {u"冬日暖阳":"yellow",u"玫瑰茜红":"red",u"热带橙色":"orange"}
	zhcolor = text.get("background_color","冬日暖阳")
	color = zh2color[zhcolor]

	rules = text.get("rules","")

	page_args = {
		"title":title,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"timing_status":timing_status,
		"timing_value_day":timing_value_day,
		"description":description,
		"reply_content":reply_content,
		"qrcode":qrcode,
		"material_image":material_image,
		"background_image":background_image,
		"color":color,
		"rules":rules
	}




	#step1：登录页面，获得分配的project_id
	get_pw_response = context.client.get("/apps/powerme/powerme/")
	pw_args_response = get_pw_response.context
	project_id = pw_args_response['project_id']#(str){new_app:powerme:0}

	#step2: 编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	dynamic_response = context.client.get(dynamic_url)
	dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

	#step3:发送Page
	page_json = __get_powermePageJson(page_args)

	termite_post_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}
	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_termite_response = context.client.post(termite_url,termite_post_args)

	#step4:发送powerme_args






@then(u'{user}获得微助力活动列表')
def step_impl(context,user):
	pass

