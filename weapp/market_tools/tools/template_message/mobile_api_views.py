# -*- coding: utf-8 -*-

__author__ = 'bert'

from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core.exceptionutil import unicode_full_stack
from core import core_setting
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from models import *
from modules.member.integral import increase_member_integral
from mall.models import *
from account.views import save_base64_img_file_local_for_webapp

