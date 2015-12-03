#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule
from weixin.message.material import models as material_models
from apps.customerized_apps.lottery import models as lottery_models
import termite.pagestore as pagestore_manager
import json

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


def __get_lotteryPageJson(args):
	"""
	传入参数，获取模板
	"""
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
			"site_title": "微信抽奖",
			"background": ""
		},
		"components": [
			{
				"type": "appkit.lotterydescription",
				"cid": 2,
				"pid": 1,
				"auto_select": False,
				"selectable": "yes",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "微信抽奖",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 2,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"title": args['title'],
					"start_time": args['start_time'],
					"end_time": args['end_time'],
					"valid_time": args['valid_time'],
					"description": args['description'],
					"expend": args['expend'],
					"delivery": args['delivery'],
					"delivery_setting": args['delivery_setting'],
					"limitation": args['limitation'],
					"chance": args['chance'],
					"allow_repeat": args['allow_repeat'],
					"items": [
						4,
						5,
						6
					]
				},
				"components": [
					{
						"type": "appkit.lotteryitem",
						"cid": 4,
						"pid": 2,
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
							"index": 3,
							"datasource": {
								"type": "api",
								"api_name": ""
							},
							"title": "一等奖",
							"prize_count": args['prize_settings'][0]['prize_count'],
							"prize": args['prize_settings'][0]['prize'],
							"image": args['prize_settings'][0]['image']
						},
						"components": []
					},
					{
						"type": "appkit.lotteryitem",
						"cid": 5,
						"pid": 2,
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
							"index": 3,
							"datasource": {
								"type": "api",
								"api_name": ""
							},
							"title": "二等奖",
							"prize_count": args['prize_settings'][1]['prize_count'],
							"prize": args['prize_settings'][1]['prize'],
							"image": args['prize_settings'][1]['image']
						},
						"components": []
					},
					{
						"type": "appkit.lotteryitem",
						"cid": 6,
						"pid": 2,
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
							"index": 3,
							"datasource": {
								"type": "api",
								"api_name": ""
							},
							"title": "三等奖",
							"prize_count": args['prize_settings'][2]['prize_count'],
							"prize": args['prize_settings'][2]['prize'],
							"image": args['prize_settings'][2]['image']
						},
						"components": []
					}
				]
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
			}
		]
	}
	return json.dumps(__page_temple)

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

# def __date_delta(start,end):
# 	"""
# 	获得日期，相差天数，返回int
# 	格式：
# 		start:(str){2015-11-23}
# 		end :(str){2015-11-30}
# 	"""
# 	start = dt.datetime.strptime(start, "%Y-%m-%d").date()
# 	end = dt.datetime.strptime(end, "%Y-%m-%d").date()
# 	return (end-start).days

def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
	return p_time

def __datetime2str(dt_time):
	"""
	datetime型数据，转为字符串型，日期
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
	return dt_time

def __limit2name(limit):
	"""
	传入积分规则，返回名字
	"""
	limit_dic={
	"once_per_user":u"一人一次",
	"once_per_day":u"一天一次",
	"twice_per_day":u"一天两次",
	"no_limit":u"不限"
	}
	if limit:
		return limit_dic[limit]
	else:
		return ""

def __name2limit(name):
	"""
	传入积分名字，返回积分规则
	"""
	name_dic={
		u"一人一次":"once_per_user",
		u"一天一次":"once_per_day",
		u"一天两次":"twice_per_day",
		u"不限":"no_limit"
	}
	if name:
		return name_dic[name]
	else:
		return ""

def __name2type(name):
	type_dic = {
		u"积分":"integral",
		u"优惠券":"coupon",
		u"实物":"entity"
	}
	if name:
		return type_dic[name]
	else:
		return ""

def __delivery2Bool(name):
	d_dic ={
		u"所有用户":"false",
		u'仅限未中奖用户':"true"
	}

	if name:
		return d_dic[name]
	else:
		return ""

def __get_coupon_json(coupon_rule_name):
	"""
	获取优惠券json
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
	coupon ={
		"id":coupon_rule.id,
		"count":coupon_rule.count,
		"name":coupon_rule.name
	}
	return coupon

