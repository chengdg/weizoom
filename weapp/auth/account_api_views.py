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
from django.db.utils import IntegrityError

from account import models as account_models
from models import *
from core import paginator
import export
from core.restful_url_route import *
from core.jsonresponse import create_response
from watchdog.utils import watchdog_error


COUNT_PER_PAGE = 20


@api(app='auth', resource='department', action='create')
@login_required
def create_department(request):
	"""
	创建部门

	Method: POST

	@param name 部门名
	"""
	count = Department.objects.filter(owner = request.manager, name = request.POST['name']).count()
	if count:
		response = create_response(500)
		response.data = {"msg": u'部门名称重复'}
	else:
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

	count = Department.objects.filter(owner = request.manager, name = request.POST['name']).exclude(id=request.POST['id']).count()
	if count:
		response = create_response(500)
		response.data = {"msg": u'部门名称重复'}
	else:
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
		relations = DepartmentHasUser.objects.filter(owner=request.manager)
	else:
		relations = DepartmentHasUser.objects.filter(owner=request.manager, department_id=department_id)
	user_ids = []
	userid2departmentid = dict()
	for relation in relations:
		user_ids.append(relation.user_id)
		userid2departmentid[relation.user_id] = relation.department_id

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
		user.role_name = ''
		id2user[user.id] = user
		user_ids.append(user.id)
	id2role = dict([(role.id, role) for role in Group.objects.filter(owner=request.manager)])
	for relation in UserHasGroup.objects.filter(user_id__in=user_ids):
		user = id2user[relation.user_id]
		role = id2role[relation.group_id]
		if len(user.role_name) > 0 and user.role_length == 1:
			user.role_name += '及其他'
			user.role_length = 2
		elif not hasattr(user, 'role_length'):
			user.role_name = role.name
			user.role_length = 1

	id2departmentname = dict([(department.id, department.name) for department in Department.objects.filter(owner=request.manager)])
	#构造返回数据
	items = []
	for user in users:
		items.append({
			"id": user.id,
			"name": user.first_name,
			"login_name": user.username,
			"is_active": user.is_active,
			"role_name": user.role_name,
			"department_name": id2departmentname.get(userid2departmentid[user.id], '')
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
		for user in User.objects.filter(id=user_id):
			# .update(is_active=False, username=F('username')+u'abc')
			user.is_active = False
			user.last_name = str(time.time()).split('.')[0]
			user.username += user.last_name
			user.save()
		account_models.UserProfile.objects.filter(user_id=user_id).update(is_active=False)
		# 更新主账号的子账号数量
		request.user_profile.sub_account_count += 1
		request.user_profile.save()

	response = create_response(200)
	return response.get_response()


@api(app='auth', resource='account', action='create')
@login_required
def create_account(request):
	#创建user
	username = request.POST['username']
	first_name = request.POST['name']
	password = request.POST['password']

	msg = None
	try:
		user = User.objects.create_user(username, 'none@weizoom.com', password, first_name=first_name)
	except IntegrityError:
		msg = u'账户名称已存在'
	if request.user_profile.sub_account_count < 1:
		msg = u'子账号数目已超过限额'
	if msg:
		response = create_response(500)
		response.data = {"msg": msg}
		return response.get_response()

	# 更新主账号的子账号数量
	request.user_profile.sub_account_count -= 1
	request.user_profile.save()

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

	response = create_response(200)
	return response.get_response()


@api(app='auth', resource='account', action='update')
@login_required
def update_account(request):
	user_id = request.POST['id']
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


	response = create_response(200)
	return response.get_response()

@api(app='auth', resource='account_password', action='update')
@login_required
def update_account_password(request):
	id = request.POST.get("id", None)
	password = request.POST.get("password", None)
	if id and password:
		try:
			sub_account = User.objects.get(id=id)
			sub_profile = sub_account.get_profile()
			if sub_profile.manager_id == request.manager.id:
				sub_account.set_password(password)
				sub_account.save()
			else:
				watchdog_error(u"所需修改密码的子帐号(id:%s)不属于当前管理帐号(manager_id:%s)" % (id, str(sub_profile.manager_id)), "mall")
				return create_response(500).get_response()
		except:
			watchdog_error(u"需要修改的子帐号(id:%s)不存在" % id, "mall")
			return create_response(500).get_response()
		return create_response(200).get_response()
	else:
		watchdog_error(u"所需修改的子帐号ID或者password不存在", "mall")
		return create_response(500).get_response()