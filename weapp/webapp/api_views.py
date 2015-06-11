# -*- coding: utf-8 -*-
"""@package webapp.api_views

"""

#import logging
#import time
#from datetime import timedelta, datetime, date
#import urllib, urllib2
#import os
#import json
#import subprocess
#import shutil
#import base64
#import random

#from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.template import Context, RequestContext
#from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
#from django.conf import settings
#from django.shortcuts import render_to_response
from django.contrib.auth.models import User
#from django.contrib import auth

from models import *
#from account.models import UserProfile
#from product.models import Product
#from product.models import UserHasProduct
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

from weixin.message.message.module_api import get_realtime_unread_count
from mall.module_api import get_unread_order_count
from notice.module_api import get_unread_notice_count

from watchdog.utils import watchdog_debug

@login_required
def get_unread_count_notify(request):
	"""
	获取未读的订单数(deprecated)
	
	"""
	try:
		unread_realtime_count = get_realtime_unread_count(request.user)
		unread_notice_count = get_unread_notice_count(request.user)
		unread_order_count = get_unread_order_count(request.user.id)

		response = create_response(200)
		response.data = {
			'unread_realtime_count': unread_realtime_count,
			'unread_order_count': unread_order_count,
			'unread_notice_count': unread_notice_count
			}
		watchdog_debug("response.data={}".format(response.data))
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
	return response.get_response()


def get_homepage_info(request):
	webapp_owner = User.objects.get(username=request.GET['webapp_owner_name'])
	homepage_workspace = Workspace.objects.get(owner=webapp_owner, inner_name='home_page')
	homepage_project = Project.objects.get(workspace=homepage_workspace, inner_name=homepage_workspace.template_name)

	response = create_response(200)
	response.data = {
		'project_id': homepage_project.id,
		'webapp_owner_id': homepage_project.owner_id
	}

	return response.get_response()

