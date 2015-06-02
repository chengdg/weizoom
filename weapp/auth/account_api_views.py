# -*- coding: utf-8 -*-
"""@package auth.account_api_view
部门员工模块的API的实现文件
"""

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string
import operator

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from account import models as account_models
from models import *
from core import paginator
import export
from core.restful_url_route import *
from core.jsonresponse import create_response


COUNT_PER_PAGE = 20


@api(app='auth', resource='department', action='create')
@login_required
def create_department(request):
	"""
	创建部门

	Method: POST

	@param name 部门名
	"""
	department = Department.objects.create(
		owner = request.manager,
		name = request.POST['name']
	)

	response = create_response(200)
	response.data = {
		'id': department.id,
		'name': department.name
	}
	return response.get_response()


@api(app='auth', resource='department', action='delete')
@login_required
def delete_department(request):
	"""
	删除部门

	Method: POST

	@param id 部门id
	"""
	Department.objects.filter(owner=request.manager, id=request.POST['id']).delete()

	response = create_response(200)
	return response.get_response()


@api(app='auth', resource='department', action='update')
@login_required
def update_department(request):
	"""
	更新部门

	Method: POST

	@param id 部门id
	@param name 部门名
	"""
	Department.objects.filter(owner=request.manager, id=request.POST['id']).update(name=request.POST['name'])

	response = create_response(200)
	return response.get_response()


@api(app='auth', resource='department_users', action='get')
@login_required
def get_department_users(request):
	"""
	获得部门员工列表，员工包括启用和停用的员工，按添加时间倒序排列

	Method: GET

	@param id 部门id, 若id为0，则获取所有部门员工
	"""
	department_id = int(request.GET.get('id', 0))
	if department_id == 0:
		user_ids = [relation.user_id for relation in DepartmentHasUser.objects.filter(owner=request.manager)]
	else:
		user_ids = [relation.user_id for relation in DepartmentHasUser.objects.filter(owner=request.manager, department_id=department_id)]
	users = list(User.objects.filter(id__in=user_ids))
	users.sort(lambda x,y: cmp(y.id, x.id))

	#根据user.profile.is_active过滤
	id2user = dict([(user.id, user) for user in users])
	for profile in account_models.UserProfile.objects.filter(user_id__in=user_ids):
		id2user[profile.user_id].profile = profile
	users = [user for user in users if user.profile.is_active]

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, users = paginator.paginate(users, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	#填充user的角色信息
	id2user = dict()
	user_ids = []
	for user in users:
		user.roles = []
		id2user[user.id] = user
		user_ids.append(user.id)
	id2role = dict([(role.id, role) for role in Group.objects.filter(owner=request.manager)])
	for relation in UserHasGroup.objects.filter(user_id__in=user_ids):
		user = id2user[relation.user_id]
		role = id2role[relation.group_id]
		user.roles.append({
			"id": role.id,
			"name": role.name
		})

	#构造返回数据
	items = []
	for user in users:
		items.append({
			"id": user.id,
			"name": user.first_name,
			"is_active": user.is_active,
			"roles": user.roles
		})

	response = create_response(200)
	response.data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'sortAttr': '',
		'data': {}
	}
	return response.get_response()


@api(app='auth', resource='account_status', action='update')
@login_required
def inactive_account(request):
	"""
	更新用户状态

	Method: POST

	@param id 用户id
	@param status 用户状态：可取active(启用), inactive(停用), delete(删除)三种

	@note 启用状态：用户可登录系统，由user.is_active=True表示
	@note 停用状态: 用户不可登录系统，但在部门员工列表中可见，由user.is_active=False表示
	@note 删除状态：用户不可登录系统，在部门员工列表中也不可见，由user.is_active=False, user_profile.is_active=False表示
	"""
	user_id = request.POST['id']
	profile = account_models.UserProfile.objects.get(user_id=user_id)
	if profile.manager_id != request.manager.id:
		return create_response(500).get_response()

	status = request.POST['status']
	if status == 'active':
		User.objects.filter(id=user_id).update(is_active=True)
	elif status == 'inactive':
		User.objects.filter(id=user_id).update(is_active=False)
	elif status == 'delete':
		User.objects.filter(id=user_id).update(is_active=False)
		account_models.UserProfile.objects.filter(user_id=user_id).update(is_active=False)

	response = create_response(200)
	return response.get_response()