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
from apps.customerized_apps.vote import models as vote_models
import termite.pagestore as pagestore_manager
import json
import copy

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

def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
	return p_time

def __date2str(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_time = "{}".format(bdd_util.get_date_str(cr_date))
	return p_time

def __datetime2str(dt_time):
	"""
	datetime型数据，转为字符串型，日期
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
	return dt_time


def name2permission(name):
	name_dic={u"必须关注才可参与":"member",u"无需关注即可参与":"no_member"}
	if name:
		return name_dic[name]
	else:
		return None

def name2picshow_type(name):
	name_dic = {u"列表":"list",u"表格":"table"}
	if name:
		return name_dic[name]
	else:
		return None

def name2selection_type(name):
	name_dic = {u"单选":"single",u"多选":"multi"}
	if name:
		return name_dic[name]
	else:
		return None

# # def __limit2name(limit):
# # 	"""
# # 	传入积分规则，返回名字
# # 	"""
# # 	limit_dic={
# # 	"once_per_user":u"一人一次",
# # 	"once_per_day":u"一天一次",
# # 	"twice_per_day":u"一天两次",
# # 	"no_limit":u"不限"
# # 	}
# # 	if limit:
# # 		return limit_dic[limit]
# # 	else:
# # 		return ""

# # def __name2limit(name):
# # 	"""
# # 	传入积分名字，返回积分规则
# # 	"""
# # 	name_dic={
# # 		u"一人一次":"once_per_user",
# # 		u"一天一次":"once_per_day",
# # 		u"一天两次":"twice_per_day",
# # 		u"不限":"no_limit"
# # 	}
# # 	if name:
# # 		return name_dic[name]
# # 	else:
# # 		return ""

# # def __name2type(name):
# # 	type_dic = {
# # 		u"全部":"-1",
# # 		u"积分":"integral",
# # 		u"优惠券":"coupon",
# # 		u"实物":"entity",
# # 		u"未中奖":"no_prize"
# # 	}
# # 	if name:
# # 		return type_dic[name]
# # 	else:
# # 		return ""

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

def __vote_name2id(name):
	"""
	给投票项目的名字，返回id元祖
	返回（related_page_id,vote_vote中id）
	"""
	obj = vote_models.vote.objects.get(name=name)
	return (obj.related_page_id,obj.id)

# def __status2name(status_num):
# 	"""
# 	投票：状态值 转 文字
# 	"""
# 	status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
# 	return status2name_dic[status_num]

def __name2status(name):
	"""
	投票： 文字 转 状态值
	"""
	if name:
		name2status_dic = {u"所有投票":-1,u"未开始":0,u"进行中":1,u"已结束":2}
		return name2status_dic[name]
	else:
		return -1

# # def __name2coupon_status(name):
# # 	"""
# # 	投票： 文字 转 优惠券领取状态值
# # 	"""
# # 	if name:
# # 		name2status_dic = {u"全部":-1,u"未领取":0,u"已领取":1}
# # 		return name2status_dic[name]
# # 	else:
# # 		return -1

def __name2prize_type(name):
	name2prize_type_dic = {u"所有奖品":"all",u"优惠券":"coupon",u"积分":"integral"}

	if name:
		return name2prize_type_dic[name]
	else:
		return "all"

def __get_actions(status):
	"""
	根据输入投票状态
	返回对于操作列表
	"""
	actions_list = [u"链接",u"预览",u"统计",u"查看结果"]
	if status == u"进行中":
		actions_list.insert(0,u"关闭")
	elif status=="已结束" or "未开始":
		actions_list.insert(0,u"删除")
	return actions_list


def __name2textlist(itemName):
	itemName_dic={u"姓名":'name',u"手机":'phone',u"邮箱":'email',u"QQ号":'qq',u"QQ":'qq',u"qq":'qq',u"职位":"job",u"住址":"addr"}
	if itemName:
		return itemName_dic[itemName]
	else:
		return ""

def __get_votePageJson(args):
	"""
	传入参数，获取模板
	"""

	pid = "null"
	cid = 1
	index = 1

	next_pid = pid
	next_cid = cid
	next_index = index

	cur_pid = ""
	cur_cid = ""
	cur_index = ""


	#0.模板列表一览
	__page_temple = {}#总模板
	__votedescription_temple= {}#投票面板
	__submitbutton_temple = {}#提交按钮
	__componentadder_temple = {}#添加按钮
	__textselection_temple = {}#文本选项
	__imageselection_temple = {}#图片选项
	__textlist_temple = {}#快捷添加

	#1.主模板 pid:1
	__page_temple ={
		"type": "appkit.page",
		"cid": '',
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
			"index": "",
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"content_padding": "15px",
			"title": "index",
			"event:onload": "",
			"uploadHeight": "568",
			"uploadWidth": "320",
			"site_title": "微信投票",
			"background": ""
		},
		"components": []
	}


	cur_pid = next_pid#null
	cur_cid = next_cid#1
	cur_index = next_index#1

	next_pid = 1
	next_cid = cur_cid+1
	next_index = cur_index+1


	page_temple = __page_temple
	page_temple['pid'] = cur_pid
	page_temple['cid'] = cur_cid
	page_temple['model']['index'] = cur_index
	page_temple['components']= []



	#2.投票面板 pid:2

	__votedescription_temple = {
		"type": "appkit.surveydescription",
		"cid": '',
		"pid": '',
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"property_view_title": "投票简介",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": 1,
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"title": "",
			"subtitle": "",
			"description": "",
			"start_time": "",
			"end_time": "",
			"valid_time": "",
			"permission": "",
			"prize": ""
		},
		"components": []
	}


	cur_pid = next_pid
	cur_cid = next_cid
	cur_index = next_index

	next_pid = cur_pid
	next_cid = cur_cid+1
	next_index = cur_index+1

	vote_title = args["title"]
	vote_subtitle = args["subtitle"]
	vote_description = args["description"]
	vote_start_time = args["start_time"]
	vote_end_time = args["end_time"]
	vote_valid_time = args["valid_time"]
	vote_permission = name2permission(args["permission"])
	vote_prize = args["prize"]


	vote_temple = __votedescription_temple

	vote_temple['cid'] = cur_cid
	vote_temple['pid'] = cur_pid

	vote_temple['model']['index'] = cur_index
	vote_temple['model']['title'] = vote_title
	vote_temple['model']['subtitle'] = vote_subtitle
	vote_temple['model']['description'] = "<p>{}</p>".format(vote_description)
	vote_temple['model']['start_time'] = vote_start_time
	vote_temple['model']['end_time'] = vote_end_time
	vote_temple['model']['valid_time'] = vote_valid_time
	vote_temple['model']['permission'] = vote_permission
	vote_temple['model']['prize'] = vote_prize

	vote_temple['components']=[]

	page_temple['components'].append(vote_temple)

	#3.提交按钮(系统必需) pid:3
	__submitbutton_temple = {
			"type": "appkit.submitbutton",
			"cid": "",
			"pid": "",
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
				"index": "",
				"datasource": {
					"type": "api",
					"api_name": ""
				},
				"text": "提交"
			},
			"components": []
		}

	cur_pid = next_pid #1
	cur_cid = next_cid #3
	cur_index = next_index #3

	next_pid = cur_pid #1
	next_cid = cur_cid+1 #4
	next_index = cur_index+1 #4

	submitbutton_temple = __submitbutton_temple
	submitbutton_temple['pid'] = cur_pid
	submitbutton_temple['cid'] = cur_cid
	submitbutton_temple['model']['index'] = 100000+cur_pid #特殊对待
	submitbutton_temple['components']=[]

	page_temple['components'].append(submitbutton_temple)

	#4.添加柄(系统必需)  pid:4
	__componentadder_temple = {
			"type": "appkit.componentadder",
			"cid": "",
			"pid": "",
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
				"index": "",
				"datasource": {
					"type": "api",
					"api_name": ""
				},
				"components": ""
			},
			"components": []
		}

	cur_pid = next_pid #1
	cur_cid = next_cid #4
	cur_index = next_index #4

	next_pid = cur_pid #1
	next_cid = cur_cid+1 #5
	next_index = cur_index+1 #5

	componentadder_temple = __componentadder_temple
	componentadder_temple['pid'] = cur_pid
	componentadder_temple['cid'] = cur_cid
	componentadder_temple['model']['index'] = next_index #应该等于所有的部件数+1不知道这样子会影响不
	componentadder_temple['components']=[]

	page_temple['components'].append(componentadder_temple)

	#5.文本选项组件(用户自定义)  pid:5开始
	__textselection_temple = {
			"type": "appkit.textselection",
			"cid": "",
			"pid": "",
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
				"title": "11select",
				"type": "single",
				"is_mandatory": "true",
				"items":""
			},
			"components": ""
		}

	__textselectionitem_temple = {
			"type": "appkit.textselectionitem",
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
				"title": ""
			},
			"components": []
		}


	text_options_arr = args['text_options']
	next_index = next_index-2 #校准

	for text_options in text_options_arr:
		text_options_title = text_options['title']
		text_options_required = __name2Bool(text_options['is_required'])
		text_options_type = name2selection_type(text_options['type'])

		cur_pid = next_pid #1
		cur_cid = next_cid #5...
		cur_index = next_index #3...

		next_pid = cur_pid #1
		next_cid = cur_cid+1 #6...
		next_index = cur_index+1 #4...

		text_options_temple = {}
		text_options_temple =  copy.deepcopy(__textselection_temple)
		text_options_temple['pid'] = cur_pid
		text_options_temple['cid'] = cur_cid
		text_options_temple['model']['index'] = cur_index #校准顺序后4...
		text_options_temple['model']['title'] = text_options_title #校准顺序后4...
		text_options_temple['model']['type'] = text_options_type
		text_options_temple['model']['is_mandatory'] = text_options_required #校准顺序后4...
		text_options_temple['model']['items'] = []
		text_options_temple['components']=[]

		#内部
		selectionitem_arr = text_options['option']
		for selectionitem in selectionitem_arr:
			selectionitem_title = selectionitem['options']
			#内部的id处理
			sub_cur_pid = cur_cid #1
			cur_cid = next_cid #7...
			# cur_index = next_index

			# next_pid = cur_cid #1
			next_cid = cur_cid+1 #8...
			# next_index = cur_index+1 #6...

			selectionitem_temple = copy.deepcopy(__textselectionitem_temple)
			selectionitem_temple['pid'] = sub_cur_pid
			selectionitem_temple['cid'] = cur_cid
			selectionitem_temple['model']['index'] = cur_cid #与父同，内部组件

			selectionitem_temple['model']['title'] = selectionitem_title
			selectionitem_temple['components']=[]

			text_options_temple['model']['items'].append(cur_cid)
			text_options_temple['components'].append(selectionitem_temple)

		page_temple['components'].append(text_options_temple)


	#6图片选项模块(据有内置模块)

	__imageselection_temple = {
			"type": "appkit.imageselection",
			"cid": "",
			"pid": "",
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
				"disp_type": "",
				"is_mandatory": "",
				"items": []
			},
			"components": []
		}
	__imageitem_temple = {
					"type": "appkit.imageitem",
					"cid": "",
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
						"image": "",
						"title": ""
					},
					"components": []
				}


	imageselection_arr = args['pic_options']

	for imageselection in imageselection_arr:

		imageselection_title = imageselection['title']
		imageselection_type = name2selection_type(imageselection['type'])
		imageselection_showtype = name2picshow_type(imageselection['pic_show_type'])
		imageselection_required = __name2Bool(imageselection['is_required'])


		cur_pid = next_pid #1
		cur_cid = next_cid #7...
		cur_index = next_index #5...

		next_pid = cur_cid #1
		next_cid = cur_cid+1 #8...
		next_index = cur_index+1 #6...

		imageselection_temple = copy.deepcopy(__imageselection_temple)
		imageselection_temple['pid'] = cur_pid
		imageselection_temple['cid'] = cur_cid
		imageselection_temple['model']['index'] = cur_index
		imageselection_temple['model']['title'] = imageselection_title
		imageselection_temple['model']['type'] = imageselection_type
		imageselection_temple['model']['disp_type'] = imageselection_showtype
		imageselection_temple['model']['is_mandatory'] = imageselection_required
		imageselection_temple['model']['items']=[]#内部组件
		imageselection_temple['components']=[]#内部组件

		#内部拓展
		imageitem_arr = imageselection['option']
		for imageitem in imageitem_arr:

			imageitem_image = imageitem['pic']
			imageitem_title = imageitem['pic_desc']

			#内部的id处理
			sub_cur_pid = cur_cid #1
			cur_cid = next_cid #7...
			# cur_index = next_index

			# next_pid = cur_cid #1
			next_cid = cur_cid+1 #8...
			# next_index = cur_index+1 #6...


			imageitem_temple = copy.deepcopy(__imageitem_temple)
			imageitem_temple['pid'] = sub_cur_pid
			imageitem_temple['cid'] = cur_cid
			imageitem_temple['model']['index'] = cur_cid #与父同，内部组件

			imageitem_temple['model']['image'] = imageitem_image
			imageitem_temple['model']['title'] = imageitem_title
			imageitem_temple['components']=[]

			imageselection_temple['model']['items'].append(cur_cid)
			imageselection_temple['components'].append(imageitem_temple)

		page_temple['components'].append(imageselection_temple)


	#7快捷模块(用户自定义)

	__textlist_temple = {
			"type": "appkit.textlist",
			"cid": "",
			"pid": '',
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
		textlist_temple['pid'] = cur_pid
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
			# cur_index = next_index

			# next_pid = cur_cid #1
			next_cid = cur_cid+1 #8...
			# next_index = cur_index+1 #6...

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

def __prize_settings_process(prize_type,integral,coupon):
	"""
	处理prize_settings

	Tag为page，返回page的prize字典
	Tage为event,返回event_event的prize字典
	"""
	prize = {}

	if prize_type:
		if prize_type == "无奖励":
			prize = {"type":"no_prize","data":None}
		elif prize_type=="积分":
			prize = {"type":"integral","data":integral}
		elif prize_type == "优惠券":
			coupon_name = coupon
			coupon_id = __get_coupon_rule_id(coupon_name)
			prize = {"type":"coupon",
					 "data":{
						"id":coupon_id,
						"name":coupon_name
					 }
					}
		else:
			pass
	return prize

def __Create_Vote(context,text,user):
	"""
	模拟用户登录页面
	创建投票项目
	写入mongo表：
		1.vote_vote表
		2.page表
	"""
	design_mode = 0
	version = 1
	text = text

	title = text.get("title","")
	subtitle = text.get("subtitle","")
	description = text.get("content","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	permission = text.get("permission")

	prize_type = text.get("prize_type","")
	integral = text.get("integral","")
	coupon = text.get("coupon","")
	prize = __prize_settings_process(prize_type,integral,coupon)

	text_options = text.get("text_options","")
	pic_options = text.get("pic_options","")
	textlist = text.get("participate_info","")


	page_args = {
		"title":title,
		"subtitle":subtitle,
		"description":description,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"permission":permission,
		"prize":prize,
		"text_options":text_options,
		"pic_options":pic_options,
		"textlist":textlist
	}

	#step1：登录页面，获得分配的project_id
	get_vote_response = context.client.get("/apps/vote/vote/")
	vote_args_response = get_vote_response.context
	project_id = vote_args_response['project_id']#(str){new_app:vote:0}

	#step2: 编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	dynamic_response = context.client.get(dynamic_url)
	dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

	# #step3:发送Page
	page_json = __get_votePageJson(page_args)

	termite_post_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}
	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_termite_response = context.client.post(termite_url,termite_post_args)
	related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

	#step4:发送vote_args
	post_vote_args = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"related_page_id":related_page_id
	}
	vote_url ="/apps/vote/api/vote/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
	post_vote_response = context.client.post(vote_url,post_vote_args)

	#跳转,更新状态位
	design_mode = 0
	count_per_page = 1000
	version = 1
	page = 1
	enable_paginate = 1

	rec_vote_url ="/apps/vote/api/votes/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
	rec_vote_response = context.client.get(rec_vote_url)

