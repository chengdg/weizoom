# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import

import time
from django.conf import settings
from django.db.models import F

from core.exceptionutil import unicode_full_stack

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from modules.member.models import *
from datetime import datetime

# from weixin.message.handler.weixin_message import WeixinMessageTypes
# from weixin.message.message import util as message_util
# from weixin.message.message.models import Message
# from weixin.message.qa.models import Rule
from weixin.user.models import WeixinUser, get_token_for

from account.social_account.models import SocialAccount
from account import models as account_models

from celery import task

import util as member_util
from account.social_account.account_info import get_social_account_info
from utils.string_util import byte_to_hex, hex_to_byte

# @task
# def process_error_openid(openid, user_profile):
# 	print 'call process_error_openid start'
# 	_process_error_openid(openid, user_profile)
# 	print 'OK'
	

@task
def update_member_pay_info(order):
	webapp_user_id = order.webapp_user_id
	member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
	if member:
		try:
			unit_price = (member.pay_money + order.final_price)/(member.pay_times + 1)
			Member.objects.filter(id=member.id).update(pay_money=F('pay_money')+order.final_price, pay_times=F('pay_times')+1, unit_price=unit_price)
		except:
			notify_message = u"_process_error_openid member_id:{}, cause:\n{}".format(member.id, unicode_full_stack())
			watchdog_error(notify_message)



@task
def update_member_integral(member_id, follower_member_id, integral_increase_count, event_type, webapp_user_id, reason="", manager=""):
	#time.sleep(0.5)
	integral_increase_count = int(integral_increase_count)
	member = Member.objects.get(id = member_id)
	if follower_member_id:
		follower_member = Member.objects.get(id = follower_member_id)
	else:
		follower_member = None

	if integral_increase_count == 0:
		return None

	current_integral = member.integral + integral_increase_count
	if integral_increase_count > 0:
		Member.objects.filter(id = member_id).update(integral=F('integral')+integral_increase_count, experience=F('experience')+integral_increase_count)
	else:
		Member.objects.filter(id = member_id).update(integral=F('integral')+integral_increase_count)
	try:

		MemberIntegralLog.objects.create(
				member = member, 
				follower_member_token = follower_member.token if follower_member else '', 
				integral_count = integral_increase_count, 
				event_type = event_type,
				webapp_user_id = webapp_user_id,
				reason=reason,
				current_integral=current_integral,
				manager=manager
			)
	except:
		notify_message = u"update_member_integral member_id:{}, cause:\n{}".format(member.id, unicode_full_stack())
		watchdog_error(notify_message)

@task
def increase_intgral_for_be_member_first(member_id, webapp_id, event_type):
	if IntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() > 0:
		integral_stting = IntegralStrategySttings.objects.filter(webapp_id=webapp_id)[0]
		update_member_integral(member_id, 0, integral_stting.be_member_increase_count, event_type, 0)

	"""
	防止数据库锁
	"""	
	try:
		update_member_from_weixin_api(member_id, webapp_id)
	except:
		notify_message = u"member_id:{} increase_intgral_for_be_member_first update_member_from_weixin_api cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_error(notify_message)
	


@task
def create_member_info(member_id, name, sex):
	if MemberInfo.objects.filter(member_id=member_id).count() > 0:
		return 
	
	MemberInfo.objects.create(
			member = Member.objects.get(id=member_id),
			name = name,
			sex = sex
			)


@task
def process_oauth_member_relation_and_source(fmt, member_id, is_new_created_member=False):
	print 'received watchdog process_oauth_member_relation_and_source'
	_process_oauth_member_relation_and_source(fmt, member_id, is_new_created_member)		
	return 'OK'

def _process_oauth_member_relation_and_source(fmt, member_id, is_new_created_member=False):
	from modules.member.integral_new import increase_for_click_shared_url
	member = Member.objects.get(id=member_id)
	try:
		if fmt and member and fmt != member.token:
			#建立关系，更新会员来源
			follow_member = Member.objects.get(token=fmt)
			if follow_member.webapp_id != member.webapp_id:
				return
				
			if is_new_created_member:
				MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
				MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
				member.source = SOURCE_BY_URL
				member.save()
			elif MemberFollowRelation.objects.filter(member_id=member.id, follower_member_id=follow_member.id).count() == 0:
				MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
				MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
			#点击分享链接给会员增加积分
			try:
				increase_for_click_shared_url(follow_member, member, request.get_full_path())
			except:
				notify_message = u"increase_for_click_shared_url:('member_id':{}), cause:\n{}".format(member.id, unicode_full_stack())
				watchdog_fatal(notify_message)
	except:
		notify_message = u"('fmt':{}), 处理分享信息process_oauth_member_relation_and_source cause:\n{}".format(fmt, unicode_full_stack())
		watchdog_fatal(notify_message)

def update_member_from_weixin_api(member_id, webapp_id):
	social_account = MemberHasSocialAccount.objects.filter(member_id=member_id)[0].account
	#SocialAccount.objects.get(id=social_account_id)
	user_profile = account_models.UserProfile.objects.get(webapp_id=social_account.webapp_id)
	social_account_info = get_social_account_info(social_account, user_profile)
	#member_grade = MemberGrade.get_default_grade(social_account.webapp_id)
	sex = 0
	if social_account_info:
		member_nickname = social_account_info.nickname if social_account_info else ''
		if isinstance(member_nickname, unicode):
			member_nickname_str = member_nickname.encode('utf-8')
		else:
			member_nickname_str = member_nickname
		username_hexstr = byte_to_hex(member_nickname_str)
		
		if not username_hexstr:
			username_hexstr = ''
		sex = social_account_info.sex
		if sex == '' or sex == None:
			sex = 0
		Member.objects.filter(id=member_id).update(user_icon=social_account_info.head_img, 
					update_time = datetime.now(), 
					username_hexstr=username_hexstr,
					#is_subscribed=social_account_info.is_subscribed,
					city=social_account_info.city,
					province=social_account_info.province,
					country=social_account_info.country,
					sex=sex,
					)

	create_member_info(member_id,'', sex)