def __get_coupon_rule_id(coupon_rule_name):
	"""
	获取优惠券id
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
	return coupon_rule.id

def __prize_settings_process(prize_settings):
	"""
	处理prize_settings

	Tag为page，返回page的prize字典
	Tage为lottery,返回lottery_lottery的prize字典
	"""

	page_prize_list = []
	lottery_prize_list = []

	if prize_settings:
		index = 0
		plist = [u'一等奖',u'二等奖',u'三等奖']
		for prize_setting in prize_settings:
			#Page
			page_prize_dic = {}
			page_prize_dic['title'] = prize_setting.get("prize_grade","")
			page_prize_dic['prize_count'] = prize_setting.get("prize_counts","")
			page_prize_dic['image'] = prize_setting.get("pic","")

			page_prize_dic['prize'] = {}
			prize_type = __name2type(prize_setting.get("prize_type"))
			if prize_type == "integral":
				prize_data = prize_setting.get("integral")
			elif prize_type == "coupon":
				coupon_name = prize_setting.get("coupon")
				coupon_id = __get_coupon_rule_id(coupon_name)
				prize_data = {
					"id":coupon_id,
					"name":coupon_name
				}
			elif prize_type == "entity":
				prize_data = prize_setting.get("gift","")
			else:
				prize_data = ""
			page_prize_dic['prize']["type"] = prize_type
			page_prize_dic['prize']["data"] = prize_data

			page_prize_list.append(page_prize_dic)

			#lottery_lottery
			lottery_prize_dic = {}
			lottery_prize_dic[plist[index]] = {
				"title":prize_setting.get("title",""),
				"prize_count":prize_setting.get("prize_counts",""),
				"prize_type":prize_type,
				"prize_data":prize_data
			}
			index += 1

		return (page_prize_list,lottery_prize_dic)
	else:
		return []

def __lottery_name2id(name):
	"""
	给抽奖项目的名字，返回id元祖
	返回（related_page_id,lottery_lottery中id）
	"""
	obj = lottery_models.lottery.objects.get(name=name)
	return (obj.related_page_id,obj.id)

# def __status2name(status_num):
# 	"""
# 	抽奖：状态值 转 文字
# 	"""
# 	status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
# 	return status2name_dic[status_num]

# def __name2status(name):
# 	"""
# 	抽奖： 文字 转 状态值
# 	"""
# 	if name:
# 		name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
# 		return name2status_dic[name]
# 	else:
# 		return -1


def __get_actions(status):
	"""
	根据输入抽奖状态
	返回对于操作列表
	"""
	actions_list = [u"查看结果",u"预览"]
	if status == u"已结束":
		actions_list.insert(1,u"删除")
	elif status=="进行中" or "未开始":
		actions_list.insert(1,u"关闭")
	return actions_list


