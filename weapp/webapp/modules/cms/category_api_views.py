# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil

from models import *

########################################################################
# update_category_display_index: 修改排列顺序
########################################################################
@login_required
def update_category_display_index(request):
	ids = request.GET['ids'].split('_')
	for index, id in enumerate(ids):
		Category.objects.filter(id=id).update(display_index=index+1)

	response = create_response(200)
	return response.get_response()


########################################################################
# get_categories: 获得分类列表
########################################################################
@login_required
def get_categories(request):
	query = request.GET.get('query', None)
		
	#处理排序
	sort_attr = request.GET.get('sort_attr', 'created_at');
	categories = Category.objects.filter(owner=request.user).order_by(sort_attr)

	#处理搜索
	if query:
		categories = categories.filter(name__icontains=query)
	
	items = []
	for category in  categories:
		items.append({
			'id': category.id,
			'name': category.name,
			'created_at': datetime.strftime(category.created_at, '%Y-%m-%d %H:%M')
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
		'sortAttr': sort_attr
	}
	return response.get_response()