def __Update_Vote(context,text,page_id,vote_id):
	"""
	模拟用户登录页面
	编辑投票项目
	写入mongo表：
		1.vote_vote表
		2.page表
	"""

	design_mode=0
	version=1
	project_id = "new_app:vote:"+page_id

	title = text.get("title","")
	subtitle = text.get("subtitle","")
	description = text.get("content","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	permission = text.get("permission")

	prize_type = text.get("prize_type","")
	integral = text.get("integral","")
	coupon = text.get("coupon","")
	prize = __prize_settings_process(prize_type,integral,coupon)

	text_options = text.get("text_options","")
	pic_options = text.get("pic_options","")
	textlist = text.get("participate_info","")


	page_args = {
		"title":title,
		"subtitle":subtitle,
		"description":description,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"permission":permission,
		"prize":prize,
		"text_options":text_options,
		"pic_options":pic_options,
		"textlist":textlist
	}


	page_json = __get_votePageJson(page_args)

	update_page_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}

	update_vote_args = {

		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"id":vote_id#updated的差别
	}


	#page 更新Page
	update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_page_response = context.client.post(update_page_url,update_page_args)

	#step4:更新vote
	update_vote_url ="/apps/vote/api/vote/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_vote_response = context.client.post(update_vote_url,update_vote_args)

	#跳转,更新状态位
	design_mode = 0
	count_per_page = 1000
	version = 1
	page = 1
	enable_paginate = 1

	rec_vote_url ="/apps/vote/api/votes/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
	rec_vote_response = context.client.get(rec_vote_url)

