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

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.dateutil import get_today


from account.models import *
from models import *

import export


COUNT_PER_PAGE = 20

# Termite GENERATED START: views

FIRST_NAV_NAME = 'webapp'

# MODULE START: category
CMS_CATEGORY_NAV = 'cms-category'

########################################################################
# list_categories: 显示文章分类列表
########################################################################
@login_required
def list_categories(request):
	categories = Category.objects.filter(owner=request.user).order_by('display_index')

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': CMS_CATEGORY_NAV,
		'categories': categories,
	})
	return render_to_response('cms/editor/categories.html', c)


########################################################################
# add_category: 添加分类
########################################################################
@login_required
def add_category(request):
	if request.POST:
		category = Category.objects.create(
			owner = request.user,
			name = request.POST.get('name', '').strip()
			#pic_url = request.POST.get('pic_url', '').strip()
		)
		#category.display_index = 0-category.id
		#category.save()

		return HttpResponseRedirect('/cms/editor/categories/')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': CMS_CATEGORY_NAV,
		})
		return render_to_response('cms/editor/edit_category.html', c)


########################################################################
# update_category: 更新分类
########################################################################
@login_required
def update_category(request, category_id):
	if request.POST:
		Category.objects.filter(owner=request.user, id=category_id).update(
			name = request.POST.get('name', '').strip()
			#pic_url = request.POST.get('pic_url', '').strip(),
		)

		return HttpResponseRedirect('/cms/editor/categories/')
	else:
		category = Category.objects.get(owner=request.user, id=category_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': CMS_CATEGORY_NAV,
			'category': category,
		})
		return render_to_response('cms/editor/edit_category.html', c)


########################################################################
# delete_category: 删除分类
########################################################################
@login_required
def delete_category(request, category_id):
	CategoryHasArticle.objects.filter(id=category_id).delete()
	Category.objects.filter(id=category_id).delete()

	return HttpResponseRedirect('/cms/editor/categories/')
# MODULE END: category
