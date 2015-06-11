# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from account import models as account_models
from models import *
import export
from core.restful_url_route import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.ACCOUNT_AUTH_FIRST_NAV


########################################################################
# get_account_help: 获得在售商品列表
########################################################################
@view(app='auth', resource='account_help', action='get')
@login_required
def get_account_help(request):
	sub_account_count = account_models.UserProfile.objects.filter(manager_id=request.user.id, is_active=True).exclude(user_id=request.user.id).count()
	remain_sub_account_count = request.user_profile.sub_account_count
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.ACCOUNT_AUTH_HELP_NAV,
		'sub_account_count': sub_account_count,
		'remain_sub_account_count': remain_sub_account_count
	})

	return render_to_response('auth/account_help.html', c)


@view(app='auth', resource='departments', action='get')
@login_required
def get_departments(request):
	"""
	部门列表页面
	"""
	departments = list(Department.objects.filter(owner=request.manager))
	departments.sort(lambda x,y: cmp(y.id, x.id))
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.ACCOUNT_AUTH_ACCOUNT_NAV,
		'departments': departments,
		'focus_department_id': request.GET.get('focus', 0)
	})

	return render_to_response('auth/departments.html', c)


@view(app='auth', resource='account', action='create')
@login_required
def create_account(request):
	"""
	新建员工页面
	"""
	roles = Group.objects.filter(owner=request.manager)
	departments =  list(Department.objects.filter(owner=request.manager))

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.ACCOUNT_AUTH_ACCOUNT_NAV,
		'roles': roles,
		'departments': departments
	})

	return render_to_response('auth/edit_account.html', c)


@view(app='auth', resource='account', action='update')
@login_required
def update_account(request):
	"""
	更新员工信息页面
	"""
	user_id = request.GET['id']

	#部门信息
	user_department_id = DepartmentHasUser.objects.get(user_id=user_id).department_id
	departments =  list(Department.objects.filter(owner=request.manager))
	for department in departments:
		if department.id == user_department_id:
			department.is_selected = True
		else:
			department.is_selected = False

	#用户信息
	user = User.objects.get(id=user_id)
	user.profile = user.get_profile()

	#角色信息
	roles = list(Group.objects.filter(owner=request.manager))
	id2role = dict([(role.id, role) for role in roles])
	for relation in UserHasGroup.objects.filter(user_id=user_id):
		id2role[relation.group_id].is_selected = True

	#用户相关的权限信息
	user_permission_ids = [str(relation.permission_id) for relation in UserHasPermission.objects.filter(user_id=user_id)]
	user.user_permission_ids_str = ','.join(user_permission_ids)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.ACCOUNT_AUTH_ACCOUNT_NAV,
		'roles': roles,
		'departments': departments,
		'account_user': user
	})

	return render_to_response('auth/edit_account.html', c)