def __Delete_Vote(context,vote_id):
	"""
	删除投票活动
	写入mongo表：
		1.vote_vote表

	注释：page表在原后台，没有被删除
	"""
	design_mode = 0
	version = 1
	del_vote_url = "/apps/vote/api/vote/?design_mode={}&version={}&_method=delete".format(design_mode,version)
	del_args ={
		"id":vote_id
	}
	del_vote_response = context.client.post(del_vote_url,del_args)
	return del_vote_response

def __Stop_Vote(context,vote_id):
	"""
	关闭投票活动
	"""

	design_mode = 0
	version = 1
	stop_vote_url = "/apps/vote/api/vote_status/?design_mode={}&version={}".format(design_mode,version)
	stop_args ={
		"id":vote_id,
		"target":'stoped'
	}
	stop_vote_response = context.client.post(stop_vote_url,stop_args)
	return stop_vote_response

def __Search_Vote(context,search_dic):
	"""
	搜索投票活动

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	#分页情况，更新分页参数
	if hasattr(context,"paging"):
		paging_dic = context.paging
		count_per_page = paging_dic['count_per_page']
		page = paging_dic['page_num']


	name = search_dic["name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]
	status = search_dic["status"]
	prize_type = search_dic['prize_type']



	search_url = "/apps/vote/api/votes/?design_mode={}&version={}&name={}&status={}&prize_type={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
			design_mode,
			version,
			name,
			status,
			prize_type,
			start_time,
			end_time,
			count_per_page,
			page,
			enable_paginate)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response

# def __Search_Vote_Result(context,search_dic):
# 	"""
# 	搜索,投票参与结果

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

