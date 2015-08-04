# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
from webapp.modules.cms.models import SpecialArticle

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

from models import *

from settings import FIRST_NAV_NAME
from settings import LEFT_NAVS as HOME_SECOND_NAVS

from apps.register import api, view_func

########################################################################
# get_link_all: 临时加入链接
########################################################################
@login_required
def get_link_all(request):

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': HOME_SECOND_NAVS,
		'second_nav_name': 'link_all',
	})
	return render_to_response('editor/link_all.html' , c)

########################################################################
# list_apps: 
########################################################################
@login_required
def list_apps(request):

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': HOME_SECOND_NAVS,
		'second_nav_name': 'integral_settings'
	})
	return render_to_response('apps.html' , c)


