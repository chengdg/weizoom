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
from modules.member.models import IntegralStrategySttings

import export
import module_api


COUNT_PER_PAGE = 20

FIRST_NAV_NAME = 'webapp'
MALL_SETTINGS_NAV = 'mall-settings'

########################################################################
# __extract_postage_config_special: 抽取商品规格
########################################################################
def __extract_postage_config_special(request):
	name2special = dict()
	special_configs = []
	for key, value in request.POST.items():
		if not key.startswith('special^'):
			continue

		_, special_id, special_field = key.split('^')

		if special_id in name2special:
			special_config = name2special[special_id]
		else:
			special_config = {"name": special_id}
			name2special[special_id] = special_config

		if value:
			special_config[special_field] = value
		else:
			special_config[special_field] = '0'

		special_configs = name2special.values()
		special_configs.sort(lambda x,y: cmp(x['name'], y['name']))

	return special_configs

def __create_config_special_and_special_has_province(user, config, special_configs):
	for special in special_configs:
		config_special = PostageConfigSpecial.objects.create(			
			owner = user,
			postage_config = config,
			first_weight_price = special['first_weight_price'],
			added_weight_price = special['added_weight_price']
		)

		for province_id in special['province'].split(','):
			PostageConfigSpecialHasProvince.objects.create(			
				owner = user,
				postage_config = config,
				postage_config_special = config_special,
				province_id = int(province_id)
			)

########################################################################
# add_postage_config: 添加运费配置
########################################################################
@login_required
def add_postage_config(request):
	if request.POST:		
		first_weight = request.POST.get('first_weight', '0.0').strip()
		added_weight = request.POST.get('added_weight', '0.0').strip()
		is_enable_added_weight = (request.POST.get('is_enable_added_weight', '0').strip() == '1')

		config = PostageConfig.objects.create(
			owner = request.user,
			name = request.POST.get('name', '').strip(),
			first_weight = first_weight,
			first_weight_price = request.POST.get('first_weight_price', '0.0').strip(),
			is_enable_added_weight = is_enable_added_weight,
			added_weight = added_weight,
			added_weight_price = request.POST.get('added_weight_price', '0.0').strip()
		)

		special_configs = __extract_postage_config_special(request)
		__create_config_special_and_special_has_province(request.user, config, special_configs)
		return HttpResponseRedirect('/mall/editor/mall_settings/')
	else:

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MALL_SETTINGS_NAV,
		})
		return render_to_response('mall/editor/edit_postage_config.html', c)


########################################################################
# update_postage_config: 更新运费配置
########################################################################
@login_required
def update_postage_config(request, postage_config_id):
	if request.POST:
		first_weight = request.POST.get('first_weight', '0.0').strip()
		added_weight = request.POST.get('added_weight', '0.0').strip()
		is_enable_added_weight = (request.POST.get('is_enable_added_weight', '0').strip() == '1')

		config = PostageConfig.objects.filter(owner=request.user, id=postage_config_id).update(
			name = request.POST.get('name', '').strip(),
			first_weight = first_weight,
			first_weight_price = request.POST.get('first_weight_price', '0').strip(),
			is_enable_added_weight = is_enable_added_weight,
			added_weight = added_weight,
			added_weight_price = request.POST.get('added_weight_price', '').strip()
		)
		config = PostageConfig.objects.get(id=postage_config_id)
		config.get_special_configs().delete()

		special_configs = __extract_postage_config_special(request)
		__create_config_special_and_special_has_province(request.user, config, special_configs)
		return HttpResponseRedirect('/mall/editor/mall_settings/')
	else:
		postage_config = PostageConfig.objects.get(owner=request.user, id=postage_config_id)
		
		values = []
		for value in PostageConfigSpecial.objects.filter(postage_config=postage_config):
			values.append({
				"id": value.id,
				"first_weight_price": value.first_weight_price,
				"added_weight_price": float(value.added_weight_price),
				"province": value.get_provinces_array()
			})
		postage_config.values_json_str = json.dumps(values)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MALL_SETTINGS_NAV,
			'postage_config': postage_config,
		})
		return render_to_response('mall/editor/edit_postage_config.html', c)

########################################################################
# delete_postage_config: 删除运费配置
########################################################################
@login_required
def delete_postage_config(request, postage_config_id):
	config = PostageConfig.objects.get(id = postage_config_id)
	if config.is_used:
		#将选用的运费改为“免运费”
		PostageConfig.objects.filter(owner=request.user, name=u'免运费').update(is_used=True)
		
	PostageConfig.objects.filter(id=postage_config_id).delete()

	# 修改商品的邮费
	module_api.update_products_postage(request.user.id, -1)

	return HttpResponseRedirect('/mall/editor/mall_settings/')
# MODULE END: postagesettings
# Termite GENERATED END: views