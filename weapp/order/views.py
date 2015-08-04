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
from order.account.order_decorators import project_freight_required
from models import *

OPERATION_NAV_NAME = 'operation-index'

@project_freight_required
def show_index(request):
	problems = None

	c = RequestContext(request, {
		'nav_name': OPERATION_NAV_NAME,
		'problem_titles': problems,
		'freight_user': request.freight_user
	})
	return render_to_response('order/index.html', c)
