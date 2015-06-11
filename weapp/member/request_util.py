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

from mall.models import *
from modules.member.models import *
from modules.member import util as member_util
from account.models import *

from tools.regional.views import get_str_value_by_string_ids
from core.send_order_email_code import *
from modules.member.member_decorators import member_required
from market_tools.export_api import *
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
from watchdog.utils import *

from apps.export import get_webapp_usage_link as get_all_cusapps_usage_link
import webapp.modules.mall.module_api as mall_api

########################################################################
# __get_current_user_info: 获取当前用户的头像和名称信息
########################################################################
def __get_current_user_info(request, member):
	member_util.member_basic_info_updater(request.user_profile, member)
	return Member.objects.get(id = member.id)


########################################################################
# get_user_info: 个人信息
########################################################################
def get_user_info(request):
	profile = request.user_profile
	member = request.member
	week = None
	shipInfo = None
	# TODO: 优化获取头像信息
	member = __get_current_user_info(request, member)

	# 收货信息
	shipInfos = ShipInfo.objects.filter(webapp_user_id=request.webapp_user.id)
	if shipInfos.count() > 0:
		shipInfo = shipInfos[0]
		shipInfo.area = get_str_value_by_string_ids(shipInfo.area)
	
	# 历史订单、待支付
	member.history_order_count = Order.objects.filter(webapp_user_id=request.webapp_user.id).count()
	member.not_payed_order_count = Order.objects.filter(webapp_user_id=request.webapp_user.id, status=ORDER_STATUS_NOT).count()

	#购物车中商品数量
	# product_counts = ShoppingCart.objects.filter(webapp_user_id=request.webapp_user.id).values_list('count', flat=True)
	# member.shopping_cart_product_count = sum(product_counts, 0)
	member.shopping_cart_product_count = mall_api.get_shopping_cart_product_nums(request.webapp_user)

	#营销工具使用情况链接
	market_tools = get_market_tool_webapp_usage_links(request.webapp_owner_id, request.member)
	#添加定制化app在个人中心页面显示的"我的**"
	market_tools += get_all_cusapps_usage_link(request.webapp_owner_id, request.member)
	#bert add at 14 
	#经验值
	grade_lists = MemberGrade.get_all_grades_list(member.webapp_id)
	is_can_use_weizoomcard = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.webapp_owner_id)
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'个人中心',
		'member': member,
		'shipInfo':shipInfo,
	    'request': request,
	    'market_tools': market_tools,
	    'is_can_use_weizoomcard':is_can_use_weizoomcard
	})
	return render_to_response('%s/user_center.html' % request.template_dir, c)


########################################################################
# influence_guide: 积分指南
########################################################################
def influence_guide(request):
	webapp_id = request.user_profile.webapp_id
	rices = Ricepage.objects.filter(built_name=u'积分指南')
	rice = None
	if rices.count() > 0:
		rice = rices[0]
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': page_title,
		'webapp_id': webapp_id,
	    'influence': rice
	})

	return render_to_response('%s/influence_guide.html' % request.template_dir, c)


########################################################################
# edit_ship_info: 修改收货人信息
########################################################################
def edit_ship_info(request):
	webapp_id = request.user_profile.webapp_id
	ship_info_id = request.GET.get('ship_info_id',0)
	if ship_info_id == '':
		ship_info_id = 0
	else:
		ship_info_id = int(ship_info_id)
	if ship_info_id > 0:
		ship_info = ShipInfo.objects.get(id=ship_info_id)
	else:
		ship_info = None

	if not ship_info and request.webapp_user:
		try:
			ship_info = ShipInfo.objects.get(webapp_user_id=request.webapp_user.id)
		except:
			ship_info = ShipInfo.objects.create(
				webapp_user_id = request.webapp_user.id
			)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'收货人信息',
		'webapp_id': webapp_id,
	    'shipInfo': ship_info
	})
	return render_to_response('%s/ship_info.html' % request.template_dir, c)


########################################################################
# save_ship_info: 保存收货人信息
########################################################################
def save_ship_info(request):
	ship_name = request.POST['ship_name']
	ship_address = request.POST['ship_address']
	ship_tel = request.POST['ship_tel']
	area = request.POST['area']
	ship_id = int(request.POST.get('ship_id', -1))
	request.webapp_user.update_ship_info(
		ship_name = ship_name,
		ship_address = ship_address,
		ship_tel = ship_tel,
		area = area,
		ship_id = ship_id
	)

	url = './?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%d&project_id=0' % request.webapp_owner_id
	return HttpResponseRedirect(url)


########################################################################
# get_integral_log: 获取会员积分使用日志
# 1. 解析会员信息：
#    当会员信息为空时，直接跳转到404页面
# 2. 获取与该会员对应的积分日志列表（按日期倒叙）
# 3. 组织积分日志结构，将同一天好友奖励的积分日志在一条记录中显示，并且显示好友头像
# 4. 将组织后的日志信息，渲染到integral_log.html页面中
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

	# 4. 将组织后的日志信息，渲染到integral_log.html页面中
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'积分日志',
		'member_integral_logs': organized_integral_log_list,
		'member': member
	})
	return render_to_response('%s/integral_log.html' % request.template_dir, c)


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

	day_friend_log.logs.append(member_integral_log)
	day_friend_log.integral_count = day_friend_log.integral_count + member_integral_log.integral_count
	return day_friend_log


########################################################################
# get_member_grade: 会员等级页
########################################################################
def get_member_grade(request):
	webapp_id = request.user_profile.webapp_id
	member_grade = MemberGrade.objects.filter(webapp_id=webapp_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'会员等级',
		'member_grades': member_grade,
	})
	return render_to_response('%s/member_guide.html' % request.template_dir, c)


########################################################################
# get_integral_grade: 积分指南页
########################################################################
def get_integral_grade(request):
	owner_id = request.webapp_owner_id
	article =  SpecialArticle.objects.get(name='integral_guide', owner_id=owner_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'积分指南',
		'article': article
	})
	return render_to_response('%s/integral_grade.html' % request.template_dir, c)


########################################################################
# get_user_guide: 用户指南页
########################################################################
def get_user_guide(request):
	webapp_owner_id = request.webapp_owner_id
	webapp_id = request.user_profile.webapp_id

	#积分指南
	integral_guide =  SpecialArticle.objects.get(name='integral_guide', owner_id=webapp_owner_id)

	#用户等级
	member_grades = MemberGrade.objects.filter(webapp_id=webapp_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'用户指南',
		'integral_guide': integral_guide,
		'member_grades': member_grades
	})
	return render_to_response('%s/user_guide.html' % request.template_dir, c)