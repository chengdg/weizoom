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
from django.db.models import Sum
from django.db.models import Q

from market_tools import export
from excel_response import ExcelResponse

from core.jsonresponse import JsonResponse, create_response
from core import paginator

from market_tools.tools.coupon.util import get_coupon_rules, consume_coupon

from models import *
from modules.member import module_api as member_module_api
#from member.models import Member

COUNT_PER_PAGE = 20
MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'activity'

########################################################################
# list_activities: 显示活动列表
########################################################################
@login_required
def list_activities(request):
	activities = Activity.objects.filter(owner=request.user)

	for activity in activities:
		activity.member_count = activity.joined_weapp_users_count
		activity.check_time()
		
		start_date = activity.start_date
		today = datetime.today()

		start_date_time = datetime.strptime(start_date, '%Y-%m-%d')
		if today >= start_date_time:
			activity.allowed_start = 1
		else:
			activity.allowed_start = 0

		activity.status_text = STATUS2TEXT[activity.status]
		activity.can_delete = False
		activity.can_stop = False
		activity.can_restart = False
		if activity.status == ACTIVITY_STATUS_NO_START:
			activity.can_delete = True
		if activity.status == ACTIVITY_STATUS_RUNING:
			activity.can_stop = True
		elif activity.status == ACTIVITY_STATUS_STOP:
			activity.can_restart = True
		elif activity.status == ACTIVITY_STATUS_TIMEOUT:
			activity.can_delete = True

	#分页
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, activities = paginator.paginate(activities, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'activities': activities,
		'pageinfo': json.dumps(paginator.to_dict(pageinfo)),
	})
	return render_to_response('activity/editor/activities.html', c)


########################################################################
# __extract_items: 抽取activity items
########################################################################
def __extract_items(request):
	id2info = {}
	for key, value in request.POST.items():
		if not key.startswith('item_'):
			continue

		_, type, name, id = key.split('_')
		if type == 'text':
			type = ACTIVITYITEM_TYPE_TEXT
		elif type == 'select':
			type = ACTIVITYITEM_TYPE_SELECT
		elif type == 'checkbox':
			type = ACTIVITYITEM_TYPE_CHECKBOX
		elif type == 'image':
			type = ACTIVITYITEM_TYPE_IMAGE
		else:
			type = -1

		if id in id2info:
			info = id2info[id]
		else:
			info = {'type': type, 'id': int(id)}
			id2info[id] = info

		info[name] = value

	items = id2info.values()
	items.sort(lambda x,y: cmp(x['id'], y['id']))

	return items


########################################################################
# __update_activity_items: 更新activity items
########################################################################
def __update_activity_items(request, activity_id):
	ActivityItem.objects.filter(activity_id=activity_id).delete()

	for item in __extract_items(request):
		ActivityItem.objects.create(
			owner = request.user, 
			activity_id = activity_id, 
			title = item['title'], 
			type = item['type'],
			initial_data = item.get('data', ''),
			is_mandatory = 'mandatory' in item
		)


########################################################################
# __get_start_time_and_end_time: 获取开始时间和结束时间
########################################################################
def __get_start_time_and_end_time(request):
	start_date = request.POST.get("start_date", "0")
	end_date = request.POST.get("end_date", "0")
	if start_date != "0" and end_date != "0":
		start_date_time = datetime.strptime(start_date,'%Y-%m-%d')
		end_date_time = datetime.strptime(end_date,'%Y-%m-%d')
		temp = start_date;
		if start_date_time > end_date_time:
			start_date = end_date
			end_date = temp
	return start_date, end_date