# 	search_url = "/apps/vote/api/vote_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
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

@when(u'{user}新建微信投票活动')
def step_impl(context,user):
	text_list = json.loads(context.text)
	for text in text_list:
		__Create_Vote(context,text,user)

@then(u'{user}获得微信投票活动列表')
def step_impl(context,user):
	design_mode = 0
	count_per_page = 10
	version = 1
	page = 1
	enable_paginate = 1

	actual_list = []
	expected = json.loads(context.text)

	#搜索查看结果
	if hasattr(context,"search_vote"):
		rec_search_list = context.search_vote
		for item in rec_search_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":item['start_time'],
				"end_time":item['end_time'],
				"prize_type":item['prize_type'],
				"participant_count":item['participant_count'],
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)

		for expect in expected:
			if 'start_date' in expect:
				expect['start_time'] = __date2time(expect['start_date'])
				del expect['start_date']
			if 'end_date' in expect:
				expect['end_time'] = __date2time(expect['end_date'])
				del expect['end_date']
		print("expected: {}".format(expected))

		bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
	#其他查看结果
	else:
		#分页情况，更新分页参数
		if hasattr(context,"paging"):
			paging_dic = context.paging
			count_per_page = paging_dic['count_per_page']
			page = paging_dic['page_num']

		for expect in expected:
			if 'start_date' in expect:
				expect['start_time'] = __date2time(expect['start_date'])
				del expect['start_date']
			if 'end_date' in expect:
				expect['end_time'] = __date2time(expect['end_date'])
				del expect['end_date']


		print("expected: {}".format(expected))

		rec_vote_url ="/apps/vote/api/votes/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
		rec_vote_response = context.client.get(rec_vote_url)
		rec_vote_list = json.loads(rec_vote_response.content)['data']['items']#[::-1]

		for item in rec_vote_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":__date2time(item['start_time']),
				"end_time":__date2time(item['end_time']),
				"participant_count":item['participant_count'],
				"prize_type":item['prize_type']
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)

