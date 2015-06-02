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

from watchdog.utils import watchdog_fatal, watchdog_error

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from models import *
from modules.member.util import get_member

########################################################################
# edit_member_qrcode_settings: 编辑/新建会员二维码
########################################################################
def is_complained(request):
	try:
		member = request.member
		if member:
			return MemberComlainRecord.objects.filter(
					member_id=member.id,
					created_at__year=low_date.year, 
					created_at__month=low_date.month, 
					created_at__day=low_date.day).count()
		else:
			watchdog_info(u"会员反馈api_view:is_complained 没有会员信息")	
			return False
	except:
		notify_msg = u"检查会员是否可以反馈信息api view：is_complained失败 cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		return False