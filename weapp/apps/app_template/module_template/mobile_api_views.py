# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
__STRIPPER_TAG__
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core import chartutil
__STRIPPER_TAG__
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
__STRIPPER_TAG__
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert, watchdog_fatal
__STRIPPER_TAG__
from apps.register import api, mobile_api
from termite import pagestore as pagestore_manager
from apps import viper_util
from {{app_name}}.models import *
from {{app_name}}.mysql_models import *
from {{app_name}} import settings as app_settings
__STRIPPER_TAG__
__STRIPPER_TAG__


{% for page in pages %}
{% if page.component.model.type == 'edit_page' %}
TARGET_RESOURCE = "{{page.component.model.title}}"
__STRIPPER_TAG__
__STRIPPER_TAG__
{% endif %}
{% endfor %}


################################################
# get_record_meta_data: 获取记录元信息
################################################
@mobile_api(resource='record_meta_data', action='get')
def get_record_meta_data(request):
	request.target_resource = TARGET_RESOURCE
	record = viper_util.get_record(request, app_settings)
	#filter __${variable} from record
	data = {}
	for key in record:
		if not key.startswith('__'):
			continue
		data[key] = record[key]

	response = create_response(200)
	response.data = data
	return response.get_response()