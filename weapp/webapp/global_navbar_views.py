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
def edit_global_navbar(request):
	c = RequestContext(request, {
		'first_nav_name': WEBAPP_TEMPLATE_FIRST_NAV_NAME,
		'second_navs': WEBAPP_TEMPLATE_SECOND_NAVS,
		'second_nav_name': 'webapp_global_navbar'
	})
	return render_to_response('webapp/global_navbar.html', c)