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

ACCOUNT_AUTH_FIRST_NAV = 'auth'
ACCOUNT_AUTH_HELP_NAV = 'accountToHelp'
ACCOUNT_AUTH_ROLE_NAV = 'roleManagement'
ACCOUNT_AUTH_ACCOUNT_NAV = 'employeeManagement'


NAV = {
	'section': u'账号权限',
	'navs': [
		{
			'name': ACCOUNT_AUTH_HELP_NAV,
			'title': u'账号帮助',
			'url': '/auth/account_help/get/',
			'need_permissions': ['view_account_help']
		},
		{
			'name': ACCOUNT_AUTH_ROLE_NAV,
			'title': u'角色管理',
			'url': '/auth/roles/get/',
			'need_permissions': ['manage_role']
		},
		{
			'name': ACCOUNT_AUTH_ACCOUNT_NAV,
			'title': u'员工管理',
			'url': '/auth/departments/get/',
			'need_permissions': ['manage_account']
		}
	]
}

########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.user.username == 'manager':
		pass
	else:
		second_navs = [NAV]#webapp_module_views.get_modules_page_second_navs(request)

	return second_navs