##从这里开始，从头找
def __Create_Lottery(context,text,user):
	"""
	模拟用户登录页面
	创建抽奖项目
	写入mongo表：
		1.lottery_lottery表
		2.page表
	"""

	design_mode = 0
	version = 1
	text = text

	title = text.get("name","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	desc = text.get('desc','')#描述
	reduce_integral = text.get('reduce_integral',0)#消耗积分
	send_integral = text.get('send_integral',0)#参与送积分
	send_integral_rules = text.get('send_integral_rules',"")#送积分规则
	lottery_limit = __name2limit(text.get('lottery_limit',u'一人一次'))#抽奖限制
	win_rate = text.get('win_rate','0%').split('%')[0]#中奖率
	is_repeat_win = __name2Bool(text.get('is_repeat_win',"true"))#重复中奖
	expect_prize_settings_list = text.get('prize_settings',[])
	page_prize_settings,lottery_prize_settings = __prize_settings_process(expect_prize_settings_list)

	page_args = {
		"title":title,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"description":desc,#描述
		"expend":reduce_integral,#消耗积分
		"delivery":send_integral,#参与送积分
		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
		"limitation":lottery_limit,#抽奖限制
		"chance":win_rate,#中奖率
		"allow_repeat":is_repeat_win,#重复中奖
		"prize_settings":page_prize_settings
	}
	#step1：登录页面，获得分配的project_id
	get_lottery_response = context.client.get("/apps/lottery/lottery/")
	lottery_args_response = get_lottery_response.context
	project_id = lottery_args_response['project_id']#(str){new_app:lottery:0}

	#step2: 编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	dynamic_response = context.client.get(dynamic_url)
	dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

	#step3:发送Page
	page_json = __get_lotteryPageJson(page_args)

	termite_post_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}
	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_termite_response = context.client.post(termite_url,termite_post_args)
	related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

	#step4:发送lottery_args
	post_lottery_args = {
		"_method":"put",
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"expend":reduce_integral,#消耗积分
		"delivery":send_integral,#参与送积分
		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
		"limitation":lottery_limit,#抽奖限制
		"chance":win_rate,#中奖率
		"allow_repeat":is_repeat_win,#重复中奖
		"prize_settings":lottery_prize_settings,
		"related_page_id":related_page_id
	}
	lottery_url ="/apps/lottery/api/lottery/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_lottery_response = context.client.post(lottery_url,post_lottery_args)

def __Update_Lottery(context,text,page_id,lottery_id):
	"""
	模拟用户登录页面
	编辑抽奖项目
	写入mongo表：
		1.lottery_lottery表
		2.page表
	"""

	design_mode=0
	version=1
	project_id = "new_app:lottery:"+page_id

	title = text.get("name","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	desc = text.get('desc','')#描述
	reduce_integral = text.get('reduce_integral',0)#消耗积分
	send_integral = text.get('send_integral',0)#参与送积分
	send_integral_rules = text.get('send_integral_rules',"")#送积分规则
	lottery_limit = __name2limit(text.get('lottery_limit',u'一人一次'))#抽奖限制
	win_rate = text.get('win_rate','0%').split('%')[0]#中奖率
	is_repeat_win = __name2Bool(text.get('is_repeat_win',"true"))#重复中奖
	expect_prize_settings_list = text.get('prize_settings',[])
	page_prize_settings,lottery_prize_settings = __prize_settings_process(expect_prize_settings_list)


	page_args = {
		"title":title,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"description":desc,#描述
		"expend":reduce_integral,#消耗积分
		"delivery":send_integral,#参与送积分
		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
		"limitation":lottery_limit,#抽奖限制
		"chance":win_rate,#中奖率
		"allow_repeat":is_repeat_win,#重复中奖
		"prize_settings":page_prize_settings
	}

	page_json = __get_lotteryPageJson(page_args)

	update_page_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}

	update_lottery_args = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"expend":reduce_integral,#消耗积分
		"delivery":send_integral,#参与送积分
		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
		"limitation":lottery_limit,#抽奖限制
		"chance":win_rate,#中奖率
		"allow_repeat":is_repeat_win,#重复中奖
		"prize_settings":lottery_prize_settings,
		"id":lottery_id#updated的差别
	}


	#page 更新Page
	update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_page_response = context.client.post(update_page_url,update_page_args)

	#step4:更新lottery
	update_lottery_url ="/apps/lottery/api/lottery/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_lottery_response = context.client.post(update_lottery_url,update_lottery_args)

def __Delete_Lottery(context,lottery_id):
	"""
	删除抽奖活动
	写入mongo表：
		1.lottery_lottery表

	注释：page表在原后台，没有被删除
	"""
	design_mode = 0
	version = 1
	del_lottery_url = "/apps/lottery/api/lottery/?design_mode={}&version={}".format(design_mode,version)
	del_args ={
		"id":lottery_id,
		"_method":'delete'
	}
	del_lottery_response = context.client.post(del_lottery_url,del_args)
	return del_lottery_response

