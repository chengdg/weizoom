# -*- coding: utf-8 -*-
__author__ = "liupeiyu"

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core import apiview_util
from django.contrib.auth.decorators import login_required
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.models import User
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions


#===============================================================================
# get_user_all : 获取所有账号信息
#===============================================================================
def get_user_all(request):
	users = User.objects.exclude(username__in=['admin'])
	
	items = []
	for user in users:
		items.append({
			'id': user.id,
			'name': user.username
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
	}
	return response.get_response()


#===============================================================================
# get_has_weizoom_card_permissions_user : 获取有微众卡权限的用户
#===============================================================================
def get_has_weizoom_card_permissions_user(request):
	permissions = AccountHasWeizoomCardPermissions.objects.all()
	user2id = dict([(u.id, u) for u in User.objects.all()])

	items = []
	for permission in permissions:
		user = user2id.get(permission.owner_id)
		items.append({
			'id': user.id,
			'name': user.username
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
	}
	return response.get_response()


#===============================================================================
# update_weizoom_card_account_permission : 更新用户使用微众卡的权限
#===============================================================================
def update_weizoom_card_account_permission(request):	
	owner_ids = request.GET['owner_ids']
	if not owner_ids or (owner_ids is ''):
		AccountHasWeizoomCardPermissions.objects.all().delete()
	else:
		ids = owner_ids.split(',')
		AccountHasWeizoomCardPermissions.objects.exclude(owner_id__in=ids).delete()
		permission_owner_ids = [int(a.owner_id) for a in AccountHasWeizoomCardPermissions.objects.filter(owner_id__in=ids)]
		
		for id in ids:
			if int(id) not in permission_owner_ids:
				AccountHasWeizoomCardPermissions.objects.create(
					owner_id=id,
					is_can_use_weizoom_card=True
				)

	response = create_response(200)
	return response.get_response()


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)