@when(u"{user}编辑微信投票活动'{vote_name}'")
def step_impl(context,user,vote_name):
	expect = json.loads(context.text)[0]
	vote_page_id,vote_id = __vote_name2id(vote_name)#纯数字
	__Update_Vote(context,expect,vote_page_id,vote_id)

# # @then(u"{user}获得微信投票活动'{vote_name}'")
# # def step_impl(context,user,vote_name):
# # 	expect = json.loads(context.text)[0]

# # 	title = expect.get("name","")

# # 	cr_start_date = expect.get('start_date', u'今天')
# # 	start_date = bdd_util.get_date_str(cr_start_date)
# # 	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

# # 	cr_end_date = expect.get('end_date', u'1天后')
# # 	end_date = bdd_util.get_date_str(cr_end_date)
# # 	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

# # 	valid_time = "%s~%s"%(start_time,end_time)

# # 	desc = expect.get('desc','')#描述
# # 	reduce_integral = expect.get('reduce_integral',0)#消耗积分
# # 	send_integral = expect.get('send_integral',0)#参与送积分
# # 	send_integral_rules = expect.get('send_integral_rules',"")#送积分规则
# # 	vote_limit = __name2limit(expect.get('vote_limit',u'一人一次'))#投票限制
# # 	win_rate = expect.get('win_rate','0%').split('%')[0]#中奖率
# # 	is_repeat_win = __name2Bool(expect.get('is_repeat_win',"true"))#重复中奖
# # 	expect_prize_settings_list = expect.get('prize_settings',[])
# # 	page_prize_settings,vote_prize_settings = __prize_settings_process(expect_prize_settings_list)


# # 	obj = vote_models.vote.objects.get(name=vote_name)#纯数字
# # 	related_page_id = obj.related_page_id
# # 	pagestore = pagestore_manager.get_pagestore('mongo')
# # 	page = pagestore.get_page(related_page_id, 1)
# # 	page_component = page['component']['components'][0]['components']

