# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack

from webapp.modules.mall.models import *
from modules.member.models import *
from modules.member import util as member_util
from account.models import *

from tools.regional.views import get_str_value_by_string_ids
from core.send_order_email_code import *
from modules.member.member_decorators import member_required
from market_tools.export_api import *
from watchdog.utils import *


########################################################################
# get_integral_log: 获取会员积分使用日志
# 1. 解析会员信息：
#    当会员信息为空时，直接跳转到404页面
# 2. 获取与该会员对应的积分日志列表（按日期倒叙）
# 3. 组织积分日志结构，将同一天好友奖励的积分日志在一条记录中显示，并且显示好友头像
########################################################################
def get_integral_log(request):
	# 1. 解析会员信息
	member_id = request.GET.get('member_id','')
	try:
		if not hasattr(request, 'member') or request.member is None:
			member = Member.objects.get(id=member_id)
		else:
			member = request.member
		MemberIntegralLog.update_follower_member_token(member)
	except:
		notify_msg = u"webapp，积分日志, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		raise Http404('不存在该会员')

	# 2. 获取与该会员对应的积分日志列表（按日期倒叙）
	member_integral_logs = list(MemberIntegralLog.objects.filter(member=member).order_by('-created_at'))

	# 3. 组织积分日志结构，将同一天好友奖励的积分日志在一条记录中显示，并且显示好友头像
	organized_integral_log_list = __get_organized_integral_log_list(member_integral_logs)

	return organized_integral_log_list


########################################################################
# __get_organized_integral_log_list: 获取组织后的日志列表
########################################################################
def __get_organized_integral_log_list(log_list):
	# 组织后的日志列表
	organized_log_list = list()
	# 当前好友奖励
	current_friend_log_list = None
	# 当前日志日期
	current_friend_log_list_date = None

	for log in log_list:
		# 是否是为好友奖励
		if __is_dueto_friend_action(log):
			if current_friend_log_list_date == log.created_at.strftime('%Y%m%d'):
				# 是当天日期的好友奖励日志，加入current_friend_log_list
				current_friend_log_list = __append_current_friend_day_logs(current_friend_log_list, log)
			else:
				# 不是是当天日期的好友奖励日志
				# 初始化当前好友奖励current_friend_log_list，并加入日志
				# 更改当前日志日期
				current_friend_log_list = __create_current_friend_day_logs(log)
				current_friend_log_list = __append_current_friend_day_logs(current_friend_log_list, log)

				organized_log_list.append(current_friend_log_list)
				current_friend_log_list_date = log.created_at.strftime('%Y%m%d')
		else:
			# 将非好友奖励的日志，加入列表中
			organized_log_list = __append_organized_log_list(organized_log_list, log)

	return organized_log_list


########################################################################
# __append_organized_log_list: 将日志加入到组织后的列表中
########################################################################
def __append_organized_log_list(log_list, current_log):
	log_list.append(current_log)
	return log_list

########################################################################
# __is_dueto_friend_action: 是否为好友奖励
# 存在follower_member_token或者event_type是‘好友奖励’
# 的日志为‘好友奖励’日志，返回True
# 否者返回False
########################################################################
def __is_dueto_friend_action(log):
	if log and (log.follower_member_token or log.event_type == FOLLOWER_CLICK_SHARED_URL):
		return True

	return False

########################################################################
# 创建一个同一天的好友list
########################################################################
def __create_current_friend_day_logs(member_integral_log):
	day_friend_log = MemberIntegralLog()
	day_friend_log.created_at = member_integral_log.created_at
	day_friend_log.event_type = FOLLOWER_CLICK_SHARED_URL
	day_friend_log.logs = list()
	return day_friend_log

########################################################################
# 将一个好友奖励日志，放入同一天的日志list中
########################################################################
def __append_current_friend_day_logs(day_friend_log, member_integral_log):
	try:
		friend_member = Member.objects.get(token=member_integral_log.follower_member_token)
		if friend_member.user_icon and friend_member.user_icon != '':
			member_integral_log.pic = friend_member.user_icon
		else:
			member_integral_log.pic = ''
	except:
		member_integral_log.pic = ''

	if day_friend_log is None:
		day_friend_log = __create_current_friend_day_logs(member_integral_log)

	# 如果会员的好友中没有头像，就不将好友加入到同一天的日志中
	# 但是会增加同一天的积分值
	if member_integral_log.pic:
		day_friend_log.logs.append(member_integral_log)

	day_friend_log.integral_count = day_friend_log.integral_count + member_integral_log.integral_count
	return day_friend_log
