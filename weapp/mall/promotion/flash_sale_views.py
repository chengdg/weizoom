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

import models as mall_models
from models import *
from mall import export
from core.restful_url_route import *
from modules.member.models import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_PROMOTION_FIRST_NAV


########################################################################
# get_flash_sales: 获得限时抢购列表
########################################################################
@view(app='mall_promotion', resource='flash_sales', action='get')
@login_required
def get_flash_sales(request):

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV
	})

	return render_to_response('mall/editor/promotion/flash_sales.html', c)


########################################################################
# create_flash_sale: 添加限时抢购
########################################################################
@view(app='mall_promotion', resource='flash_sale', action='create')
@login_required
def create_flash_sale(request):
	member_grades = MemberGrade.get_all_grades_list(request.user_profile.webapp_id)

	c = RequestContext(request, {
		'member_grades': member_grades,
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV
	})

	return render_to_response('mall/editor/promotion/create_flash_sale.html', c)


########################################################################
# copy_flash_sale: 拷贝限时抢购
########################################################################
@view(app='mall_promotion', resource='flash_sale', action='copy')
@login_required
def copy_flash_sale(request):
	promotion_id = request.GET['id']
	promotion = Promotion.objects.get(id=promotion_id)
	Promotion.fill_details(request.user, [promotion], {
		'with_concrete_promotion': True
	})

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV,
		'promotion': promotion
	})

	return render_to_response('mall/editor/promotion/create_flash_sale.html', c)


########################################################################
# get_flash_sale_detail: 浏览限时抢购详情
########################################################################
@view(app='mall_promotion', resource='flash_sale_detail', action='get')
@login_required
def get_flash_sale_detail(request):
	promotion_id = request.GET['id']
	promotion = Promotion.objects.get(owner=request.user, type=PROMOTION_TYPE_FLASH_SALE, id=promotion_id)
	Promotion.fill_details(request.user, [promotion], {
		'with_product': True,
		'with_concrete_promotion': True
	})

	for product in promotion.products:
		product.models = product.models[1:]

	if promotion.member_grade_id:
		try:
			promotion.member_grade_name = MemberGrade.objects.get(id=promotion.member_grade_id).name
		except:
			promotion.member_grade_name = MemberGrade.get_default_grade(request.user_profile.webapp_id).name

	jsons = [{
		"name": "product_models",
		"content": promotion.products[0].models
	}]

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV,
		'promotion': promotion,
		'jsons': jsons
	})

	return render_to_response('mall/editor/promotion/flash_sale_detail.html', c)