########################################################################
# create_activity: 添加活动
########################################################################
TYPE_TEXT_NAME = "text_%s"
TYPE_SELECT_NAME = "select_%s"
TYPE_IMAGE_NAME = "image_%s"
TYPE_SELECT_OPTION = "option_%s"
@login_required
def create_activity(request):
	if request.POST:
		name = request.POST["name"]
		detail =request.POST.get("detail", '')
		guide_url = request.POST.get("guide_url", '')
		is_enable_offline_sign = request.POST.get("is_enable_offline_sign", False)
		is_non_member = request.POST.get("is_non_member", False)
		prize_type = request.POST.get("prize_type", '-1')
		prize_source = request.POST.get("prize_source", '')

		start_date, end_date = __get_start_time_and_end_time(request)
		current_time = datetime.today()
		current_time = current_time.strftime('%Y-%m-%d')
		current_time = datetime.strptime(current_time, '%Y-%m-%d')
		start_date_time = datetime.strptime(start_date, '%Y-%m-%d')

		status = ACTIVITY_STATUS_NO_START
		if start_date_time == current_time:
			status = ACTIVITY_STATUS_RUNING
		
		activity = Activity.objects.create(
			owner=request.user, 
			guide_url=guide_url, 
			name=name, 
			start_date=start_date, 
			end_date=end_date, 
			detail=detail, 
			status=status,
			is_enable_offline_sign=is_enable_offline_sign,
			prize_type=prize_type,
			prize_source=prize_source,
			is_non_member=is_non_member
		)

		__update_activity_items(request, activity.id)
		
		return HttpResponseRedirect('/market_tools/activity/')
	else:
		coupon_rules = get_coupon_rules(request.user)
		coupon_rule_items = []
		for coupon_rule in coupon_rules:
			coupon_rule_items.append(coupon_rule.to_dict())
		c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'activity': {'can_update': True},
			'coupon_rule_items': json.dumps(coupon_rule_items)
		})
		return render_to_response('activity/editor/edit_activity.html', c)


########################################################################
# update_activity: 更新活动
########################################################################
@login_required
def update_activity(request, activity_id):
	if request.POST:
		name = request.POST["name"]
		detail =request.POST.get("detail", '')
		guide_url = request.POST.get("guide_url", '')
		is_enable_offline_sign = request.POST.get("is_enable_offline_sign", False)
		if is_enable_offline_sign:
			prize_type = request.POST.get("prize_type", '-1')
			prize_source = request.POST.get("prize_source", '')
		else:
			prize_type = -1
			prize_source = ''
		is_non_member = request.POST.get("is_non_member", False)
		start_date, end_date = __get_start_time_and_end_time(request)
		current_time = datetime.today()
		current_time = current_time.strftime('%Y-%m-%d')
		current_time = datetime.strptime(current_time, '%Y-%m-%d')
		start_date_time = datetime.strptime(start_date, '%Y-%m-%d')

		status = ACTIVITY_STATUS_NO_START
		if start_date_time == current_time:
			status = ACTIVITY_STATUS_RUNING
		
		Activity.objects.filter(id=activity_id).update(
			guide_url = guide_url, 
			name = name, 
			start_date = start_date, 
			end_date = end_date, 
			detail = detail, 
			status = status,
			prize_type = prize_type,
			prize_source = prize_source,
			is_non_member = is_non_member
		)

		__update_activity_items(request, activity_id)

		return HttpResponseRedirect('/market_tools/activity/')
	else:
		activity = Activity.objects.get(id=activity_id)
		activity.can_update = False
		if activity.status == ACTIVITY_STATUS_NO_START:
			activity.can_update = True

		activity_items = []
		for activity_item in ActivityItem.objects.filter(activity=activity):
			type = 'text'
			if activity_item.type == ACTIVITYITEM_TYPE_SELECT:
				type = 'select'
			elif activity_item.type == ACTIVITYITEM_TYPE_IMAGE:
				type = 'image'
			elif activity_item.type == ACTIVITYITEM_TYPE_CHECKBOX:
				type = 'checkbox'

			activity_items.append({
				'id': activity_item.id,
				'title': activity_item.title,
				'initial_data': activity_item.initial_data,
				'is_mandatory': activity_item.is_mandatory,
				'type': type
			})
		coupon_rules = get_coupon_rules(request.user)
		coupon_rule_items = []
		for coupon_rule in coupon_rules:
			coupon_rule_items.append({
				'id': coupon_rule.id,
				'name': coupon_rule.name,
			})
		c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'activity': activity,
			'activity_items': json.dumps(activity_items),
			'coupon_rule_items': json.dumps(coupon_rule_items)
		})
		return render_to_response('activity/editor/edit_activity.html', c)


########################################################################
# update_activity_status: 更改活动状态
########################################################################
def update_activity_status(request, activity_id):
	action = request.GET['action']
	if action == 'stop':
		Activity.objects.filter(id=activity_id).update(status=ACTIVITY_STATUS_STOP)
	elif action == 'restart':
		Activity.objects.filter(id=activity_id).update(status=ACTIVITY_STATUS_RUNING)
	else:
		pass
	try:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	except:
		return HttpResponseRedirect('/market_tools/activity/')


########################################################################
# delete_activity: 删除活动
########################################################################
@login_required
def delete_activity(request, activity_id):
	Activity.objects.filter(id=activity_id).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# show_activity: 活动信息
