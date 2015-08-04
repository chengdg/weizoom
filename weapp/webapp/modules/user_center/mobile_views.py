# -*- coding: utf-8 -*-
"""@package webapp.modules.user_center.mobile_views
微信页面“用户中心”对应的view

"""

#import time
#from datetime import timedelta, datetime, date
#import urllib, urllib2
import os
#import json
#from webapp.modules.cms.models import SpecialArticle

#from django.http import HttpResponseRedirect, HttpResponse, Http404
#from django.template import Context, RequestContext
#from django.contrib.auth.decorators import login_required, permission_required
#from django.conf import settings
#from django.shortcuts import render_to_response
#from django.contrib.auth.models import User, Group, Permission
#from django.contrib import auth
#from django.db.models import Q

#from core.jsonresponse import JsonResponse, create_response
#from core.dateutil import get_today
#from core.exceptionutil import full_stack, unicode_full_stack

from modules.member.member_decorators import member_required#binding_required
from webapp.modules.user_center import request_util


template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]


@member_required
#@binding_required
def get_user_info(request):
	"""
	个人信息
	"""
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_user_info(request)



########################################################################
# edit_ship_info: 修改收货人信息
########################################################################
@member_required
def edit_ship_info(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.edit_ship_info(request)


########################################################################
# save_ship_info: 保存收货人信息
########################################################################
@member_required
def save_ship_info(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.save_ship_info(request)


########################################################################
# get_integral_log: 获取会员积分使用日志
########################################################################
@member_required
def get_integral_log(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_integral_log(request)


########################################################################
# get_member_grade: 会员等级页
########################################################################
def get_member_grade(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_member_grade(request)


########################################################################
# get_integral_grade: 积分指南页
########################################################################
def get_integral_grade(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_integral_grade(request)


########################################################################
# get_user_guide: 获得用户指南页
########################################################################
def get_user_guide(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_user_guide(request)


########################################################################
# help_page: 帮助中心
########################################################################
def get_help(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.help_page(request)

########################################################################
# feed_back_page: 意见反馈
########################################################################
def get_feed_back(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.feed_back_page(request)

########################################################################
# get_integral_introduction: 获取积分介绍
########################################################################
@member_required
def get_integral_introduction(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_integral_introduction(request)

@member_required
def get_wishlist(request):
	"""
	获取会员收藏
	"""
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_wishlist(request)

@member_required
def get_binding_page(request):
	"""
	绑定页面
	"""
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_binding_page(request)

#@binding_required
@member_required
def get_binded_user_info(request):
	"""
	绑定信息
	"""
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_binded_user_info(request)

@member_required
def get_refueling_page(request):
	"""
	加油活动页面
	"""
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_refueling_page(request)