# def __Stop_Lottery(context,lottery_id):
# 	"""
# 	关闭抽奖活动
# 	"""

# 	design_mode = 0
# 	version = 1
# 	stop_lottery_url = "/apps/lottery/api/lottery_status/?design_mode={}&version={}".format(design_mode,version)
# 	stop_args ={
# 		"id":lottery_id,
# 		"target":'stoped'
# 	}
# 	stop_lottery_response = context.client.post(stop_lottery_url,stop_args)
# 	return stop_lottery_response

# def __Search_Lottery(context,search_dic):
# 	"""
# 	搜索抽奖活动

# 	输入搜索字典
# 	返回数据列表
# 	"""

# 	design_mode = 0
# 	version = 1
# 	page = 1
# 	enable_paginate = 1
# 	count_per_page = 10

# 	name = search_dic["name"]
# 	start_time = search_dic["start_time"]
# 	end_time = search_dic["end_time"]
# 	status = __name2status(search_dic["status"])



# 	search_url = "/apps/lottery/api/lotterys/?design_mode={}&version={}&name={}&status={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
# 			design_mode,
# 			version,
# 			name,
# 			status,
# 			start_time,
# 			end_time,
# 			count_per_page,
# 			page,
# 			enable_paginate)

# 	search_response = context.client.get(search_url)
# 	bdd_util.assert_api_call_success(search_response)
# 	return search_response

# def __Search_Lottery_Result(context,search_dic):
# 	"""
# 	搜索,抽奖参与结果

# 	输入搜索字典
# 	返回数据列表
# 	"""

# 	design_mode = 0
# 	version = 1
# 	page = 1
# 	enable_paginate = 1
# 	count_per_page = 10

# 	id = search_dic["id"]
# 	participant_name = search_dic["participant_name"]
# 	start_time = search_dic["start_time"]
# 	end_time = search_dic["end_time"]



# 	search_url = "/apps/lottery/api/lottery_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
# 			design_mode,
# 			version,
# 			id,
# 			participant_name,
# 			start_time,
# 			end_time,
# 			count_per_page,
# 			page,
# 			enable_paginate)

# 	search_response = context.client.get(search_url)
# 	bdd_util.assert_api_call_success(search_response)
# 	return search_response



@when(u'{user}新建微信抽奖活动')
def step_impl(context,user):
	text_list = json.loads(context.text)
	for text in text_list:
		__Create_Lottery(context,text,user)

@then(u'{user}获得微信抽奖活动列表')
def step_impl(context,user):
	design_mode = 0
	count_per_page = 10
	version = 1
	page = 1
	enable_paginate = 1

	actual_list = []
	expected = json.loads(context.text)

	#搜索查看结果
	if hasattr(context,"search_lottery"):
		pass
		# rec_search_list = context.search_lottery
		# for item in rec_search_list:
		# 	tmp = {
		# 		"name":item['name'],
		# 		"status":item['status'],
		# 		"start_time":item['start_time'],
		# 		"end_time":item['end_time'],
		# 		"participant_count":item['participant_count'],
		# 		"total_lottery_value":item['total_power']
		# 	}
		# 	tmp["actions"] = __get_actions(item['status'])
		# 	actual_list.append(tmp)

		# for expect in expected:
		# 	if 'start_date' in expect:
		# 		expect['start_time'] = __date2time(expect['start_date'])
		# 		del expect['start_date']
		# 	if 'end_date' in expect:
		# 		expect['end_time'] = __date2time(expect['end_date'])
		# 		del expect['end_date']
		# print("expected: {}".format(expected))

		# bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
	#其他查看结果
	else:
		#分页情况，更新分页参数
		# if hasattr(context,"paging"):
		# 	paging_dic = context.paging
		# 	count_per_page = paging_dic['count_per_page']
		# 	page = paging_dic['page_num']

		for expect in expected:
			if 'start_date' in expect:
				expect['start_time'] = __date2time(expect['start_date'])
				del expect['start_date']
			if 'end_date' in expect:
				expect['end_time'] = __date2time(expect['end_date'])
				del expect['end_date']


		print("expected: {}".format(expected))

		rec_lottery_url ="/apps/lottery/api/lotteries/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
		rec_lottery_response = context.client.get(rec_lottery_url)
		rec_lottery_list = json.loads(rec_lottery_response.content)['data']['items']#[::-1]

		for item in rec_lottery_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":__date2time(item['start_time']),
				"end_time":__date2time(item['end_time']),
				"participant_count":item['participant_count'],
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)


