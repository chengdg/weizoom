
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

from excel_response import ExcelResponse

from account.models import *
from models import *
from util import  get_coupon_rules

from modules.member.models import Member, WebAppUser

COUNT_PER_PAGE = 20

FIRST_NAV_NAME = 'market_tools'
SECOND_NAV_NAME = 'complain'

########################################################################
# get_complain: 反馈列表
########################################################################
@login_required
def get_complain(request):
	complains = MemberComplainRecord.objects.filter(complain_settings__owner=request.user).order_by('-created_at')
	cur_page = int(request.GET.get('page', '1'))
	
	for complain in complains:
		if complain.webapp_user_id != -1:
			try:
				member = WebAppUser.get_member_by_webapp_user_id(complain.webapp_user_id)
				if member and member.is_for_test == False:
					complain.member_username = member.username_for_html
					complain.member_id = member.id
				else:
					complain.member_username = u'非会员'
			except:
				complain.member_username = u'非会员'
		else:
			complain.member_username = u'非会员'

	pageinfo, complains = paginator.paginate(complains, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
	
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'complains': complains,
		'pageinfo': json.dumps(paginator.to_dict(pageinfo)),
	})
	return render_to_response('complain/editor/member_complain_list.html', c)

########################################################################
# member_complain_settings: 显示
########################################################################
@login_required
def member_complain_settings(request):

	coupon_rules = get_coupon_rules(request.user)
	if request.method == 'GET':
		member_complain_settings = MemberComplainSettings.objects.filter(owner=request.user)
		member_complain_setting = member_complain_settings[0] if member_complain_settings.count() > 0 else None
	else:
		
		prize_source = request.POST.get('prize_source|0', '').strip()
		prize_type = request.POST.get('prize_type|0', '').strip()

		if MemberComplainSettings.objects.filter(owner=request.user).count() == 0:
			MemberComplainSettings.objects.create(
				detail=request.POST.get('detail', '').strip(), 
				name = request.POST.get('name', '').strip(),
				# prize_content = request.POST.get('prize_source|0', '').strip(),
				prize_type = 0,
				owner = request.user,
				is_non_member = request.POST.get('is_non_member', False),
				is_allowed_image = request.POST.get('is_allowed_image', False)
				)
		else:
			MemberComplainSettings.objects.filter(owner=request.user).update(
				detail=request.POST.get('detail', '').strip(), 
				name = request.POST.get('name', '').strip(),
				# prize_content = request.POST.get('prize_source|0', '').strip(),
				prize_type = 0,
				is_non_member = request.POST.get('is_non_member', False),
				is_allowed_image = request.POST.get('is_allowed_image', False)
				)
		return HttpResponseRedirect('/market_tools/complain/')
		#member_complain_setting = MemberComplainSettings.objects.filter(owner=request.user)[0]

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'member_complain_setting': member_complain_setting,
		'coupon_rules': coupon_rules,
	})
	return render_to_response('complain/editor/member_complain_settings.html', c)

# def get_feedback(request):
# 	complains = MemberFeedbackRecord.objects.filter(feedback_settings__owner=request.user)

# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV_NAME,
# 		'second_navs': export.get_second_navs(request),
# 		'second_nav_name': SECOND_NAV_NAME,
# 		'complains': complains
# 	})
# 	return render_to_response('complain/editor/member_feedback_list.html', c)

# def  member_feedback_settings(request):
# 	coupon_rules = get_coupon_rules(request.user)
# 	if request.method == 'GET':
# 		member_complain_settings = MemberFeedbackSettings.objects.filter(owner=request.user)
# 		member_complain_setting = member_complain_settings[0] if member_complain_settings.count() > 0 else None
# 	else:
		
# 		prize_source = request.POST.get('prize_source|0', '').strip()
# 		prize_type = request.POST.get('prize_type|0', '').strip()

# 		if MemberFeedbackSettings.objects.filter(owner=request.user).count() == 0:
# 			MemberFeedbackSettings.objects.create(
# 				detail=request.POST.get('detail', '').strip(), 
# 				name = request.POST.get('name', '').strip(),
# 				prize_content = request.POST.get('prize_source|0', '').strip(),
# 				prize_type = request.POST.get('prize_type|0', '').strip(),
# 				owner = request.user,
# 				is_allowed_image = request.POST.get('is_allowed_image', False)
# 				)
# 		else:
# 			MemberFeedbackSettings.objects.filter(owner=request.user).update(
# 				detail=request.POST.get('detail', '').strip(), 
# 				name = request.POST.get('name', '').strip(),
# 				prize_content = request.POST.get('prize_source|0', '').strip(),
# 				prize_type = request.POST.get('prize_type|0', '').strip(),
# 				is_allowed_image = request.POST.get('is_allowed_image', False)
# 				)
# 		member_complain_setting = MemberFeedbackSettings.objects.filter(owner=request.user)[0]

# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV_NAME,
# 		'second_navs': export.get_second_navs(request),
# 		'second_nav_name': SECOND_NAV_NAME,
# 		'member_complain_setting': member_complain_setting,
# 		'coupon_rules': coupon_rules,
# 	})
# 	return render_to_response('complain/editor/member_feedback_settings.html', c)