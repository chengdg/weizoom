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
# create_premium_sale: 创建买赠活动
########################################################################
@api(app='mall_promotion', resource='premium_sale', action='create')
@login_required
def create_premium_sale(request):
	premium_sale = PremiumSale.objects.create(
		owner = request.user,
		count = request.POST.get('count', 1) or 1,
		is_enable_cycle_mode = (request.POST.get('is_enable_cycle_mode', 'false') == 'true')
	)

	now = datetime.today()
	start_date = datetime.strptime(request.POST.get('start_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
	# 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
	status = PROMOTION_STATUS_NOT_START
	promotion = Promotion.objects.create(
		owner = request.user,
		type = PROMOTION_TYPE_PREMIUM_SALE,
		name = request.POST.get('name', ''),
		status = status,
		promotion_title = request.POST.get('promotion_title', ''),
		member_grade_id = request.POST.get('member_grade', 0),
		start_date = start_date,
		end_date = request.POST.get('end_date', '2000-01-01 00:00:00'),
		detail_id = premium_sale.id
	)

	#处理主商品
	products = json.loads(request.POST.get('products', '[]'))
	product_ids = set([product['id'] for product in products])
	for product_id in product_ids:
		ProductHasPromotion.objects.create(
			product_id = product_id,
			promotion = promotion
		)

	#处理赠品
	premium_products = json.loads(request.POST.get('premium_products', '[]'))
	for product in premium_products:
		PremiumSaleProduct.objects.create(
			owner = request.user,
			premium_sale = premium_sale,
			product_id = product['id'],
			count = product['count'],
			unit = product['unit'],
		)

	if start_date <= now:
		promotion.status = PROMOTION_STATUS_STARTED
		promotion.save()
	response = create_response(200)
	return response.get_response()