@when(u"{user}编辑微信抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	expect = json.loads(context.text)[0]
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	__Update_Lottery(context,expect,lottery_page_id,lottery_id)


@then(u"{user}获得微信抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	expect = json.loads(context.text)[0]

	title = expect.get("name","")

	cr_start_date = expect.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = expect.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	desc = expect.get('desc','')#描述
	reduce_integral = expect.get('reduce_integral',0)#消耗积分
	send_integral = expect.get('send_integral',0)#参与送积分
	send_integral_rules = expect.get('send_integral_rules',"")#送积分规则
	lottery_limit = __name2limit(expect.get('lottery_limit',u'一人一次'))#抽奖限制
	win_rate = expect.get('win_rate','0%').split('%')[0]#中奖率
	is_repeat_win = __name2Bool(expect.get('is_repeat_win',"true"))#重复中奖
	expect_prize_settings_list = expect.get('prize_settings',[])
	page_prize_settings,lottery_prize_settings = __prize_settings_process(expect_prize_settings_list)


	obj = lottery_models.lottery.objects.get(name=lottery_name)#纯数字
	related_page_id = obj.related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_component = page['component']['components'][0]['components']

	expect_lottery_dic = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"expend":reduce_integral,#消耗积分
		"delivery":send_integral,#参与送积分
		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
		"limitation":lottery_limit,#抽奖限制
		"chance":win_rate,#中奖率
		"allow_repeat":is_repeat_win,#重复中奖
		"prize_settings":page_prize_settings
	}


	actual_prize_list=[]
	for comp in page_component:
		actual_prize_dic={}
		actual_prize_dic['title'] = comp['model']['title']
		actual_prize_dic['prize_count'] = comp['model']['prize_count']
		actual_prize_dic['image'] = comp['model']['image']
		actual_prize_dic['prize'] = {
			"type":comp['model']['prize']['type'],
			"data":comp['model']['prize']['data']
		}
		actual_prize_list.append(actual_prize_dic)

	actual_lottery_dic = {
		"name": obj.name,
		"start_time":__datetime2str(obj.start_time),
		"end_time":__datetime2str(obj.end_time),
		"expend":obj.expend,#消耗积分
		"delivery":obj.delivery,#参与送积分
		"delivery_setting":obj.delivery_setting,#送积分规则
		"limitation":obj.limitation,#抽奖限制
		"chance":obj.chance,#中奖率
		"allow_repeat":obj.allow_repeat,#重复中奖
		"prize_settings":actual_prize_list,
	}

	__debug_print(expect_lottery_dic)
	__debug_print(actual_lottery_dic)
	bdd_util.assert_dict(expect_lottery_dic, actual_lottery_dic)

@when(u"{user}删除微信抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	del_response = __Delete_Lottery(context,lottery_id)
	bdd_util.assert_api_call_success(del_response)


# @when(u"{user}关闭抽奖活动'{lottery_name}'")
# def step_impl(context,user,lottery_name):
# 	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
# 	stop_response = __Stop_Lottery(context,lottery_id)
# 	bdd_util.assert_api_call_success(stop_response)


# @when(u"{user}查看抽奖活动'{lottery_name}'")
# def step_impl(context,user,lottery_name):
# 	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
# 	url ='/apps/lottery/api/lottery_participances/?_method=get&id=%s' % (lottery_id)
# 	url = bdd_util.nginx(url)
# 	response = context.client.get(url)
# 	context.participances = json.loads(response.content)
# 	context.lottery_id = "%s"%(lottery_id)

# @then(u"{webapp_user_name}获得抽奖活动'{power_me_rule_name}'的结果列表")
# def step_tmpl(context, webapp_user_name, power_me_rule_name):
# 	if hasattr(context,"search_lottery_result"):
# 		participances = context.search_lottery_result
# 	else:
# 		participances = context.participances['data']['items']
# 	actual = []
# 	print(participances)
# 	for p in participances:
# 		p_dict = OrderedDict()
# 		p_dict[u"rank"] = p['ranking']
# 		p_dict[u"member_name"] = p['username']
# 		p_dict[u"lottery_value"] = p['power']
# 		p_dict[u"parti_time"] = bdd_util.get_date_str(p['created_at'])
# 		actual.append((p_dict))
# 	print("actual_data: {}".format(actual))
# 	expected = []
# 	if context.table:
# 		for row in context.table:
# 			cur_p = row.as_dict()
# 			if cur_p[u'parti_time']:
# 				cur_p[u'parti_time'] = bdd_util.get_date_str(cur_p[u'parti_time'])
# 			expected.append(cur_p)
# 	else:
# 		expected = json.loads(context.text)
# 	print("expected: {}".format(expected))

# 	bdd_util.assert_list(expected, actual)

# @when(u"{user}设置抽奖活动列表查询条件")
# def step_impl(context,user):
# 	expect = json.loads(context.text)
# 	if 'start_date' in expect:
# 		expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
# 		del expect['start_date']

# 	if 'end_date' in expect:
# 		expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
# 		del expect['end_date']

# 	search_dic = {
# 		"name": expect.get("name",""),
# 		"start_time": expect.get("start_time",""),
# 		"end_time": expect.get("end_time",""),
# 		"status": expect.get("status",u"全部")
# 	}
# 	search_response = __Search_Lottery(context,search_dic)
# 	lottery_array = json.loads(search_response.content)['data']['items']
# 	context.search_lottery = lottery_array

# @when(u"{user}访问抽奖活动列表第'{page_num}'页")
# def step_impl(context,user,page_num):
# 	count_per_page = context.count_per_page
# 	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}访问抽奖活动列表下一页")
# def step_impl(context,user):
# 	paging_dic = context.paging
# 	count_per_page = paging_dic['count_per_page']
# 	page_num = int(paging_dic['page_num'])+1
# 	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}访问抽奖活动列表上一页")
# def step_impl(context,user):
# 	paging_dic = context.paging
# 	count_per_page = paging_dic['count_per_page']
# 	page_num = int(paging_dic['page_num'])-1
# 	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}设置抽奖活动结果列表查询条件")
# def step_impl(context,user):
# 	expect = json.loads(context.text)

# 	if 'parti_start_time' in expect:
# 		expect['start_time'] = __date2time(expect['parti_start_time']) if expect['parti_start_time'] else ""
# 		del expect['parti_start_time']

# 	if 'parti_end_time' in expect:
# 		expect['end_time'] = __date2time(expect['parti_end_time']) if expect['parti_end_time'] else ""
# 		del expect['parti_end_time']

# 	id = context.lottery_id
# 	participant_name = expect.get("member_name","")
# 	start_time = expect.get("start_time","")
# 	end_time = expect.get("end_time","")

# 	search_dic = {
# 		"id":id,
# 		"participant_name":participant_name,
# 		"start_time":start_time,
# 		"end_time":end_time
# 	}
# 	search_response = __Search_Lottery_Result(context,search_dic)
# 	lottery_result_array = json.loads(search_response.content)['data']['items']
# 	context.search_lottery_result = lottery_result_array

# @then(u"{user}能批量导出抽奖活动'{lottery_name}'")
# def step_impl(context,user,lottery_name):
# 	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
# 	url ='/apps/lottery/api/lottery_participances_export/?_method=get&export_id=%s' % (lottery_id)
# 	url = bdd_util.nginx(url)
# 	response = context.client.get(url)
# 	bdd_util.assert_api_call_success(response)