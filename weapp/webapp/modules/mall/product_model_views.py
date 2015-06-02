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
from core import paginator
from core.dateutil import get_today

from excel_response import ExcelResponse

from account.models import *
from models import *
import signals
from modules.member.models import IntegralStrategySttings

import export


COUNT_PER_PAGE = 20

FIRST_NAV_NAME = 'webapp'
MALL_SETTINGS_NAV = 'mall-settings'


########################################################################
# __extract_property_value: 抽取product model property
########################################################################
def __extract_property_value(request):
	cid2value = {}
	for key, value in request.POST.items():
		if not key.startswith('value^'):
			continue
		_, name, cid = key.strip().split('^')
		cid = int(cid)
		if not cid in cid2value:
			cid2value[cid] = {'id': cid}
		cid2value[cid][name] = value

	cid_value_list = cid2value.items()
	cid_value_list.sort(lambda x,y:cmp(y[0], x[0]))
	return cid_value_list


########################################################################
# add_product_model_property: 添加商品规格
########################################################################
@login_required
def add_product_model_property(request):
	if request.POST:
		type = int(request.POST.get('type', PRODUCT_MODEL_PROPERTY_TYPE_TEXT))

		property = ProductModelProperty.objects.create(
			owner = request.user,
			type = type,
			name = request.POST.get('name', u'属性')
		)

		cid_value_list = __extract_property_value(request)
		for id, value in cid_value_list:
			ProductModelPropertyValue.objects.create(
				property = property,
				name = value['name'],
				pic_url = '' if type == PRODUCT_MODEL_PROPERTY_TYPE_TEXT else value['image']
			)

		return HttpResponseRedirect('/mall/editor/mall_settings/')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MALL_SETTINGS_NAV
		})
		return render_to_response('mall/editor/edit_product_model_property.html', c)


########################################################################
# update_product_model_property: 更新商品规格
########################################################################
@login_required
def update_product_model_property(request):
	#解决无效的请求
	if not request.GET.has_key('id'):
		response = create_response(500)
		return response.get_response()

	property_id = request.GET['id']
	if request.POST:
		type = int(request.POST.get('type', PRODUCT_MODEL_PROPERTY_TYPE_TEXT))

		ProductModelProperty.objects.filter(id=property_id).update(
			type = type,
			name = request.POST.get('name', u'属性')
		)

		existed_value_ids = set(ProductModelPropertyValue.objects.filter(property_id=property_id).values_list('id', flat=True))
		cid_value_list = __extract_property_value(request)
		#更新和添加
		for value_id, value in cid_value_list:
			if value_id > 0:
				ProductModelPropertyValue.objects.filter(id=value_id).update(
					name = value['name'],
					pic_url = '' if type == PRODUCT_MODEL_PROPERTY_TYPE_TEXT else value.get('image', '')
				)
			else:
				value = ProductModelPropertyValue.objects.create(
					property_id = property_id,
					name = value['name'],
					pic_url = '' if type == PRODUCT_MODEL_PROPERTY_TYPE_TEXT else value.get('image', '')
				)

		#删除
		ids = set([item[0] for item in cid_value_list])
		delete_ids = existed_value_ids - ids
		ProductModelPropertyValue.objects.filter(id__in=delete_ids).update(is_deleted=True)

		#发送post_update_product_model_property signal
		signals.post_update_product_model_property.send(sender=ProductModelProperty, model_property=ProductModelProperty.objects.get(id=property_id), request=request)

		return HttpResponseRedirect('/mall/editor/mall_settings/')
	else:
		property = ProductModelProperty.objects.get(id=property_id)

		values = []
		for value in ProductModelPropertyValue.objects.filter(property=property, is_deleted=False):
			values.append({
				"id": value.id,
				"name": value.name,
				"image": value.pic_url
			})
		property.values_json_str = json.dumps(values)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MALL_SETTINGS_NAV,
			'product_model_property': property
		})
		return render_to_response('mall/editor/edit_product_model_property.html', c)


########################################################################
# delete_product_model_property: 删除商品规格属性
########################################################################
@login_required
def delete_product_model_property(request, property_id):
	#发送pre_delete_product_model_property signal
	signals.pre_delete_product_model_property.send(sender=ProductModelProperty, model_property=ProductModelProperty.objects.get(id=property_id), request=request)

	ProductModelPropertyValue.objects.filter(property_id=property_id).update(is_deleted=True)
	ProductModelProperty.objects.filter(id=property_id).update(is_deleted=True)
	
	return HttpResponseRedirect('/mall/editor/mall_settings/')
