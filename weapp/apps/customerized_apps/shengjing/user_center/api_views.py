# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random

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

from watchdog.utils import watchdog_fatal, watchdog_error

from shengjing.models import *

from apps.register import api

########################################################################
#send_captcha: 发送验证码
########################################################################
@api(resource='score', action='modify')
def update_settings(request):
	response = create_response(200)
	data = dict()
	binding_for_father = request.POST.get('binding_for_father', 0) 
	become_member_of_shengjing_for_father = request.POST.get('become_member_of_shengjing_for_father', 0) 
	after_applied_course = request.POST.get('after_applied_course', 0) 
	try:
		ShengjingIntegralStrategySttings.objects.filter(webapp_id=request.user.get_profile().webapp_id).update(binding_for_father=binding_for_father,become_member_of_shengjing_for_father=become_member_of_shengjing_for_father,after_applied_course=after_applied_course)
	except:
		response = create_response(500)
		notify_msg = u"修改积分配置失败 cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
	return response.get_response()

