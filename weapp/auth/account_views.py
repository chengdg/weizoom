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
	sub_account_count = account_models.UserProfile.objects.filter(manager_id = request.user.id).count()
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
	if request.POST:
		#创建user
		username = request.POST['username']
		first_name = request.POST['name']
		password = request.POST['password']
		user = User.objects.create_user(username, 'none@weizoom.com', password, first_name=first_name)

		profile = user.get_profile()
		profile.manager_id = request.manager.id
		profile.is_mp_registered = True
		profile.save()

		#处理<department, user>关系
		department_id = request.POST['department']
		DepartmentHasUser.objects.create(
			owner = request.manager,
			department_id = department_id,
			user = user
		)

		#处理<user, group>关系
		role_ids = request.POST.get('role_ids', '').split(',')
		for role_id in role_ids:
			role_id = role_id.strip()
			if not role_id:
				continue
			UserHasGroup.objects.create(
				user = user,
				group_id = role_id
			)

		return HttpResponseRedirect('/auth/departments/get/?focus=%s' % department_id)
	else:
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
	if request.POST:
		user_id = request.GET['id']

		#更新user
		User.objects.filter(id=user_id).update(first_name=request.POST['name'])

		#更新<department, user>关系 
		department_id = request.POST['department']
		relation = DepartmentHasUser.objects.get(owner=request.manager, user_id=user_id)
		if relation.department_id != department_id:
			DepartmentHasUser.objects.filter(owner=request.manager, user_id=user_id).update(department=department_id)

		#更新<user, group>关系
		UserHasGroup.objects.filter(user_id=user_id).delete()
		role_ids = request.POST.get('role_ids', '').split(',')
		for role_id in role_ids:
			role_id = role_id.strip()
			if not role_id:
				continue
			UserHasGroup.objects.create(
				user_id = user_id,
				group_id = role_id
			)

		#更新<user, permission>关系
		UserHasPermission.objects.filter(owner=request.manager, user_id=user_id).delete()
		user_permission_ids_str = request.POST.get('user_permission_ids', "unmodified").strip()
		if user_permission_ids_str and (not user_permission_ids_str == 'unmodified'):
			user_permission_ids = user_permission_ids_str.split(',')
			for permission_id in user_permission_ids:
				UserHasPermission.objects.create(
					owner = request.manager,
					user_id = user_id,
					permission_id = permission_id
				)


		return HttpResponseRedirect('/auth/departments/get/?focus=%s' % department_id)
	else:
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