########################################################################
@login_required
def list_activity_members(request):
	activity_id = request.GET['activity_id']
	activity  = Activity.objects.get(id=activity_id)
	
#	members = activity.joined_members
#	member_ids = [member.id for member in members]
#
#	member2values = {}
#	for item_value in ActivityItemValue.objects.filter(activity=activity, member_id__in=member_ids):
#		member2values.setdefault(item_value.member_id, {})[item_value.item_id] = item_value
#
#	items = list(ActivityItem.objects.filter(activity=activity))
#	if activity.is_sign:
#		activity_user_codes = ActivityUserCode.objects.filter(activity=activity, user_id__in=member_ids)
#		user_id2code = dict([(a.user_id, a.sign_code) for a in activity_user_codes])
#
#	for member in members:
#		item_values = []
#		for item in items:
#			id2value = member2values[member.id]
#			if not item.id in id2value:
#				#存在非必填项
#				continue
#
#			value = id2value[item.id]
#			user_input_value = value.value
#
#			is_image = False
#			if item.type == ACTIVITYITEM_TYPE_IMAGE:
#				is_image = True
#			try:
#				member.sign_code = user_id2code[member.id]
#			except:
#				member.sign_code = ''
#			item_values.append({
#				'title': item.title,
#				'is_image': is_image,
#				'user_input_value': user_input_value
#			})
#
#		member.item_values = item_values

	c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'activity': activity
#			'members': members
		})
	return render_to_response('activity/editor/activity_members.html', c)


########################################################################
# export_activity_members: 导出活动会员
########################################################################
@login_required
def export_activity_members(request, activity_id):
	activity = Activity.objects.get(id=activity_id)
	title_list = [u'会员名称',u'凭证码', u'是否签到']
	items = ActivityItem.objects.filter(activity=activity)
	titile_order = []
	for item in items:
		title_list.append(item.title)
		titile_order.append(item.id)

	member_info =  [ [activity.name]]
	member_info.append(title_list)
	member_id_list = ActivityItemValue.objects.filter(activity=activity, owner=request.user).values("webapp_user_id").distinct().order_by("webapp_user_id")

	for member_id_dict in member_id_list:
		webapp_user_id = member_id_dict['webapp_user_id']

		member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
		items_values =  ActivityItemValue.objects.filter(activity=activity, webapp_user_id=webapp_user_id)
		if member:
			nike_name = member.username
			try:
				nike_name = nike_name.decode('utf8')
			except:
				nike_name = member.username_hexstr
			items_value_list = [nike_name]
		else:
			items_value_list = ['-']

		if int(webapp_user_id) != -1:
			activity_codes = ActivityUserCode.objects.filter(activity=activity, webapp_user_id=webapp_user_id)
			if activity_codes.count() > 0:
				activity_code = activity_codes[0]
				items_value_list.append(activity_code.sign_code)
				if activity_code.sign_status == 0:
					items_value_list.append(u'未签到')
				else:
					items_value_list.append(u'已签到')
			else:
				items_value_list.append('-')
				items_value_list.append('-')
		else:
			items_value_list.append('-')
			items_value_list.append('-')

		items_value_dict = {}
		for items_value in items_values:
			p=titile_order.index(items_value.item.id) 
			items_value_dict[p] = items_value.value
		
		for i in range(len(titile_order)):
			if items_value_dict.has_key(i):
				items_value_list.append(items_value_dict[i])
			else:
				items_value_list.append('')

		member_info.append(items_value_list)

	return ExcelResponse(member_info,output_name=u'报名列表'.encode('utf8'),force_csv=False)


########################################################################
# update_activity_sign_status: 更改活动签到状态
########################################################################
def update_activity_sign_status(request, sign_code):
	activity_user_code = ActivityUserCode.objects.filter(sign_code=sign_code)
	activity_user_code.update(sign_status=1)
	if activity_user_code:
		activity = activity_user_code[0].activity
		member_id = int(request.GET.get('member_id', -1))
		member = member_module_api.get_member_by_id(member_id)
		if member:
			#给予奖励
			#无奖励
			if activity.prize_type == -1:
				pass
			#优惠券
			elif activity.prize_type == 1:
				rule_id = activity.prize_source
				# coupons = create_coupons(activity.owner, rule_id, 1, member.id)
				consume_coupon(activity.owner.id, rule_id, member.id)
			#积分
			elif activity.prize_type == 3:
				prize_detail = activity.prize_source
				#增加积分
				member.consume_integral(-int(prize_detail), u'参加获得，获得积分')
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

