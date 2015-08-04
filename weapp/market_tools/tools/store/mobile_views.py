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
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack
from core import paginator

from models import *

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]


########################################################################
# get_store_citys: 显示"选择门店城市"页面
########################################################################
def get_store_citys(request):
	citys = Store.objects.filter(owner_id=request.webapp_owner_id).values("city").distinct()

	c = RequestContext(request, {
		'page_title':u'选择所在区域',
		'citys':citys,
		'hide_non_member_cover': True,
	})
	return render_to_response('store/webapp/get_store_citys.html', c)

########################################################################
# get_store_list: 显示“该城市所有门店列表”页面
########################################################################
def get_store_list(request):
	city = request.GET.get('city')

	stores = Store.objects.filter(city=city)
	c = RequestContext(request, {
		'page_title':u'门店列表-%s' % city,
		'stores':stores,
		'hide_non_member_cover': True,
		'city':city
	})
	return render_to_response('store/webapp/get_store_list.html', c)

########################################################################
# get_store_detail: 显示“门店详细信息”页面
########################################################################
def get_store_detail(request):
	store_id = request.GET.get('id')
	store = Store.objects.get(id=store_id)

	#获取轮播图
	store.swipe_images = []
	swipe_images = StoreSwipeImage.objects.filter(store_id=store_id)
	if not swipe_images:
		swipe_images = StoreSwipeImage.objects.filter(store_id=store_id)
	for swipe_image in swipe_images:
		store.swipe_images.append({
			'url': swipe_image.url
		})
	store.swipe_images_json = json.dumps(store.swipe_images)
	location = store.location
	lng,lat = location.split(",")
	
	c = RequestContext(request, {
		'page_title':u'门店详情-%s' % store.name,
		'store':store,
		'hide_non_member_cover': True,
		'lat': lat,
		'lng': lng
	})
	return render_to_response('store/webapp/get_store_detail.html', c)


########################################################################
# get_map: 显示“门店地图信息”页面
########################################################################
def get_map(request):
	store_id = request.GET.get('store_id')
	store = Store.objects.get(id=store_id)
	 
	c = RequestContext(request, {
		'page_title':u'门店地图-%s' % store.name,
		'store':store,
		'hide_non_member_cover': True,
	})
	return render_to_response('store/webapp/map.html', c)