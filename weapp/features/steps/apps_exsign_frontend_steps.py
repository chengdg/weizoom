# -*- coding: utf-8 -*-
__author__ = 'kuki'
from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.exsign.models import exSign, exSignParticipance, exSignDetails
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re
from mall.promotion.models import Coupon

from weixin.message.material import models as material_models
import apps_step_utils as apps_util

def __get_exsign_record_id(webapp_owner_id):
	return exSign.objects.get(owner_id=webapp_owner_id).id

@when(u"{webapp_user_name}进入{webapp_owner_name}专项签到页面进行签到")
def step_tmpl(context, webapp_user_name, webapp_owner_name):
	webapp_owner_id = context.webapp_owner_id
	appRecordId = __get_exsign_record_id(webapp_owner_id)
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': appRecordId
	}
	response = context.client.post('/m/apps/exsign/api/exsign_participance/?_method=put', params)
	context.datas = json.loads(response.content)['data']

@then(u"{webapp_user_name}获取专项签到成功的内容")
def step_tmpl(context, webapp_user_name):
	datas = context.datas
	# 构造实际数据
	actual = []
	daily_coupons = datas['curr_prize']["coupon"]
	daily_coupon_list = []
	for d in daily_coupons:
		daily_coupon_list.append(d["name"])
	curr_coupons = datas['curr_prize']["coupon"]
	curr_coupon_list = []
	for c in curr_coupons:
		curr_coupon_list.append(c["name"])
	actual.append({
		'serial_count': datas['serial_count'],
		'daily_prize': {
			'integral': datas['daily_prize']['integral'],
			'coupons': daily_coupon_list
		},
		'curr_prize': {
			'integral': datas['curr_prize']['integral'],
			'coupons': curr_coupon_list
		}
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)


@when(u"修改{user}的专项签到时间为前一天")
def step_impl(context, user):
	signParticipance = exSignParticipance.objects.get(member_id=context.member.id)
	created_at = signParticipance.created_at
	signParticipance.update(set__created_at = created_at-timedelta(days=1))
	item = exSignDetails.objects.filter(belong_to=context.exsign_id, member_id=context.member.id).order_by('-id').first()
	item.update(set__created_at = created_at-timedelta(days=1))
	__change_sign_date(context.member.id,1)

#只修改参与时间
def __change_sign_date(member_id,days):
	signParticipance = exSignParticipance.objects.get(member_id=member_id)
	latest_date = signParticipance.latest_date
	signParticipance.update(set__latest_date = latest_date-timedelta(days))

@When(u'{webapp_user_name}把{webapp_owner_name}的专项签到活动链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name):
	context.shared_url = context.link_url

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的专项签到链接进行签到')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	if member.is_subscribed: #非会员不可签到
		appRecordId = __get_exsign_record_id(webapp_owner_id)
		params = {
			'webapp_owner_id': webapp_owner_id,
			'id': appRecordId
		}
		response = context.client.post('/m/apps/exsign/api/exsign_participance/?_method=put', params)
	else:
		pass


@when(u"{webapp_user_name}点击图文'{title}'进入专项签到活动页面")
def step_impl(context, webapp_user_name, title):
	user = User.objects.get(id=context.webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	_, exsign_id = __exsign_name2id('', title)
	context.exsign_id = str(exsign_id)
	context.openid = openid

	#获取页面
	view_mobile_main_page(context)
	get_dynamic_data(context)

def view_mobile_main_page(context):
	"""
	进入活动主页
	@param context:
	@return:
	"""
	return apps_util.get_response(context, {
		"app": "m/apps/exsign",
		"resource": "m_exsign",
		"method": "get",
		"type": "get",
		"args": {
			"webapp_owner_id": context.webapp_owner_id,
			"id": context.exsign_id
		}
	})

def get_dynamic_data(context):
	return apps_util.get_response(context, {
		"app": "m/apps/exsign",
		"resource": "m_exsign",
		"type": "api",
		"method": "get",
		"args": {
		    "webapp_owner_id": context.webapp_owner_id,
		    "id": context.exsign_id
		}
	})

def __exsign_name2id(name, title=None):
	"""
	给签到项目的名字，返回id元祖
	返回（related_page_id,group_group中id）
	"""
	if title:
		name = material_models.News.objects.get(title=title).url
	exsign = exSign.objects.get(name=name)
	return exsign.related_page_id,exsign.id

@when(u"{webapp_user_name}参加专项签到活动于'{date_str}'")
def step_impl(context, webapp_user_name, date_str):
	today = datetime.now()
	date = "%s %s" % (bdd_util.get_date_str(date_str),today.strftime("%H:%M:%S"))
	if not hasattr(context,"latest_date"):
		context.latest_date = {
			webapp_user_name : bdd_util.get_date(date)
		}

	params = {
		'webapp_owner_id': context.webapp_owner_id,
		'id': context.exsign_id
	}
	signParticipance = exSignParticipance.objects(member_id=context.member.id)
	if signParticipance:
		timedelta = (bdd_util.get_date(date) - context.latest_date[webapp_user_name]).days
		__change_sign_date(context.member.id,timedelta)#将上一次签到时间向前调整
		response = context.client.post('/m/apps/exsign/api/exsign_participance/?_method=put', params)
	else:
		response = context.client.post('/m/apps/exsign/api/exsign_participance/?_method=put', params)
		#首次签到的话，将首次签到时间置为设定的时间
		signParticipance.update(set__created_at = bdd_util.get_date(date))
	#如果是另一个用户签到了，创建新的最近一次签到时间到dict里
	if webapp_user_name not in context.latest_date:
		context.latest_date[webapp_user_name] = bdd_util.get_date(date)
	#对比时间，记录最后一次签到时间
	if context.latest_date[webapp_user_name] < bdd_util.get_date(date):
		context.latest_date[webapp_user_name] = bdd_util.get_date(date)


	item = exSignDetails.objects.filter(belong_to=context.exsign_id, member_id=context.member.id).order_by('-id').first()
	item.update(created_at = bdd_util.get_date(date))


	# 下面的step会将签到详情领取时间改成step接受的时间.
	sign_details_index = exSignDetails.objects.count() - 1
	last_sign = exSignDetails.objects.all()[sign_details_index] # 得到最后一个签到信息

	if last_sign.prize["coupon"]: # 如果最后一个签到信息中提示获得了优惠券.修改日期为当前时间
		import time
		time.sleep(1)

		from apps.customerized_apps.mysql_models import  ConsumeCouponLog
		coupon_log_index = ConsumeCouponLog.objects.count() - 1
		last_coupon = ConsumeCouponLog.objects.all()[coupon_log_index]
		coupon = Coupon.objects.filter(id=last_coupon.coupon_id)

		coupon.update(provided_time=date) # 修改日期为当前时间


	context.need_change_date = True

@then(u"{webapp_user_name}参加专项签到活动")
def step_impl(context, webapp_user_name):
	# today = datetime.now()
	# date = today.strftime("%Y-%m-%d %H:%M:%S")
	# if not hasattr(context,"latest_date"):
	# 	context.latest_date = {
	# 		webapp_user_name : bdd_util.get_date(date)
	# 	}

	params = {
		'webapp_owner_id': context.webapp_owner_id,
		'id': context.exsign_id
	}
	# signParticipance = SignParticipance.objects(member_id=context.member.id)
	# if signParticipance:
	# 	timedelta = (bdd_util.get_date(date) - context.latest_date[webapp_user_name]).days
	# 	__change_sign_date(context.member.id,timedelta)#将上一次签到时间向前调整
	response = context.client.post('/m/apps/exsign/api/exsign_participance/?_method=put', params)
	# else:
	# 	response = context.client.post('/m/apps/sign/api/sign_participance/?_method=put', params)
	# 	#首次签到的话，将首次签到时间置为设定的时间
	# 	signParticipance.update(set__created_at = bdd_util.get_date(date))
	# #如果是另一个用户签到了，创建新的最近一次签到时间到dict里
	# if webapp_user_name not in context.latest_date:
	# 	context.latest_date[webapp_user_name] = bdd_util.get_date(date)
	# #对比时间，记录最后一次签到时间
	# if context.latest_date[webapp_user_name] < bdd_util.get_date(date):
	# 	context.latest_date[webapp_user_name] = bdd_util.get_date(date)
	#
	# item = SignDetails.objects.filter(belong_to=context.sign_id, member_id=context.member.id).order_by('-id').first()
	# item.update(set__created_at = bdd_util.get_date(date))
	#
	# context.need_change_date = True


@when(u"{user}设置专项签到统计列表查询参数")
def step_impl(context, user):
	context.filter = json.loads(context.text)
