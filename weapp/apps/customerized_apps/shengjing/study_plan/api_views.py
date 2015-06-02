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
from core import apiview_util

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

from apps.register import api
from shengjing.crm_api import api_views as crm_api_views

########################################################################
# get_courses:
########################################################################
@api(resource='course_list', action='get')
def get_courses(request):
    shengjing_course_configs = ShengjingCourseConfig.objects.filter(owner=request.user).order_by('-update_time')
    
    count_per_page = int(request.GET.get('count_per_page', 15))
    cur_page = int(request.GET.get('page', '1'))
    pageinfo, shengjing_course_configs = paginator.paginate(shengjing_course_configs, cur_page, count_per_page, query_string=request.META['QUERY_STRING']) 
    
    response = create_response(200)
    cur_shengjing_course_configs = []
    for config in shengjing_course_configs:
        cur_course_config = JsonResponse()
        cur_course_config.id = config.id
        cur_course_config.name = config.name
        cur_course_config.created_at = config.created_at.strftime('%Y-%m-%d')
        cur_course_config.update_time = config.update_time.strftime('%Y-%m-%d')
        cur_shengjing_course_configs.append(cur_course_config)
    
    response.data.items = cur_shengjing_course_configs
    response.data.sortAttr = request.GET.get('sort_attr', '-display_index')
    response.data.pageinfo = paginator.to_dict(pageinfo)
    
    return response.get_response()


########################################################################
# get_shengjing_courses:
########################################################################
@api(resource='shengjing_course_list', action='get')
def get_shengjing_courses(request):
    try:
        courses, _ = crm_api_views.list_course(1, 100000, -1)
        response = create_response(200)
        response.data.items = courses
    except:
        response = create_response(500)
        response.errMsg = u'获取数据失败'
    
    return response.get_response()


########################################################################
# update_course_display_index: 修改排列顺序
########################################################################
@login_required
@api(resource='course_display_index', action='modify')
def update_course_display_index(request): 
    src_id = request.GET.get('src_id', None)
    dst_id = request.GET.get('dst_id', None)

    if not src_id or not dst_id:
        response = create_response(500)
        response.errMsg = u'invalid arguments: src_id(%s), dst_id(%s)' % (src_id, dst_id)
        return response.get_response()        

    src_id = int(src_id)
    dst_id = int(dst_id)
    if dst_id == 0:
        #dst_id = 0, 将src的display_index设置得比第一个数据的display_index大即可
        first_course = ShengjingCourse.objects.filter(owner=request.user).order_by('-display_index')[0]
        if first_course.id != src_id:
            ShengjingCourse.objects.filter(id=src_id).update(display_index=first_course.display_index+1)
    else:
        #dst_id不为0，交换src, dst的display_index
        id2course = dict([(p.id, p) for p in ShengjingCourse.objects.filter(id__in=[src_id, dst_id])])
        ShengjingCourse.objects.filter(id=src_id).update(display_index=id2course[dst_id].display_index)
        ShengjingCourse.objects.filter(id=dst_id).update(display_index=id2course[src_id].display_index)

    response = create_response(200)
    return response.get_response()  


########################################################################
# update_course_display_index: 修改排列顺序
########################################################################
@login_required
@api(resource='course', action='delete')
def delete_course(request):  
    id = request.POST.get('id', '')
    ShengjingCourseConfig.objects.filter(id=id).delete()
    
    response = create_response(200)
    return response.get_response()  
    
    
def call_api(request):
    api_function = apiview_util.get_api_function(request, globals())
    return api_function(request)