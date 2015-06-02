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
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from core.jsonresponse import JsonResponse, create_response
from core import paginator, dateutil

from market_tools import export
from weixin.user.models import get_system_user_binded_mpuser, is_subscribed

from excel_response import ExcelResponse

from account.models import *
from models import *
from util import  get_coupon_rules, get_all_grades_list

COUNT_PER_PAGE = 20

FIRST_NAV_NAME = 'market_tools'
SECOND_NAV_NAME = 'member_qrcode'


########################################################################
# list_member_qrcode_settings: 显示
########################################################################
@login_required
def member_qrcode_settings(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
		should_show_authorize_cover = True
	else:
		should_show_authorize_cover = False
	
	coupon_rules = get_coupon_rules(request.user)
	member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner=request.user)
	member_qrcode_setting = member_qrcode_settings[0] if member_qrcode_settings.count() > 0 else None
	if member_qrcode_setting:
		award_contents = MemberQrcodeAwardContent.objects.filter(member_qrcode_settings=member_qrcode_setting)
		if award_contents.count() > 0:
			award_content = award_contents[0] if member_qrcode_setting.award_member_type == 1 else None
		else:
			award_content = None
	else:
		award_contents = None
		award_content = None
	member_grades = get_all_grades_list(request)

	if member_grades and award_contents:
	
		for member_grade in member_grades:
			content = award_contents.filter(member_level=member_grade.id)[0] if award_contents.filter(member_level=member_grade.id).count() > 0 else None
			if content:
				member_grade.award_type = content.award_type
				member_grade.award_content = content.award_content

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'member_qrcode_settings': member_qrcode_setting,
		'coupon_rules': coupon_rules,
		'award_content': award_content,
		'member_grades': member_grades,
		'should_show_authorize_cover': should_show_authorize_cover,
		'is_hide_weixin_option_menu': True
	})
	return render_to_response('member_qrcode/editor/member_qrcode_settings.html', c)

