# -*- coding: utf-8 -*-
"""
@package auth.permission_api_views

权限的API实现
"""

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import copy
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

from models import *
from core import paginator
import export
from core.restful_url_route import *
from core.jsonresponse import create_response


COUNT_PER_PAGE = 20


def __build_permission_tree():
	"""
	构建权限列表的tree数据结构，构建完后的数据结构如

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
	tree = {
		"id": 0,
		"level": 0,
		"permissions": [{
			"id": 1, 
			"level":, 1
			"name": u"模块1",
			"code_name": u"module1",
			"permissions": [{
				"id": 2, 
				"level": 2,
				"name": u"子模块1",
				"code_name": u"sub_module1",
				"permissions": [{
					"id": 3,
					"level": 3,
					"name": u"读权限",
					"code_name": u"read_sub_module1",
				}, {
					"id": 4,
					"level": 3,
					"name": u"写权限",
					"code_name": u"write_sub_module1",
				}, {
					"id": 5,
					"level": 3,
					"name": u"删除权限",
					"code_name": u"delete_sub_module1",
				}]
			}]
		}, {
			......
		}]
	}
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""

	id2permission = {}
	root = {"permissions":[], "level":0, "id":0}
	for db_permission in Permission.objects.all():
		permission = {
			"id": db_permission.id,
			"name": db_permission.name,
			"code_name": db_permission.code_name,
			"permissions": []
		}

		if db_permission.parent_id == 0:
			parent_permission = root
		else:
			parent_permission = id2permission[db_permission.parent_id]
		
		permission['level'] = parent_permission['level'] + 1
		parent_permission['permissions'].append(permission)
		id2permission[db_permission.id] = permission

	return root


ACTION_LABEL_TMPL = '<label class="xui-i-permission xui-i-level%(level)d"><input type="checkbox" data-id="%(id)d" data-is-leaf="%(is_leaf)s"/ %(checked)s %(disabled)s> %(name)s</label>'
VIEW_LABEL_TMPL = '<div class="pr xui-i-permission xui-i-level%(level)d" data-id="%(id)d"><em class="xui-i-line%(level)d"></em>%(name)s</div>'
def __walk_tree(node_list, node, role_permission_ids, user_permission_ids, type, options):
	"""
	使用breadth first策略，递归遍历tree的节点，并生成html代码

	type = view

		生成浏览用的html代码，html中不显示所有权限，只显示在role_permission_ids中出现的权限

		注意: 这时，role_permission_ids已经过__fill_parent_permissions的处理，填充了必要的父级权限

	type = action

		生成操作用的html代码，html中显示所有权限，在role_permission_ids中的权限的复选框会被选中
	"""
	node_id = node['id']
	is_root = (node_id == 0)
	permissions = node['permissions']
	del node['permissions']
	is_leaf = (len(permissions) == 0)
	node['is_leaf'] = "true" if is_leaf else "false"

	if not is_root:
		#如果node在role permissions或user permissions中，需要选中
		node_id = int(node_id)
		is_checked = (node_id in role_permission_ids) or (node_id in user_permission_ids)
		node['checked'] = 'checked' if is_checked else ''

		if (node_id in role_permission_ids) and ('disable_role_permission' in options):
			node['disabled'] = 'disabled'
		else:
			node['disabled'] = ''

		if (not is_leaf) and type == 'action':
			node_list.append('<div class="xa-node">')
		if type == 'action':
			html = ACTION_LABEL_TMPL % node
		else:
			html = VIEW_LABEL_TMPL % node

		if (type == 'action') or (type == 'view' and is_checked):
			node_list.append(html)

	for node in permissions:
		__walk_tree(node_list, node, role_permission_ids, user_permission_ids, type, options)
	
	if not is_root:
		if (not is_leaf) and (type == 'action'):
			node_list.append('</div>')


def __render_permission_list(tree, role_permission_ids, user_permission_ids, type, options={}):
	"""
	调用__walk_tree，渲染权限列表的html代码
	"""
	node_list = []
	__walk_tree(node_list, tree, role_permission_ids, user_permission_ids, type, options)
	return ''.join(node_list)


def __fill_parent_permissions(permission_id_set):
	"""
	填充所有必要的上一级permission
	"""
	unchecked_ids = copy.copy(permission_id_set)
	new_ids = set()
	id2permission = dict([(permission.id, permission) for permission in Permission.objects.all()])
	while True:
		for permission_id in unchecked_ids:
			permission = id2permission[permission_id]
			parent_permission_id = permission.parent_id
			if parent_permission_id == 0:
				continue

			parent_permission = id2permission[permission.parent_id]
			new_id = parent_permission.id
			if not new_id in permission_id_set:
				new_ids.add(new_id)
				permission_id_set.add(new_id)

		if len(new_ids) == 0:
			break
		else:
			unchecked_ids = new_ids
			new_ids = set()
_fill_parent_permissions = __fill_parent_permissions


@api(app='auth', resource='role_permissions', action='get')
@login_required
def get_role_permissions(request):
	"""
	获取角色的权限集合

	Method: GET

	@param type: 数据类型
		action: 操作类型，返回带checkbox的html
		view: 浏览类型，返回不带checkbox的html
	"""
	role_id = request.GET['id'].strip()
	if not role_id:
		return create_response(200).get_response()
	elif ',' in role_id:
		role_ids = role_id.split(',')
	else:
		role_ids = [role_id,]
	type = request.GET.get('type', 'view')
	role_permission_ids = set([relation.permission_id for relation in GroupHasPermission.objects.filter(group_id__in=role_ids)])
	if type == 'view':
		__fill_parent_permissions(role_permission_ids)

	permission_tree = __build_permission_tree()
	permission_list = __render_permission_list(permission_tree, role_permission_ids, set(), type)

	response = create_response(200)
	response.data = permission_list
	return response.get_response()


@api(app='auth', resource='role_permissions', action='update')
@login_required
def update_role_permissions(request):
	"""
	更新角色的权限集合

	Method: POST

	@param role_id: 角色id
	@param permission_ids: 权限id集合
	"""
	role_id = request.POST['role_id']
	permission_ids = request.POST.getlist('permission_ids[]')
	
	GroupHasPermission.objects.filter(owner=request.manager, group_id=role_id).delete()
	for permission_id in permission_ids:
		GroupHasPermission.objects.create(
			owner = request.manager,
			group_id = role_id,
			permission_id = permission_id
		)

	response = create_response(200)
	return response.get_response()


@api(app='auth', resource='account_permissions', action='get')
@login_required
def get_account_permissions(request):
	"""
	获取用户的权限集合

	Method: GET

	@param id: 用户id
	@param type: 数据类型
		action: 操作类型，返回带checkbox的html
		view: 浏览类型，返回不带checkbox的html
	@param specific_role_ids: 以,分隔的特定的角色id集合，当该参数存在时，不从数据库中取user的角色数据
	@param specific_user_permission_ids: 以,分隔的特定的权限id集合，当该参数存在时，不从数据库中取user的权限数据
	"""
	user_id = request.GET['id']
	type = request.GET.get('type', 'view')

	#
	#获取角色权限
	#
	#获得用户当前所属的role集合
	group_ids = []
	if 'specific_role_ids' in request.GET:
		#获得从POST提交的role集合
		specific_role_ids_str = request.GET.get('specific_role_ids', '').strip()
		specific_role_ids = None
		if not specific_role_ids_str:
			pass
		elif ',' in specific_role_ids_str:
			specific_role_ids = [int(role_id) for role_id in specific_role_ids_str.split(',')]
		else:
			specific_role_ids = [int(specific_role_ids_str),]
		#合并以上两个role集合
		if specific_role_ids:
			group_ids = specific_role_ids
	else:
		group_ids = [relation.group_id for relation in UserHasGroup.objects.filter(user_id=user_id)]
	#获取role关联的permission集合
	role_permission_ids = set([relation.permission_id for relation in GroupHasPermission.objects.filter(group_id__in=group_ids)])
	if type == 'view':
		__fill_parent_permissions(role_permission_ids)

	#
	#获取用户权限
	#
	#获得用户的role集合
	user_permission_ids = set([relation.permission_id for relation in UserHasPermission.objects.filter(user_id=user_id)])
	if 'specific_user_permission_ids' in request.GET:
		#获得从POST提交的role集合
		specific_user_permission_ids = None
		specific_user_permission_ids_str = request.GET.get('specific_user_permission_ids', '').strip()
		if ',' in specific_user_permission_ids_str:
			specific_user_permission_ids = [int(permission_id) for permission_id in specific_user_permission_ids_str.split(',')]
		else:
			specific_user_permission_ids = [int(specific_user_permission_ids_str),]
		if specific_user_permission_ids:
			user_permission_ids.update(set(specific_user_permission_ids))
	if type == 'view':
		__fill_parent_permissions(user_permission_ids)

	options = {
		'disable_role_permission': True
	}
	permission_tree = __build_permission_tree()
	permission_list = __render_permission_list(permission_tree, role_permission_ids, user_permission_ids, type, options)

	response = create_response(200)
	response.data = permission_list
	return response.get_response()


@api(app='auth', resource='account_permissions', action='update')
@login_required
def update_account_permissions(request):
	"""
	更新用户的权限集合

	Method: POST

	@param user_id: 角色id
	@param permission_ids: 权限id集合
	"""
	user_id = request.POST['user_id']
	permission_ids = request.POST.getlist('permission_ids[]')
	
	UserHasPermission.objects.filter(owner=request.manager, user_id=user_id).delete()
	for permission_id in permission_ids:
		UserHasPermission.objects.create(
			owner = request.manager,
			user_id = user_id,
			permission_id = permission_id
		)

	response = create_response(200)
	return response.get_response()