# # 	expect_vote_dic = {
# # 		"name":title,
# # 		"start_time":start_time,
# # 		"end_time":end_time,
# # 		"expend":reduce_integral,#消耗积分
# # 		"delivery":send_integral,#参与送积分
# # 		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
# # 		"limitation":vote_limit,#投票限制
# # 		"chance":win_rate,#中奖率
# # 		"allow_repeat":is_repeat_win,#重复中奖
# # 		"prize_settings":page_prize_settings
# # 	}


# # 	actual_prize_list=[]
# # 	for comp in page_component:
# # 		actual_prize_dic={}
# # 		actual_prize_dic['title'] = comp['model']['title']
# # 		actual_prize_dic['prize_count'] = comp['model']['prize_count']
# # 		actual_prize_dic['image'] = comp['model']['image']
# # 		actual_prize_dic['prize'] = {
# # 			"type":comp['model']['prize']['type'],
# # 			"data":comp['model']['prize']['data']
# # 		}
# # 		actual_prize_list.append(actual_prize_dic)

# # 	actual_vote_dic = {
# # 		"name": obj.name,
# # 		"start_time":__datetime2str(obj.start_time),
# # 		"end_time":__datetime2str(obj.end_time),
# # 		"expend":obj.expend,#消耗积分
# # 		"delivery":obj.delivery,#参与送积分
# # 		"delivery_setting":obj.delivery_setting,#送积分规则
# # 		"limitation":obj.limitation,#投票限制
# # 		"chance":obj.chance,#中奖率
# # 		"allow_repeat":obj.allow_repeat,#重复中奖
# # 		"prize_settings":actual_prize_list,
# # 	}

# # 	bdd_util.assert_dict(expect_vote_dic, actual_vote_dic)

@when(u"{user}删除微信投票活动'{vote_name}'")
def step_impl(context,user,vote_name):
	vote_page_id,vote_id = __vote_name2id(vote_name)#纯数字
	del_response = __Delete_Vote(context,vote_id)
	bdd_util.assert_api_call_success(del_response)

@when(u"{user}关闭微信投票活动'{vote_name}'")
def step_impl(context,user,vote_name):
	vote_page_id,vote_id = __vote_name2id(vote_name)#纯数字
	stop_response = __Stop_Vote(context,vote_id)
	bdd_util.assert_api_call_success(stop_response)

@when(u"{user}设置微信投票活动列表查询条件")
def step_impl(context,user):
	expect = json.loads(context.text)
	if 'start_date' in expect:
		expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
		del expect['start_date']

	if 'end_date' in expect:
		expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
		del expect['end_date']

	search_dic = {
		"name": expect.get("name",""),
		"start_time": expect.get("start_time",""),
		"end_time": expect.get("end_time",""),
		"status": __name2status(expect.get("status",u"所有投票")),
		"prize_type":__name2prize_type(expect.get("prize_type",u"所有奖品"))
	}
	search_response = __Search_Vote(context,search_dic)
	vote_array = json.loads(search_response.content)['data']['items']
	context.search_vote = vote_array

@when(u"{user}访问微信投票活动列表第'{page_num}'页")
def step_impl(context,user,page_num):
	count_per_page = context.count_per_page
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问微信投票活动列表下一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])+1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问微信投票活动列表上一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])-1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

# @when(u"{user}查看微信投票活动'{vote_name}'")
# def check_vote_list(context,user,vote_name):
# 	design_mode = 0
# 	version = 1
# 	page = 1

# 	if hasattr(context,"enable_paginate"):
# 		enable_paginate = context.enable_paginate
# 	else:
# 		enable_paginate = 1
# 	if hasattr(context,"count_per_page"):
# 		count_per_page = context.count_per_page
# 	else:
# 		count_per_page = 10


# 	if hasattr(context,"paging"):
# 		paging_dic = context.paging
# 		count_per_page = paging_dic['count_per_page']
# 		page = paging_dic['page_num']

# 	vote_page_id,vote_id = __vote_name2id(vote_name)#纯数字
# 	url ='/apps/vote/api/vote_participances/?design_mode={}&version={}&id={}&count_per_page={}&page={}&enable_paginate={}&_method=get'.format(
# 			design_mode,
# 			version,
# 			vote_id,
# 			count_per_page,
# 			page,
# 			enable_paginate,
# 		)
# 	url = bdd_util.nginx(url)
# 	response = context.client.get(url)
# 	context.participances = json.loads(response.content)
# 	context.vote_id = "%s"%(vote_id)


