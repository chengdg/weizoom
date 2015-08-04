# # -*- coding: utf-8 -*-

# import time
# from datetime import timedelta, datetime, date
# import urllib, urllib2
# import os
# import json
# import MySQLdb
# import random
# import string

# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.shortcuts import render_to_response
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib import auth
# from django.db.models import Q, F
# from django.db.models.aggregates import Sum, Count

# import models as mall_models
# from models import *
# from mall import export
# from core.restful_url_route import *


# COUNT_PER_PAGE = 20
# FIRST_NAV = export.MALL_PROMOTION_FIRST_NAV


# ########################################################################
# # get_promotions: 获得在售商品列表
# ########################################################################
# @view(app='mall_promotion', resource='promotion_list', action='get')
# @login_required
# def get_promotion_list(request):

# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV,
# 		'second_navs': export.get_promotion_second_navs(request),
# 		'second_nav_name': export.MALL_PROMOTION_PROMOTIONS_NAV
# 	})

# 	return render_to_response('mall/editor/promotion/promotions.html', c)
