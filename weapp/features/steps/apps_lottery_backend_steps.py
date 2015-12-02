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
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings
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

def __date_delta(start,end):
	"""
	获得日期，相差天数，返回int
	格式：
		start:(str){2015-11-23}
		end :(str){2015-11-30}
	"""
	start = dt.datetime.strptime(start, "%Y-%m-%d").date()
	end = dt.datetime.strptime(end, "%Y-%m-%d").date()
	return (end-start).days

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

def __lottery_name2id(name):
	"""
	给抽奖项目的名字，返回id元祖
	返回（related_page_id,lottery_lottery中id）
	"""
	obj = lottery_models.lottery.objects.get(name=name)
	return (obj.related_page_id,obj.id)

def __status2name(status_num):
	"""
	抽奖：状态值 转 文字
	"""
	status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
	return status2name_dic[status_num]

def __name2status(name):
	"""
	抽奖： 文字 转 状态值
	"""
	if name:
		name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
		return name2status_dic[name]
	else:
		return -1


def __get_actions(status):
	"""
	根据输入抽奖状态
	返回对于操作列表
	"""
	actions_list = [u"查看",u"预览",u"复制链接"]
	if status == u"已结束":
		actions_list.append(u"删除")
	elif status=="进行中" or "未开始":
		actions_list.append(u"关闭")
	return actions_list

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

	timing_status = text.get("is_show_countdown","")

	timing_value_day = __date_delta(start_date,end_date)

	description = text.get("desc","")
	reply_content = text.get("reply")
	material_image = text.get("share_pic","")
	background_image = text.get("background_pic","")

	qrcode_name = text.get("qr_code","")
	if qrcode_name:
		qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
		qrcode_i_url = '/new_weixin/qrcode/?setting_id=%s' % str(qrcode_id)
		qrcode_response = context.client.get(qrcode_i_url)
		qrcode_info = qrcode_response.context['qrcode']
		qrcode_ticket_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qrcode_info.ticket)
		qrcode = {"ticket":qrcode_ticket_url,"name":qrcode_info.name}
	else:
		qrcode = {"ticket":"","name":""}

	zhcolor = text.get("background_color","冬日暖阳")
	color = __name2color(zhcolor)

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
	get_pw_response = context.client.get("/apps/lottery/lottery/")
	pw_args_response = get_pw_response.context
	project_id = pw_args_response['project_id']#(str){new_app:lottery:0}

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
		"timing":timing_status,
		"reply_content":reply_content,
		"material_image":material_image,
		"qrcode":json.dumps(qrcode),
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

	timing_status = text.get("is_show_countdown","")

	timing_value_day = __date_delta(start_date,end_date)

	description = text.get("desc","")
	reply_content = text.get("reply")
	material_image = text.get("share_pic","")
	background_image = text.get("background_pic","")

	qrcode_name = text.get("qr_code","")
	if qrcode_name:
		qrcode = __get_qrcode(context,qrcode_name)
	else:
		qrcode = ""

	zhcolor = text.get("background_color","冬日暖阳")
	color = __name2color(zhcolor)

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
		"timing":timing_status,
		"reply_content":reply_content,
		"material_image":material_image,
		"qrcode":json.dumps(qrcode),
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

def __Stop_Lottery(context,lottery_id):
	"""
	关闭抽奖活动
	"""

	design_mode = 0
	version = 1
	stop_lottery_url = "/apps/lottery/api/lottery_status/?design_mode={}&version={}".format(design_mode,version)
	stop_args ={
		"id":lottery_id,
		"target":'stoped'
	}
	stop_lottery_response = context.client.post(stop_lottery_url,stop_args)
	return stop_lottery_response

def __Search_Lottery(context,search_dic):
	"""
	搜索抽奖活动

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	name = search_dic["name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]
	status = __name2status(search_dic["status"])



	search_url = "/apps/lottery/api/lotterys/?design_mode={}&version={}&name={}&status={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
			design_mode,
			version,
			name,
			status,
			start_time,
			end_time,
			count_per_page,
			page,
			enable_paginate)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response

def __Search_Lottery_Result(context,search_dic):
	"""
	搜索,抽奖参与结果

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	id = search_dic["id"]
	participant_name = search_dic["participant_name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]



	search_url = "/apps/lottery/api/lottery_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
			design_mode,
			version,
			id,
			participant_name,
			start_time,
			end_time,
			count_per_page,
			page,
			enable_paginate)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response



@when(u'{user}新建抽奖活动')
def step_impl(context,user):
	text_list = json.loads(context.text)
	for text in text_list:
		__Create_Lottery(context,text,user)

@then(u'{user}获得抽奖活动列表')
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
		rec_search_list = context.search_lottery
		for item in rec_search_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":item['start_time'],
				"end_time":item['end_time'],
				"participant_count":item['participant_count'],
				"total_lottery_value":item['total_power']
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

		rec_lottery_url ="/apps/lottery/api/lotterys/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
		rec_lottery_response = context.client.get(rec_lottery_url)
		rec_lottery_list = json.loads(rec_lottery_response.content)['data']['items']#[::-1]

		for item in rec_lottery_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":__date2time(item['start_time']),
				"end_time":__date2time(item['end_time']),
				"participant_count":item['participant_count'],
				"total_lottery_value":item['total_power']
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)