# @then(u"{webapp_user_name}获得微信投票活动'{power_me_rule_name}'的结果列表")
# def step_tmpl(context, webapp_user_name, power_me_rule_name):

# 	if hasattr(context,"search_vote_result"):
# 		participances = context.search_vote_result
# 	else:
# 		participances = context.participances['data']['items']
# 	actual = []

# 	for p in participances:
# 		p_dict = OrderedDict()
# 		p_dict[u"member_name"] = p['participant_name']
# 		p_dict[u"vote_time"] = bdd_util.get_date_str(p['created_at'])
# 		actual.append((p_dict))
# 	print("actual_data: {}".format(actual))

# 	expected = []
# 	if context.table:
# 		for row in context.table:
# 			cur_p = row.as_dict()
# 			if cur_p[u'vote_time']:
# 				cur_p[u'vote_time'] = bdd_util.get_date_str(cur_p[u'vote_time'])
# 			expected.append(cur_p)
# 	else:
# 		expected = json.loads(context.text)
# 	print("expected: {}".format(expected))

# 	bdd_util.assert_list(expected, actual)
# 	context.participances = participances

# @when(u"{user}设置微信投票活动结果列表查询条件")
# def step_impl(context,user):
# 	expect = json.loads(context.text)

# 	if 'vote_start_time' in expect:
# 		expect['start_time'] = __date2time(expect['vote_start_time']) if expect['vote_start_time'] else ""
# 		del expect['vote_start_time']

# 	if 'vote_end_time' in expect:
# 		expect['end_time'] = __date2time(expect['vote_end_time']) if expect['vote_end_time'] else ""
# 		del expect['vote_end_time']

# 	print("expected: {}".format(expect))

# 	id = context.vote_id
# 	participant_name = expect.get("member_name","")
# 	start_time = expect.get("start_time","")
# 	end_time = expect.get("end_time","")

# 	search_dic = {
# 		"id":id,
# 		"participant_name":participant_name,
# 		"start_time":start_time,
# 		"end_time":end_time,
# 	}
# 	search_response = __Search_Vote_Result(context,search_dic)
# 	vote_result_array = json.loads(search_response.content)['data']['items']
# 	context.search_vote_result = vote_result_array

# @when(u"{user}访问微信投票活动'{vote_name}'的结果列表第'{page_num}'页")
# def step_impl(context,user,vote_name,page_num):
# 	count_per_page = context.count_per_page
# 	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
# 	check_vote_list(context,user,vote_name)

# @when(u"{user}访问微信投票活动'{vote_name}'的结果列表下一页")
# def step_impl(context,user,vote_name):
# 	paging_dic = context.paging
# 	count_per_page = paging_dic['count_per_page']
# 	page_num = int(paging_dic['page_num'])+1
# 	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
# 	check_vote_list(context,user,vote_name)

# @when(u"{user}访问微信投票活动'{vote_name}'的结果列表上一页")
# def step_impl(context,user,vote_name):
# 	paging_dic = context.paging
# 	count_per_page = paging_dic['count_per_page']
# 	page_num = int(paging_dic['page_num'])-1
# 	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
# 	check_vote_list(context,user,vote_name)

# # @then(u"{user}能批量导出投票活动'{vote_name}'")
# # def step_impl(context,user,vote_name):
# # 	vote_page_id,vote_id = __vote_name2id(vote_name)#纯数字
# # 	url ='/apps/vote/api/vote_participances_export/?_method=get&export_id=%s' % (vote_id)
# # 	url = bdd_util.nginx(url)
# # 	response = context.client.get(url)
# # 	bdd_util.assert_api_call_success(response)

# @when(u"{webapp_owner_name}访问用户'{webapp_user_name}'的查看结果")
# def step_impl(context,webapp_owner_name,webapp_user_name):
# 	participances = context.participances
# 	webapp_user_id = None
# 	for participance_dic in participances:
# 		if participance_dic['participant_name'] == webapp_user_name:
# 			webapp_user_id = participance_dic['id']

# 	url ='/apps/vote/api/vote_participance/?id={}'.format(
# 				webapp_user_id
# 			)
# 	url = bdd_util.nginx(url)
# 	response = context.client.get(url)
# 	participance = json.loads(response.content)['data']['items']
# 	context.participance_content = {"username":webapp_user_name,'participance':participance}


# @then(u"{webapp_owner_name}获得用户'{webapp_user_name}'的查看结果")
# def step_impl(context,webapp_owner_name,webapp_user_name):

# 	expect_order = []
# 	title_key = u"{}填写的内容".format(webapp_user_name)
# 	expect = json.loads(context.text)
# 	print("expect: {}".format(expect))


# 	#获得顺序
# 	for ex_dict in expect[title_key]:
# 		expect_order.append(ex_dict.keys()[0])



