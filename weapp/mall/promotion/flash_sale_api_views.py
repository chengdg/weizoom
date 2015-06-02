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


default_date = datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


########################################################################
# create_flash_sale: 创建限时抢购
########################################################################
@api(app='mall_promotion', resource='flash_sale', action='create')
@login_required
def create_flash_sale(request):
	count_per_purchase = request.POST.get('count_per_purchase', 9999999)
	if not count_per_purchase:
		count_per_purchase = 9999999
	limit_period = request.POST.get('limit_period', 0)
	if not limit_period:
		limit_period = 0
	flash_sale = FlashSale.objects.create(
		owner = request.user,
		limit_period = limit_period,
		promotion_price = request.POST.get('promotion_price', 0.0),
		count_per_purchase = count_per_purchase
	)
	now = datetime.today()
	start_date = datetime.strptime(request.POST.get('start_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
	# 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
	status = PROMOTION_STATUS_NOT_START
	promotion = Promotion.objects.create(
		owner = request.user,
		type = PROMOTION_TYPE_FLASH_SALE,
		name = request.POST.get('name', ''),
		promotion_title = request.POST.get('promotion_title', ''),
		status = status,
		member_grade_id = request.POST.get('member_grade', 0),
		start_date = start_date,
		end_date = request.POST.get('end_date', '2000-01-01 00:00:00'),
		detail_id = flash_sale.id
	)

	products = json.loads(request.POST['products'])
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