@when(u"{user}编辑抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	expect = json.loads(context.text)[0]
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	__Update_Lottery(context,expect,lottery_page_id,lottery_id)


@then(u"{user}获得抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	expect = json.loads(context.text)[0]

	title = expect.get("name","")
	cr_start_date = expect.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = expect.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	# valid_time = "%s~%s"%(start_time,end_time)
	timing_status = expect.get("is_show_countdown","")
	# timing_value_day = __date_delta(start_date,end_date)
	description = expect.get("desc","")
	reply_content = expect.get("reply")
	material_image = expect.get("share_pic","")
	background_image = expect.get("background_pic","")

	qrcode_name = expect.get("qr_code","")
	if qrcode_name:
		qrcode = __get_qrcode(context,qrcode_name)
	else:
		qrcode = ""

	color  = expect.get("background_color","冬日暖阳")
	rules = expect.get("rules","")


	obj = lottery_models.lottery.objects.get(name=lottery_name)#纯数字
	related_page_id = obj.related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_component = page['component']['components'][0]['model']

	fe_lottery_dic = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"is_show_countdown":timing_status,
		"desc":description,
		"reply":reply_content,
		"qr_code":qrcode,
		"share_pic":material_image,
		"background_pic":background_image,
		"background_color":color,
		"rules":rules
	}

	db_lottery_dic = {
		"name": obj.name,
		"start_time":__datetime2str(obj.start_time),
		"end_time":__datetime2str(obj.end_time),
		"is_show_countdown":page_component['timing']['timing']['select'],
		"desc":page_component['description'],
		"reply":obj.reply_content,
		"qr_code":obj.qrcode,
		"share_pic":page_component['material_image'],
		"background_pic": page_component['background_image'],
		"background_color": __color2name(page_component['color']),
		"rules": page_component['rules'],
	}

	bdd_util.assert_dict(db_lottery_dic, fe_lottery_dic)

@when(u"{user}删除抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	del_response = __Delete_Lottery(context,lottery_id)
	bdd_util.assert_api_call_success(del_response)


@when(u"{user}关闭抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	stop_response = __Stop_Lottery(context,lottery_id)
	bdd_util.assert_api_call_success(stop_response)


@when(u"{user}查看抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	url ='/apps/lottery/api/lottery_participances/?_method=get&id=%s' % (lottery_id)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	context.participances = json.loads(response.content)
	context.lottery_id = "%s"%(lottery_id)

@then(u"{webapp_user_name}获得抽奖活动'{power_me_rule_name}'的结果列表")
def step_tmpl(context, webapp_user_name, power_me_rule_name):
	if hasattr(context,"search_lottery_result"):
		participances = context.search_lottery_result
	else:
		participances = context.participances['data']['items']
	actual = []
	print(participances)
	for p in participances:
		p_dict = OrderedDict()
		p_dict[u"rank"] = p['ranking']
		p_dict[u"member_name"] = p['username']
		p_dict[u"lottery_value"] = p['power']
		p_dict[u"parti_time"] = bdd_util.get_date_str(p['created_at'])
		actual.append((p_dict))
	print("actual_data: {}".format(actual))
	expected = []
	if context.table:
		for row in context.table:
			cur_p = row.as_dict()
			if cur_p[u'parti_time']:
				cur_p[u'parti_time'] = bdd_util.get_date_str(cur_p[u'parti_time'])
			expected.append(cur_p)
	else:
		expected = json.loads(context.text)
	print("expected: {}".format(expected))

	bdd_util.assert_list(expected, actual)

@when(u"{user}设置抽奖活动列表查询条件")
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
		"status": expect.get("status",u"全部")
	}
	search_response = __Search_Lottery(context,search_dic)
	lottery_array = json.loads(search_response.content)['data']['items']
	context.search_lottery = lottery_array

@when(u"{user}访问抽奖活动列表第'{page_num}'页")
def step_impl(context,user,page_num):
	count_per_page = context.count_per_page
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问抽奖活动列表下一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])+1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问抽奖活动列表上一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])-1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}设置抽奖活动结果列表查询条件")
def step_impl(context,user):
	expect = json.loads(context.text)

	if 'parti_start_time' in expect:
		expect['start_time'] = __date2time(expect['parti_start_time']) if expect['parti_start_time'] else ""
		del expect['parti_start_time']

	if 'parti_end_time' in expect:
		expect['end_time'] = __date2time(expect['parti_end_time']) if expect['parti_end_time'] else ""
		del expect['parti_end_time']

	id = context.lottery_id
	participant_name = expect.get("member_name","")
	start_time = expect.get("start_time","")
	end_time = expect.get("end_time","")

	search_dic = {
		"id":id,
		"participant_name":participant_name,
		"start_time":start_time,
		"end_time":end_time
	}
	search_response = __Search_Lottery_Result(context,search_dic)
	lottery_result_array = json.loads(search_response.content)['data']['items']
	context.search_lottery_result = lottery_result_array

@then(u"{user}能批量导出抽奖活动'{lottery_name}'")
def step_impl(context,user,lottery_name):
	lottery_page_id,lottery_id = __lottery_name2id(lottery_name)#纯数字
	url ='/apps/lottery/api/lottery_participances_export/?_method=get&export_id=%s' % (lottery_id)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)