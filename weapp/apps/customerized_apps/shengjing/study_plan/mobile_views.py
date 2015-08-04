# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from shengjing.user_center.util import get_binding_info_by_member
from shengjing.models import *
from shengjing.crm_api import api_views as crm_api_views
from modules.member.member_decorators import member_required
from watchdog.utils import watchdog_error, watchdog_info

from apps.register import mobile_view_func

from shengjing.user_center.module_api import binded_member_required
import shengjing_api_view as shengjing_api

########################################################################
# _get_template_name_and_response_data: 
########################################################################
def _get_template_name_and_response_data(request):
	member = request.member	
	binding_member,member_info = get_binding_info_by_member(member)
	response_data = dict()

	if binding_member and member_info:
		template_name = ''
	elif binding_member:
		response_data['binding_member'] = binding_member		
		template_name = 'webapp/binding_info.html'
	else:
		template_name = 'webapp/binding_page.html'	
		
	response_data['is_hide_weixin_option_menu'] = True
	
	webapp_owner_id = request.GET.get('webapp_owner_id')
	response_data['webapp_owner_id'] = webapp_owner_id

	return response_data, template_name


########################################################################
# study_plan: 学习计划
########################################################################
@member_required
@binded_member_required
@mobile_view_func(resource='study_plans', action='get')
def get_study_plan(request):
	member = request.member
	binding_member, member_info = get_binding_info_by_member(member)
	
	response_data, template_name = _get_template_name_and_response_data(request)
	
	if not template_name:
		companys = member_info.companys
		c = RequestContext(request, {
			'page_title': u'学习计划',
			'companys': companys,
			'member': member,
			'is_hide_weixin_option_menu': True
		})
		return render_to_response('webapp/study_plan.html', c)
	else:
		c = RequestContext(request, response_data)
		return render_to_response(template_name, c)	
		

########################################################################
# list_course: 课程列表
########################################################################
@member_required
@binded_member_required
@mobile_view_func(resource='mobile_courses_list', action='get')
def list_course(request):
	response_data, template_name = _get_template_name_and_response_data(request)
	if not template_name:
		c = RequestContext(request, {
			'page_title': u'课程列表',
			'is_hide_weixin_option_menu': True
		})
		return render_to_response('webapp/course_list.html', c)
	else:
		c = RequestContext(request, response_data)
		return render_to_response(template_name, c)	
	
	
########################################################################
# get_course_detail: 课程详情
########################################################################
@member_required
@binded_member_required
@mobile_view_func(resource='course_detail', action='get')
def get_course_detail(request):
	request.should_hide_footer = True
	response_data, template_name = _get_template_name_and_response_data(request)
	if not template_name:
		#获取ID为course_id的课程的详情
		course_id = request.GET.get('course_id', 0)
		try:
			course = crm_api_views.get_course(course_id)
		except:
			course = None
		#判断是否报名
		courses = ShengjingCourseRegistration.objects.filter(member_id=request.member.id, course_id=course_id)
		
		shengjing_course = ShengjingCourseRelation.objects.get(course_id=course_id, owner_id=request.webapp_owner_id)
		config = shengjing_course.config
		course['description'] = config.description
		
		binding_member, member_info = get_binding_info_by_member(request.member)
		
		if courses:
			is_apply = True
		else:
			is_apply = False
			
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
		show_referrer = True
		if phone_number:
			is_leader = True
			show_referrer = False
		else:
			is_leader = False
			if ShengjingCourseConfig.objects.get(id=shengjing_course.config_id).non_participants:
				is_leader = True
		
		c = RequestContext(request, {
			'page_title': u'课程详情',
			'course': course,
			'is_hide_weixin_option_menu': True,
			'is_apply': is_apply,
			'is_leader': is_leader,
			'show_referrer': show_referrer
		})
		return render_to_response('webapp/course_detail.html', c)
	else:
		c = RequestContext(request, response_data)
		return render_to_response(template_name, c)	
	
	
################################################
# 判断member是否为决策人
################################################
def is_leader(member_info):
	if member_info and member_info.status==LEADER:
		return True
	return False


########################################################################
# list_courses_qrcode: 课程签到列表
########################################################################
@member_required
@binded_member_required
@mobile_view_func(resource='courses_qrcode_list', action='get')
def list_courses_qrcode(request):
	response_data, template_name = _get_template_name_and_response_data(request)
	if not template_name:		
		member = request.member
		binding_member, member_info = get_binding_info_by_member(member)
		#  获取课程签到列表
		items = shengjing_api.mobile_get_invitation_list(member_info.phone_number)

		c = RequestContext(request, {
			'page_title': u'课程签到',
			'is_hide_weixin_option_menu': True,
			'items': items
		})
		return render_to_response('webapp/course_qrcode_list.html', c)
	else:
		c = RequestContext(request, response_data)
		return render_to_response(template_name, c)	
	