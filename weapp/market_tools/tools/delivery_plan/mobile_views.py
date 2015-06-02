# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import time
import json
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack

from market_tools.prize.models import *
from webapp.modules.mall.models import *
from modules.member.util import get_member
from models import *

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_delivery_plan(request):
	delivery_plan_id = int(request.GET['delivery_plan_id'])
	
	try:
		member = request.member
	except:
		member = None
		
	try:
		delivery_plan = DeliveryPlan.objects.get(id=delivery_plan_id, is_deleted=False)
		product = Product.objects.get(id=delivery_plan.product_id)
	except:
		c = RequestContext(request, {
			'is_deleted_data': True,
			'is_hide_weixin_option_menu':False,
		})
		return render_to_response('%s/delivery_plan/webapp/detail_delivery_plan.html' % TEMPLATE_DIR, c)
	
	delivery_plan.discount = delivery_plan.original_price - delivery_plan.price
	#获取轮播图
	product.swipe_images = []
	swipe_images = ProductSwipeImage.objects.filter(product_id=delivery_plan.original_product_id)
	if not swipe_images:
		swipe_images = ProductSwipeImage.objects.filter(product_id=product.id)
	for swipe_image in swipe_images:
		product.swipe_images.append({
			'url': swipe_image.url
		})
	product.swipe_images_json = json.dumps(product.swipe_images)
	
	#获取计算日期的信息
	today = datetime.today()
	start_date = today + timedelta(days=1)
	end_date = today + timedelta(days=30)
	today = today.strftime('%Y-%m-%d')
	start_date = start_date.strftime('%Y-%m-%d')
	end_date = end_date.strftime('%Y-%m-%d')
	
	if delivery_plan.type == MONTHLY:
		delivery_plan.days = 30
	elif delivery_plan.type == DAILY:
		delivery_plan.days = 1
	else:
		delivery_plan.days = 7
	
	c = RequestContext(request, {
		'page_title': delivery_plan.name,
		'delivery_plan': delivery_plan,
		'product': product,
		'member': member,
		'today': today,
		'start_date': start_date,
		'end_date': end_date,
	})

	return render_to_response('%s/delivery_plan/webapp/detail_delivery_plan.html' % TEMPLATE_DIR, c)
