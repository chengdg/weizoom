# -*- coding: utf-8 -*-

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

from models import *
from core import paginator
import export
from core.restful_url_route import *
from core.jsonresponse import create_response


COUNT_PER_PAGE = 20


@api(app='auth', resource='role', action='create')
@login_required
def create_role(request):
	"""
	创建角色

	Method: POST

	@param name 角色名
	"""
	name_count = Group.objects.filter(owner = request.manager, name = request.POST['name']).count()
	if name_count:
		response = create_response(500)
		response.data = {"msg": u'角色名称重复'}
	elif Group.objects.filter(owner = request.manager).count() >= 30:
		response = create_response(500)
		response.data = {"msg": u'角色数目已超过限额'}
	else:
		group = Group.objects.create(
			owner = request.manager,
			name = request.POST['name']
		)

		response = create_response(200)
		response.data = {
			'id': group.id,
			'name': group.name
		}
	return response.get_response()


@api(app='auth', resource='role', action='delete')
@login_required
def delete_role(request):
	"""
	删除角色

	Method: POST

	@param id 角色id
	"""
	Group.objects.filter(owner=request.manager, id=request.POST['id']).delete()

	response = create_response(200)
	return response.get_response()


########################################################################
# update_role: 更新角色
########################################################################
@api(app='auth', resource='role', action='update')
@login_required
def update_role(request):
	"""
	更新角色

	Method: POST

	@param id 角色id
	@param name 角色名
	"""
	count = Group.objects.filter(owner = request.manager, name = request.POST['name']).exclude(id=request.POST['id']).count()
	if count:
		response = create_response(500)
		response.data = {"msg": u'角色名称重复'}
	else:
		Group.objects.filter(owner=request.manager, id=request.POST['id']).update(name=request.POST['name'])

		response = create_response(200)
	return response.get_response()
