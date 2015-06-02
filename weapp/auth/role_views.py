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
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from models import *
import export
from core.restful_url_route import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.ACCOUNT_AUTH_FIRST_NAV


########################################################################
# get_roles: 获得角色列表
########################################################################
@view(app='auth', resource='roles', action='get')
@login_required
def get_roles(request):
	roles = list(Group.objects.filter(owner=request.manager))
	roles.sort(lambda x,y: cmp(y.id, x.id))
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.ACCOUNT_AUTH_ROLE_NAV,
		'roles': roles
	})

	return render_to_response('auth/roles.html', c)
