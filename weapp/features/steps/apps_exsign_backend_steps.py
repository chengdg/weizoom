#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.member.models import MemberGrade

__author__ = 'cl'

from behave import *
from test import bdd_util
from collections import OrderedDict
from features.testenv.model_factory import *

from mall.promotion import models as  promotion_models

import termite.pagestore as pagestore_manager
from apps.customerized_apps.exsign.models import exSign,exSignParticipance
import json

global delete_switch
delete_switch = True

def __debug_print(content,type_tag=True):
	"""
	debug工具函数
	"""
	if content:
		print('++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++')
		if type_tag:
			print("====== Type ======")
			print(type(content))
			print("===================")
		print(content)
		print('++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++')
	else:
		pass

def __res2json(obj):
	"""
	response 转换 json
	"""
	return json.loads(obj.content)

def __get_coupon_rule_id(coupon_rule_name):
	"""
	获取优惠券id
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
	return coupon_rule.id

def __get_coupon_rule_name(coupon_rule_name):
	"""
	获取优惠券name
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
	return coupon_rule.name

def __get_coupon_rule_count(coupon_rule_name):
	"""
	获取优惠券count
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
	return coupon_rule.count

def __get_coupon_member_grade_json(coupons):
	"""
	获取优惠券json
	"""
	coupon_name_list = []
	member_grade_list = []
	for c in coupons:
		coupon_name_list.append(c["send_coupon"])
		member_grade_list.append(c["member_grade"])
	coupon_rules = promotion_models.CouponRule.objects.filter(name__in=coupon_name_list)
	grade_name2grade_id = {mg.name: mg.id for mg in MemberGrade.objects.filter(name__in=member_grade_list)}
	coupon_name2coupon = {}
	for coupon_rule in coupon_rules:
		coupon_name2coupon[coupon_rule.name] ={
			"id": coupon_rule.id,
			"count": coupon_rule.count
		}
	re_coupons = []
	for coupon in coupons:
		coupon_name = coupon["send_coupon"]
		re_coupons.append({
			"id": coupon_name2coupon[coupon_name]["id"],
			"count": coupon_name2coupon[coupon_name]["count"],
			"name": coupon_name,
			"grade_id": grade_name2grade_id.get(coupon["member_grade"], 0)
		})

	return re_coupons

def __get_exsign(context):
	"""
	step1 登录Sign页面
	"""
	get_sign_response = context.client.get("/apps/exsign/exsign/")
	sign_args_response = get_sign_response.context
	return sign_args_response

def __get_Termite(context,project_id,design_mode=1):
	"""
	step2 访问PC的Phone页面termite2
	"""
	url = "/termite2/webapp_design_page/?project_id={}&design_mode={}".format(project_id,design_mode)
	get_termite_response = context.client.get(url)
	return get_termite_response

def __get_DynamicPage(context,project_id,design_mode=0,version=1):
	"""
	step3 获得Page右边个人配置JSON
	"""
	get_dynamicPage_response = context.client.get('/apps/api/dynamic_pages/get/',{'project_id':project_id})
	bdd_util.assert_api_call_success(get_dynamicPage_response)
	return get_dynamicPage_response


def __post_PageJson(context,post_args,project_id,design_mode=0,version=1):
	"""
	step5 POST,PageJSON到Mongo,返回Page_id

	参数：
	termite_post_args={
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": "",
	}

	"""
	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	if post_args:
		termite_post_args = post_args
	else:
		termite_post_args={
			"field":"page_content",
			"id":project_id,
			"page_id":"1",
			"page_json": "",
		}
	post_termite_response = context.client.post(termite_url,termite_post_args)
	bdd_util.assert_api_call_success(post_termite_response)
	return post_termite_response

def __post_ExSignArgs(context,exsign_args,project_id,method="post",design_mode=0,version=1):
	"""
	step6 POST,填写JSON至Mongo
	"""

	if method == 'put':
		exsign_url = "/apps/exsign/api/exsign/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
	elif method == 'post':
		exsign_url = "/apps/exsign/api/exsign/?design_mode={}&project_id={}&version={}&_method=post".format(design_mode,project_id,version)

	post_exsign_response = context.client.post(exsign_url,exsign_args)
	post_exsign_response = json.loads(post_exsign_response.content)
	return post_exsign_response

def __get_PageJson(args):
	"""
	Page模板
	传入args：生成Page

	#####
	args结构
	#####
	args ={
		"sign_title":name,
		"sign_description":sign_describe,
		"share_pic":share.get('img',""),
		"share_description":share.get('desc',""),
		"prizes":page_prizes
	}

	page_prizes = {}#Page记录数据
	for i in range(len(prize_settings_arr)):
		item = prize_settings_arr[i]
		page_prizes["prize_item%d"%i]={
				"serial_count":prize_settings_arr[i]["serial_count"],
				"serial_count_points":prize_settings_arr[i]["serial_count_points"],
				"serial_count_prizes":prize_settings_arr[i]["serial_count_prizes"]
		}
	"""
	__prizes = args.get('prizes',"")
	__items = range(5,5-1+len(__prizes))
	__inner_components = []
	if __prizes:
		index=0
		for i in __items:
			index += 1
			__components_tmp = {
						"type": "appkit.exsignitem",
						"cid": i,
						"pid": 2,
						"auto_select": "false",
						"selectable": "no",
						"force_display_in_property_view": "no",
						"has_global_content": "no",
						"need_server_process_component_data": "no",
						"is_new_created": "true",
						"property_view_title": "",
						"model": {
							"id": "",
							"class": "",
							"name": "",
							"index": i,
							"datasource": {
								"type": "api",
								"api_name": ""
							},
							"serial_count": args.get('prizes',{}).get('prize_item%d'%index,{}).get('serial_count',""),
							"serial_count_points": args.get('prizes',{}).get('prize_item%d'%index,{}).get('serial_count_points',"") ,
							"serial_count_prizes":args.get('prizes',{}).get('prize_item%d'%index,{}).get('serial_count_prizes',"")
						},
						"components": []
					}
			__inner_components.append(__components_tmp)

	__page_temple = {
		"type": "appkit.page",
		"cid": 1,
		"pid": "",
		"auto_select": "false",
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": "true",
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
			"site_title": "签到",
			"background": ""
		},
		"components": [
			{
				"type": "appkit.exsigndescription",
				"cid": 2,
				"pid": 1,
				"auto_select": "false",
				"selectable": "yes",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "签到",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 2,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"undefined": "",
					"title": args.get('sign_title',''),
					"description": args.get('sign_description',''),
					"image": args.get("share_pic",''),
					"share_description": args.get("share_description",""),
					"SignSettingGroupName": "",
					"daily_group": "",
					"daily_points": args.get('prizes',{}).get('prize_item0',{}).get('serial_count_points',""),
					"daily_prizes": args.get('prizes',{}).get('prize_item0',{}).get('serial_count_prizes',""),
					"items": __items
				},
				"components":__inner_components
			},
			{
				"type": "appkit.submitbutton",
				"cid": 3,
				"pid": 1,
				"auto_select": "false",
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
				"auto_select": "false",
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


def __get_ProjectId(context):
	"""
	获取当下条件下的Project_id，就是Page的_id
	"""
	exsign_args_response = __get_exsign(context)
	project_id = exsign_args_response['project_id']
	return project_id


def __get_DB_DynamicPages(project_id):
	"""
	直接从Mongo数据库取数据
	"""
	pagestore = pagestore_manager.get_pagestore('mongo')
	pages = pagestore.get_page_components(project_id)
	return pages

@when(u'{user}添加专项签到活动"{exsign_name}",并且保存')
def step_add_exsign(context,user,exsign_name):
	"""
	模拟登录签到PC页面，填写，保存
	"""
	project_id = '0'
	exsign_id = '0'
	#feature 数据
	exsign_json = json.loads(context.text)

	status = exsign_json.get('status',"")
	name = exsign_json.get('name',"")
	sign_describe = exsign_json.get('sign_describe',"")
	share = {
		"img":exsign_json.get("share_pic",""),
		"desc":exsign_json.get("share_describe","")
	}

	##Step1模拟登陆Sign页面 （Fin初始页面所有HTML元素）
	exsign_args_response = __get_exsign(context)

	exsign = exsign_args_response['exsign']
	is_create_new_data = exsign_args_response['is_create_new_data']
	project_id = exsign_args_response['project_id']
	webapp_owner_id = exsign_args_response['webapp_owner_id']

	##step2访问后台Phone页面 (Fin不是标准api请求，Phone页面HTML)
	__get_Termite(context,project_id,design_mode=1)
	##step3 获得Page右边个人配置JSON (Fin获得右边配置的空Json，这边主要是验证请求是否成功)
	dynamicPage_data = __get_DynamicPage(context,project_id)

	#step5 POST,PageJSON到Mongo,返回Page_id(Fin)

	##Page的数据处理
	prize_settings = {}#sign记录数据
	prize_settings_arr = []#page数据结构
	sign_settings = exsign_json.get("sign_settings","")
	for item in sign_settings:
		tmp_sign_in = item.get("sign_in","")
		tmp_integral = item.get("integral","")
		coupons = item.get("coupons","")
		tmp_prize_settings_arr = {}

		if tmp_sign_in:
			prize_settings[tmp_sign_in] = {}
			tmp_prize_settings_arr["serial_count"] = tmp_sign_in
			if tmp_integral:
				prize_settings[tmp_sign_in]["integral"] = tmp_integral
				tmp_prize_settings_arr["serial_count_points"] = tmp_integral
			else:
				prize_settings[tmp_sign_in]["integral"] = 0

			if coupons:
				tmp_prize_settings_arr["serial_count_prizes"] ={}
				prize_settings[tmp_sign_in]["coupon"] = __get_coupon_member_grade_json(coupons)

				tmp_prize_settings_arr["serial_count_prizes"] = __get_coupon_member_grade_json(coupons)
			else:
				prize_settings[tmp_sign_in]["coupon"] = []

		else:
			pass
		prize_settings_arr.append(tmp_prize_settings_arr)
	page_prizes = {}#Page记录数据
	for i in range(len(prize_settings_arr)):
		item = prize_settings_arr[i]
		page_prizes["prize_item%d"%i]={
				"serial_count":prize_settings_arr[i]["serial_count"],
				"serial_count_points":prize_settings_arr[i].get("serial_count_points",0),
				"serial_count_prizes":prize_settings_arr[i].get("serial_count_prizes",[])
		}
	#Page的参数args
	page_args ={
		"sign_title":name,
		"sign_description":sign_describe,
		"share_pic":share.get('img',""),
		"share_description":share.get('desc',""),
		"prizes":page_prizes
	}

	termite_post_args={
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": __get_PageJson(page_args),
	}
	post_termite_response = __post_PageJson(context,termite_post_args,project_id,design_mode=0,version=1)
	page_related_id = json.loads(post_termite_response.content).get('data',{}).get('project_id',0)
	#step6 POST,填写JSON至Mongo，返回JSON(Fin)
	post_sign_args = {
		"name":name,
		"prize_settings":json.dumps(prize_settings),
		"share":json.dumps(share),
		"status":status,
		"related_page_id":page_related_id,
	}
	post_exsign_response = __post_ExSignArgs(context,post_sign_args,project_id,method="put",design_mode=0,version=1)

	#传递保留参数
	context.project_id = page_related_id
	context.json_page = __get_PageJson(page_args)
	context.exsign_id = post_exsign_response['data']['id']
	context.exsign = exsign
	context.webapp_owner_id = webapp_owner_id

@given(u'{user}添加专项签到活动"{sign_name}",并且保存')
def step_impl(context,user,sign_name):
	step_add_exsign(context,user,sign_name)

@when(u'{user}编辑专项签到活动,并且保存')
def step_impl(context,user):
	"""
	编辑签到活动
	"""
	webapp_owner_id = context.webapp_owner_id
	project_id = 'new_app:exsign:%s'%(context.project_id)
	sign_id = context.exsign_id
	sign = context.exsign
	json_page = context.json_page

	#feature 数据
	sign_json = json.loads(context.text)

	status = sign_json.get('status',"")
	name = sign_json.get('name',"")
	sign_describe = sign_json.get('sign_describe',"")
	share = {
		"img":sign_json.get("share_pic",""),
		"desc":sign_json.get("share_describe","")
	}

	##step2访问后台Phone页面 (Fin不是标准api请求，Phone页面HTML)
	__get_Termite(context,project_id,design_mode=1)
	##step3 获得Page右边个人配置JSON (Fin获得右边配置的空Json，这边主要是验证请求是否成功)
	dynamicPage_data = __get_DynamicPage(context,project_id)


	#step5 POST,PageJSON到Mongo,返回Page_id(Fin)

	##Page的数据处理
	prize_settings = {}#sign记录数据
	prize_settings_arr = []#page数据结构
	sign_settings = sign_json.get("sign_settings","")
	for item in sign_settings:
		tmp_sign_in = item.get("sign_in","")
		tmp_integral = item.get("integral","")
		coupons = item.get("coupons","")
		# tmp_prize_counts = item.get("prize_counts","")
		tmp_prize_settings_arr = {}

		if tmp_sign_in:
			prize_settings[tmp_sign_in] = {}
			tmp_prize_settings_arr["serial_count"] = tmp_sign_in
			if tmp_integral:
				prize_settings[tmp_sign_in]["integral"] = tmp_integral
				tmp_prize_settings_arr["serial_count_points"] = tmp_integral
			else:
				prize_settings[tmp_sign_in]["integral"] = 0

			if coupons:
				tmp_prize_settings_arr["serial_count_prizes"] ={}
				prize_settings[tmp_sign_in]["coupon"] = __get_coupon_member_grade_json(coupons)
				tmp_prize_settings_arr["serial_count_prizes"] = __get_coupon_member_grade_json(coupons)
			else:
				prize_settings[tmp_sign_in]["coupon"] = []

		else:
			pass
		prize_settings_arr.append(tmp_prize_settings_arr)
	page_prizes = {}#Page记录数据
	for i in range(len(prize_settings_arr)):
		item = prize_settings_arr[i]
		page_prizes["prize_item%d"%i]={
				"serial_count":prize_settings_arr[i]["serial_count"],
				"serial_count_points":prize_settings_arr[i].get("serial_count_points",0),
				"serial_count_prizes":prize_settings_arr[i].get("serial_count_prizes",[])
		}
	#Page的参数args
	page_args ={
		"sign_title":name,
		"sign_description":sign_describe,
		"share_pic":share.get('img',""),
		"share_description":share.get('desc',""),
		"prizes":page_prizes
	}
	termite_post_args={
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": __get_PageJson(page_args),
	}
	post_termite_response = __post_PageJson(context,termite_post_args,project_id,design_mode=0,version=1)
	#step6 POST,填写JSON至Mongo，返回JSON(Fin)
	post_sign_args = {
		"name":name,
		"prize_settings":json.dumps(prize_settings),
		"share":json.dumps(share),
		"status":status,
		"related_page_id":context.project_id,
		"exsignId": context.exsign_id
	}
	post_sign_response = __post_ExSignArgs(context,post_sign_args,project_id,design_mode=0,version=1)
	context.json_page = __get_PageJson(page_args)


@then(u'{user}获得专项签到活动"{sign_name}"')
def step_impl(context,user,sign_name):
	"""
	feature数据生成Page，与数据库Page比较
	"""
	# feature数据
	if context.text:
		sign_json = json.loads(context.text)

	else:
		sign_json = {}

	status = sign_json.get('status',"")
	name = sign_json.get('name',"")
	sign_describe = sign_json.get('sign_describe',"")
	share = {
		"img":sign_json.get("share_pic",""),
		"desc":sign_json.get("share_describe","")
	}

	# 方案1：核对Page
	# 问题：模板组建的变化，也许需要更改组件
	# 发现一个坑，python中的True在Mongo中被保存为'true'，需要在字典中手动修改
	# 尝试自己写增强的判断函数，连带着各种麻烦，在这里留个戳，告诉后来人
	json_page = json.loads(context.json_page) #dict
	db_page = __get_DB_DynamicPages(context.project_id)[0]#永远是list第一项dict型

	if db_page["is_new_created"]:
		db_page["is_new_created"] = "true"
	else:
		db_page["is_new_created"] = "false"
	bdd_util.assert_dict(json_page,db_page)


@when(u'{user}更新专项签到活动的状态')
def update_sign_status(context,user):
	text = json.loads(context.text)
	if context.text:
		value = text.get("status","off")

	project_id = u'new_app:exsign:'+str(context.project_id)
	exsign_id = str(context.exsign_id)
	args = {
		"exsignId": exsign_id,
		"status": value
	}
	post_response = __post_ExSignArgs(context,args,project_id)
	context.exsign_id = exsign_id


@when(u'{user}离开专项签到活动"{sign_name}"')
def step_impl(context,user,sign_name):
	pass


@then(u'{user}的专项签到活动"{sign_name}"状态为"{sign_tag}"')
def step_impl(context,user,sign_name,sign_tag):
	status2name = {
		u'开启':1,
		u'关闭':0
	}
	exsign_id = context.exsign_id
	db_sign = exSign.objects(id=exsign_id)[0]

	sign_status = {'status': status2name[sign_tag]}
	db_status = {'status': db_sign['status']}
	bdd_util.assert_dict(sign_status,db_sign)

@then(u"{user}获得会员专项签到统计列表")
def step_impl(context, user):
	#更改所有参与者的最后一次签到时间
	if context.need_change_date:
		__change_all_member_last_sign_time(context)
		context.need_change_date = False

	design_mode = 0
	count_per_page = 10
	version = 1
	page = 1
	enable_paginate = 1
	participant_name = u''
	#分页情况，更新分页参数
	if hasattr(context,"paging"):
		paging_dic = context.paging
		count_per_page = paging_dic['count_per_page']
		page = paging_dic['page_num']
	if hasattr(context,"filter"):
		participant_name = context.filter["name"]
	url ='/apps/exsign/api/exsign_participances/?design_mode=%s&version=%s&count_per_page=%s&page=%s&enable_paginate=%s&_method=get&id=%s&participant_name=%s' % (design_mode,version,count_per_page,page,enable_paginate,context.exsign_id,participant_name)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	context.participances = json.loads(response.content)
	participances = context.participances['data']['items']
	actual = []
	for p in participances:
		p_dict = OrderedDict()
		p_dict[u"name"] = p['participant_name']
		p_dict[u"last_sign"] = bdd_util.get_date_str(p['latest_date_f'])
		p_dict[u"total_sign"] = p['total_count']
		p_dict[u"continuous_sign"] = p['serial_count']
		p_dict[u"integral"] = p['total_integral']
		p_dict[u"coupon_num"] = p['coupon_count']
		actual.append((p_dict))
	print("actual_data: {}".format(actual))
	expected = []
	if context.table:
		for row in context.table:
			cur_p = row.as_dict()
			if cur_p[u'last_sign']:
				cur_p[u'last_sign'] = bdd_util.get_date_str(cur_p[u'last_sign'])
			expected.append(cur_p)
	else:
		expected = json.loads(context.text)
	print("expected: {}".format(expected))

	bdd_util.assert_list(expected, actual)

#更改所有参与者的最后一次签到时间
def __change_all_member_last_sign_time(context):
	signParticipance = exSignParticipance.objects(belong_to=context.exsign_id)
	member_ids = []
	for data in signParticipance:
		member_ids.append(data.member_id)
	member_id2participance = exSignParticipance.objects(member_id__in=member_ids)
	members = member_models.Member.objects.filter(id__in=member_ids)
	member_id2member = {member.id: member for member in members}
	for member in member_id2participance:
		username = member_id2member[member.member_id].username_for_html
		latest_date = context.latest_date[username]
		member.update(set__latest_date = latest_date)

@when(u"{user}访问专项签到统计第'{page_num}'页")
def step_impl(context,user,page_num):
	count_per_page = context.count_per_page
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问专项签到统计列表下一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])+1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问专项签到统计列表上一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])-1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
