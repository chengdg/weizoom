# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core import chartutil

from core.alipay.alipay_submit import *
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
from core.alipay.alipay_notify import AlipayNotify
from core.alipay.alipay_submit import AlipaySubmit
from core.sendmail import sendmail
from account.models import UserProfile

from shengjing.models import *
from shengjing.crm_api import api_views as crm_api_views
from shengjing.user_center.util import get_binding_info_by_member
import weapp.settings as settings
from watchdog.utils import watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
from modules.member import module_api as member_module_api
from modules.member.integral import IntegralCaculator

from apps.register import mobile_api

########################################################################
# apply_course:
########################################################################
@mobile_api(resource='applied_course', action='create')
def apply_course(request):
	#获取当前会员
	try:
		member = request.member
		member_id = member.id
		member_name = member.username
	except:
		member_id = request.GET.get('member_id', '')
		member = member_module_api.get_member_by_id(int(member_id))
	course_name = request.GET.get('course_name', '')
	apply_number = int(request.GET.get('count', 0))
	owner_id = request.webapp_owner_id
	course_id = int(request.GET.get('course_id', 0))
	referrer = request.GET.get('referrer', '')
	cousrses= ShengjingCourseRegistration.objects.filter(member_id=member_id, course_id=course_id)
	if cousrses:
		course = cousrses[0]
		course.apply_number = apply_number
		course.save()
	else:
		course = ShengjingCourseRegistration()
		course.member_id = member_id
		course.course_id = course_id
		course.apply_number = apply_number
		course.owner_id = owner_id
		course.referrer = referrer
		course.save()
	_, member_info = get_binding_info_by_member(member)

	if member_info:
		companys = member_info.companys
		company_names = [c.name for c in companys]
		phone = member_info.phone_number
		member_name = member_info.name
	else:
		#没获取到对应的会员信息
		watchdog_error(u'报名时没有对应的盛景会员的信息  系统会员ID: %s' % member_id, user_id=request.user.id)
		company_names = []
		phone = ''
		member_name = ''
	company_name_strs = '_'.join(company_names)
	content = u'报名时间： %s<br>报名课程：%s<br>报名人：%s<br>所属公司：%s<br>电话：%s<br>预计参课人数: %s' % (datetime.today().strftime("%Y-%m-%d %H:%M"), course_name, member_name, company_name_strs, phone, apply_number)
	#是否是决策人	
	try:
		items = crm_api_views.get_userinfo_by_phone_number(member_info.phone_number)
	except:
		watchdog_error(u'盛景获取课程详情判断是否是决策人API出错')
		items = []
	try:
		phone_number = items['phone']
	except:
		phone_number = ''
	if not phone_number:
		content = content + u'<br>推荐人：%s' % referrer
#	try:
#		webapp_owner_id = request.webapp_owner_id
#	except:
	webapp_owner_id = request.GET.get('webapp_owner_id', '')
	emails = ShengjingEmailSettings.objects.filter(owner_id=webapp_owner_id)

	# 增加积分
	after_applied_course = ShengjingIntegralStrategySttings.objects.get(webapp_id=member.webapp_id).after_applied_course
	integral_caculator = IntegralCaculator()
	integral_caculator.increase_member_integral(member, after_applied_course, u'在线预约课程 获得积分')

	if emails:
		email= emails[0].course_registration_email
	else:
		watchdog_error(u'没有设置课程报名邮箱    邮箱内容: %s' % content, user_id=request.user.id)
		email = u''
	if email:
		sendmail(email, u'%s 报名' % course_name, content)
	
	response = create_response(200)
	return response.get_response()


########################################################################
# get_courses:获取课程列表
########################################################################
@mobile_api(resource='mobile_courses_list', action='get')
def get_courses(request):
	count = request.GET.get('count', 10)
	page = request.GET.get('page', 1)
	webapp_owner_id = request.GET.get('webapp_owner_id', 1)
	try:
		courses, has_next = crm_api_views.list_course(page, 10000, 60)
	except:
		watchdog_error(u'crm_api_views.list_course 错误！！{}'.format(unicode_full_stack()))
		response = create_response(500)
		response.errMsg = u'获取数据失败'
		return response.get_response()
	
	shengjing_courses = ShengjingCourseRelation.objects.filter(owner_id=webapp_owner_id)
	shengjing_course_id2course = dict([(c.course_id, c) for c in shengjing_courses])
	shengjing_course_id2config = dict([(course.course_id, course.config)for course in shengjing_courses])
	cur_courses = []
	for c in courses:
		if c['id'] in shengjing_course_id2course:
			c['cover_pic_url'] = shengjing_course_id2config[c['id']].course_cover_pic_url
			c['introduction'] = shengjing_course_id2config[c['id']].introduction
			cur_courses.append(c)
	response = create_response(200)
	response.data.items = cur_courses
	response.data.pageinfo.has_next = has_next
	
	return response.get_response()


########################################################################
# get_study_plan:获取课程计划
########################################################################
@mobile_api(resource='study_plan', action='get')
def get_study_plan(request):
	if hasattr(request, 'member'):
		member = request.member
	else:
		member_id = request.GET.get('member_id', '')
		try:
			member = member_module_api.get_member_by_id(int(member_id))
		except:
			response = create_response(500)
			response.errmsg = u'获取不到会员信息'
			return response.get_response()

	company = request.GET.get('company_name')
	status = request.GET.get('status', 0)
	_, member_info = get_binding_info_by_member(member)
	if member_info:
		phone_number = member_info.phone_number
	else:
		phone_number = None
		
	#是否是决策人	
	try:
		is_leader = crm_api_views.is_leader(member_info.phone_number, company)
	except:
		watchdog_error(u'盛景获取课程计划判断是否是决策人API出错')
		is_leader = False
	if is_leader:
		try:
			courses = crm_api_views.get_learning_plan(phone_number, company, status)
			response = create_response(200)
			response.data.items = courses
		except: 
			response = create_response(500)
			response.errMsg = u'获取数据失败'
	else:
		response = create_response(501)
		response.errMsg = u'您尚未购买盛景课程<br/>或者您不是企业决策人'
		
	
		
	return response.get_response()

