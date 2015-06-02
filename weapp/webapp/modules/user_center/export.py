# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from webapp import views as webapp_views

from modules.member import models as member_models

NAV = {
	'section': u'会员中心',
	'navs': [
		{
			'name': 'usercenter-memberlist',
			'title': u'会员列表',
			'url': '/webapp/user_center/',
		},
		{
			'name': 'usercenter-grades',
			'title': u'会员等级',
			'url': '/webapp/user_center/grades/',
		},
		{
			'name': 'usercenter-tags',
			'title': u'会员分组',
			'url': '/webapp/user_center/tags/',
		},
	]
}


PAGES = [
	{
		'name': member_models.ShipInfo._meta.verbose_name,
		'value': member_models.ShipInfo._meta.module_name
	}
]

########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.user.username == 'manager':
		second_navs = []
		second_navs.append(NAV)
		second_navs.append({
			'section': u'项目',
			'navs': [{
				'name': u'项目管理',
				'url': '/webapp/',
				'title': u'项目管理'
			}]
		})
	else:
		second_navs = webapp_views.get_modules_page_second_navs(request)

	return second_navs


########################################################################
# get_link_targets: 检查product名是否有重复
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=mall&webapp_owner_id=%d' % request.workspace.owner_id

	#获得页面
	pages = []
	pages.append({'text': u'用户中心页面', 'value': './?module=user_center&model=user_info&action=get&%s' % workspace_template_info})
	pages.append({'text': u'收货地址', 'value': './?module=mall&model=address&action=list&sign=material_news&%s' % workspace_template_info})
	# pages.append({'text': u'盛景入口', 'value': './?module=customerized_apps:shengjing:user_center&model=test_index&action=show&%s' % workspace_template_info})
	response.data = [
		{
			'name': u'页面',
			'data': pages
		}
	]
	return response.get_response()