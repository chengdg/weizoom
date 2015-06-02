# -*- coding: utf-8 -*-

from datetime import timedelta, datetime, date

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from apps.customerized_apps.shengjing.user_center.util import get_binding_info_by_member
from apps.customerized_apps.shengjing.models import *
from apps.customerized_apps.shengjing.crm_api import api_views as crm_api_views
from django.contrib.auth.decorators import login_required, permission_required
from apps.customerized_apps.shengjing.views import *

from shengjing.settings import FIRST_NAV_NAME
from shengjing.settings import LEFT_NAVS as HOME_SECOND_NAVS

from apps.register import view_func

from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack

########################################################################
# list_course: 课程编辑列表页
########################################################################
@login_required
@view_func(resource='course_list', action='get')
def list_course(request):
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': HOME_SECOND_NAVS,
		'second_nav_name': 'course_settings'
	})
	return render_to_response('editor/list_course.html', c) 


########################################################################
# add_course: 课程编辑
########################################################################
@login_required
@view_func(resource='course', action='create')
def add_course(request):
	if request.POST:
		course_ids = request.POST.get('course_ids', '0')
		name = request.POST.get('name', '0')
		course_cover_pic_url = request.POST.get('course_cover_pic_url', '')
		introduction = request.POST.get('course_des', '0')
		detail = request.POST.get('detail', '')
		non_participants = request.POST.get('non_participants', 'off')
		if non_participants == 'on':
			non_participants = 1
		else:
			non_participants = 0

		config = ShengjingCourseConfig.objects.create(
			owner = request.user,
			name = name,
			description = detail,
			course_cover_pic_url = course_cover_pic_url,
			introduction = introduction,
			non_participants = non_participants
			)
		course_ids = course_ids.split(',')
		ShengjingCourseRelation.objects.filter(owner=request.user, course_id__in=course_ids).delete()
		for id in course_ids:
			ShengjingCourseRelation.objects.create(
				owner = request.user,
				config = config,
				course_id = id
				)
		return HttpResponseRedirect('/apps/shengjing/?module=study_plan&resource=course_list&action=get')
	else:	
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': HOME_SECOND_NAVS,
			'second_nav_name': 'course_settings',
		})
		return render_to_response('editor/edit_course.html', c)
	
	
########################################################################
# edit_course: 课程编辑
########################################################################
@login_required
@view_func(resource='course', action='modify')
def edit_course(request):
	config_id = request.GET.get('config_id', '0')
	if request.POST:
		course_ids = request.POST.get('course_ids', '0')
		name = request.POST.get('name', '0')
		detail = request.POST.get('detail', '')
		course_cover_pic_url = request.POST.get('course_cover_pic_url', '')
		introduction = request.POST.get('course_des', '0')
		non_participants = request.POST.get('non_participants', 'off')
		if non_participants == 'on':
			non_participants = 1
		else:
			non_participants = 0

		config = ShengjingCourseConfig.objects.get(id=int(config_id))
		config.name = name
		config.description = detail
		config.introduction = introduction
		config.course_cover_pic_url=course_cover_pic_url
		config.update_time = datetime.now()
		config.non_participants = non_participants
		config.save()
		course_ids = course_ids.split(',')
		ShengjingCourseRelation.objects.filter(owner=request.user, config_id=config_id).delete()
		ShengjingCourseRelation.objects.filter(owner=request.user, course_id__in=course_ids).delete()
		for id in course_ids:
			ShengjingCourseRelation.objects.create(
				owner = request.user,
				config = config,
				course_id = id
				)
		return HttpResponseRedirect('/apps/shengjing/?module=study_plan&resource=course_list&action=get')
	else:
		config = ShengjingCourseConfig.objects.get(id=config_id)
		course_ids = [str(course.course_id) for course in ShengjingCourseRelation.objects.filter(config=config)]
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': HOME_SECOND_NAVS,
			'second_nav_name': 'course_settings',
			'course': config,
			'course_ids': ','.join(course_ids)
		})
		return render_to_response('editor/edit_course.html', c) 