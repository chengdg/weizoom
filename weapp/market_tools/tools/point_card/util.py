# -*- coding: utf-8 -*-

# import time
# from datetime import timedelta, datetime, date
# import urllib, urllib2
# import os
# import json

# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required, permission_required
# from django.conf import settings
# from django.shortcuts import render_to_response
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib import auth
# from django.db.models import Q

# from core.jsonresponse import JsonResponse, create_response
# from core.dateutil import get_today
# from core.exceptionutil import full_stack, unicode_full_stack

# from models import *
# from product import module_api as weapp_product_api

# template_path_items = os.path.dirname(__file__).split(os.sep)
# TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

# page_title = u'充值'


########################################################################
# get_coupon_rules: 获取充值卡列表
########################################################################
# def get_coupon_rules(owner):
	#profile = request.user_profile
	
	# if weapp_product_api.has_permission_to_access(owner, '/market_tools/point_card/'):
#		rules = list(CouponRule.objects.filter(owner=owner, is_active=True))
#	else:
	# 	rules = []

	# return rules


