# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack

from webapp.modules.cms import request_util


template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]


########################################################################
# get_category: 显示“文章列表”页面
########################################################################
def get_category(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_article_list(request)


########################################################################
# get_article: 显示“文章内容”页面
########################################################################
def get_article(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_article(request)


########################################################################
# get_demo_home_page: 显示“演示首页”页面
########################################################################
def get_demo_home_page(request):
	request.template_dir = '%s/%s' % (TEMPLATE_DIR, request.template_name)
	return request_util.get_demo_home_page(request)