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

from core import paginator
import models as mall_models
from models import *
from core.restful_url_route import *
from core.jsonresponse import create_response


COUNT_PER_PAGE = 20


########################################################################
# create_integral_sale: 创建积分应用活动
########################################################################
@api(app='mall_promotion', resource='integral_sale', action='create')
@login_required
def create_integral_sale(request):
	# integral_sale_type = request.POST.get('type', 0)
	integral_sale_type = INTEGRAL_SALE_TYPE_PARTIAL #if integral_sale_type == 'partial' else INTEGRAL_SALE_TYPE_TOTAL
	if integral_sale_type == INTEGRAL_SALE_TYPE_PARTIAL:
		discount = request.POST.get('discount', 100)
		discount_money = request.POST.get('discount_money', 0.0)
		integral_price = 0.0
	else:
		discount = 100
		discount_money = 0.0
		integral_price = request.POST.get('integral_price', 0.0)

	integral_sale = IntegralSale.objects.create(
		owner = request.user,
		type = integral_sale_type,
		discount = 0,
		discount_money = 0.0,
		integral_price = 0,
		is_permanant_active = (request.POST.get('is_permanant_active', 'false') == 'true')
	)

	#创建integral rule
	rules = json.loads(request.POST.get('rules'))
	for rule in rules:
		IntegralSaleRule.objects.create(
			owner = request.user,
			integral_sale = integral_sale,
			member_grade_id = rule['member_grade_id'],
			discount = rule['discount'],
			discount_money = rule['discount_money']
		)

	#创建promotion
	now = datetime.today()
	start_date = datetime.strptime(request.POST.get('start_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
	end_date = datetime.strptime(request.POST.get('end_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
	# 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
	status = PROMOTION_STATUS_NOT_START
	promotion = Promotion.objects.create(
		owner = request.user,
		type = PROMOTION_TYPE_INTEGRAL_SALE,
		name = request.POST.get('name', ''),
		status = status,
		promotion_title = request.POST.get('promotion_title', ''),
		member_grade_id = 0,
		start_date = datetime.strptime('1900-01-01', '%Y-%m-%d') if integral_sale.is_permanant_active else start_date,
		end_date = datetime.strptime('2999-01-01', '%Y-%m-%d') if integral_sale.is_permanant_active else end_date,
		detail_id = integral_sale.id
	)

	products = json.loads(request.POST.get('products', '[]'))
	product_ids = set([product['id'] for product in products])
	for product_id in product_ids:
		ProductHasPromotion.objects.create(
			product_id = product_id,
			promotion = promotion
		)

	if start_date <= now:
		promotion.status = PROMOTION_STATUS_STARTED
		promotion.save()
	response = create_response(200)
	return response.get_response()
