# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from views import WEBAPP_TEMPLATE_SECOND_NAVS, WEBAPP_TEMPLATE_FIRST_NAV_NAME
from models import *
from core.jsonresponse import create_response, JsonResponse


@login_required
def update_global_navbar(request):
	data = request.POST['data']
	is_enable = (request.POST['is_enable'] == "1")
	if GlobalNavbar.objects.filter(owner=request.user).count() > 0:
		GlobalNavbar.objects.filter(owner=request.user).update(content=data, is_enable=is_enable)
	else:
		GlobalNavbar.objects.create(
			owner = request.user,
			content = data,
			is_enable = is_enable
		)

	return create_response(200).get_response()


@login_required
def get_global_navbar(request):
	try:
		global_navbar = GlobalNavbar.objects.get(owner=request.user)
	except:
		global_navbar = GlobalNavbar()
		global_navbar.content = "[]"
		global_navbar.is_enable = False

	response = create_response(200)
	response.data = {
		'is_enable': global_navbar.is_enable, 
		'menus': json.loads(global_navbar.content)
	}

	return response.get_response()