# 	participance_content = context.participance_content
# 	webapp_user_name = participance_content['username']
# 	participance = participance_content['participance']

# 	actual = {}
# 	actual[title_key] = []

# 	for item_name in expect_order:
# 		for parti in participance:
# 			parti_name = parti['item_name']
# 			parti_value = parti['item_value']
# 			if item_name == parti_name:
# 				tmp = {}
# 				tmp[parti_name] = parti_value
# 				actual[title_key].append(tmp)


# 	bdd_util.assert_dict(expect, actual)

# @when(u"{webapp_owner_name}访问微信投票活动'{vote_name}'的统计")
# def step_impl(context,webapp_owner_name,vote_name):

# 	vote = vote_models.vote.objects.get(name=vote_name)
# 	vote_id = vote.id
# 	related_page_id = vote.related_page_id

# 	url ="/apps/vote/vote_statistics/?id={}".format(vote_id)
# 	url = bdd_util.nginx(url)
# 	response = context.client.get(url)
# 	result_list =  response.context['titles']

# 	for appkit in result_list:
# 		if appkit['type'] == 'appkit.text_options':
# 			appkit_title = appkit['title_']
# 			appkit_url ="/apps/vote/api/question/?id={}&question_title={}".format(vote_id,appkit_title)
# 			appkit_url = bdd_util.nginx(appkit_url)
# 			appkit_response = context.client.get(appkit_url)
# 			appkit_list =  json.loads(appkit_response.content)['data']['items']
# 			appkit['values'] = appkit_list

# 		elif appkit['type'] == 'appkit.uploadimg':
# 			appkit_title = appkit['title_']
# 			appkit_url ="/apps/vote/api/question/?id={}&question_title={}".format(vote_id,appkit_title)
# 			appkit_url = bdd_util.nginx(appkit_url)
# 			appkit_response = context.client.get(appkit_url)
# 			appkit_list =  json.loads(appkit_response.content)['data']['items']
# 			appkit['values'] = appkit_list

# 	context.appkit_list = result_list

# @then(u"{webapp_owner_name}获得微信投票活动'{vote_name}'的统计结果")
# def step_impl(context,webapp_owner_name,vote_name):
# 	expect = json.loads(context.text)
# 	expect_title_order = [ ex['title'] for ex in expect]

# 	for ex_item in expect:
# 		for value_item in ex_item['values']:
# 			if 'submit_time' in value_item:
# 				value_item['submit_time'] = __date2str(value_item['submit_time'])
# 	print("expect: {}".format(expect))

# 	actual = []
# 	appkit_list = context.appkit_list
# 	for index in range(len(expect_title_order)):
# 		ex_title = expect_title_order[index]
# 		for appkit in appkit_list:
# 			__debug_print(appkit)
# 			if appkit['title'] == ex_title:
# 				if appkit['type'] == 'appkit.text_options':
# 					tmp = {}
# 					tmp['participate_count'] = appkit['count']
# 					tmp['title'] = appkit['title']
# 					tmp['type'] = appkit['title_type']
# 					tmp['values'] = []
# 					for value in appkit['values']:
# 						if 'created_at' in value:
# 							value['submit_time'] = value['created_at']
# 							del value['created_at']
# 						tmp['values'].append(value)
# 					actual.append(tmp)

# 				elif appkit['type'] == 'appkit.uploadimg':
# 					tmp = {}
# 					tmp['participate_count'] = appkit['count']
# 					tmp['title'] = appkit['title']
# 					tmp['type'] = appkit['title_type']
# 					tmp['values'] = []
# 					for value in appkit['values']:
# 						__debug_print(value)
# 						if 'created_at' in value:
# 							value['submit_time'] = value['created_at']
# 							del value['created_at']
# 						if 'content' in value:
# 							imgval = value['content'][0]
# 							imgval = imgval.strip("<").strip(">").split("src=")[1].strip("\"").strip("\'")
# 							value['content'] = imgval
# 						tmp['values'].append(value)
# 					actual.append(tmp)
# 				elif appkit['type'] == 'appkit.selection':
# 					tmp = {}
# 					tmp['participate_count'] = appkit['count']
# 					tmp['title'] = appkit['title']
# 					tmp['type'] = appkit['title_type']
# 					tmp['values'] = []
# 					for value in appkit['values']:
# 						if 'name' in value:
# 							value['options'] = value['name']
# 							del value['name']
# 						if 'per' in value:
# 							value['percent'] = value['per']
# 							del value['per']
# 						tmp['values'].append(value)
# 					actual.append(tmp)

# 	print("actual: {}".format(actual))
# 	bdd_util.assert_list(expect,actual)



