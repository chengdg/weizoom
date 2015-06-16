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

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core import apiview_util
from utils.string_util import byte_to_hex
from models import *
from modules.member.models import *
from market_tools.prize.models import Prize


@login_required
def get_shakes(request):
	shakes = Shake.objects.filter(owner=request.user, is_deleted=False).order_by('-created_at')
	response = create_response(200)
	
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, shakes = paginator.paginate(shakes, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	
	response.data.items = []
	for shake_setting in shakes:
		shake = JsonResponse()
		shake.id = shake_setting.id
		shake.name = shake_setting.name
		response.data.items.append(shake)
		
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = '-created_at'
	
	return response.get_response()

########################################################################
# edit_red_envelope: 编辑/新建红包
########################################################################
@login_required
def edit_shake(request):
	id = int(request.POST.get('id', 0))
	name = request.POST.get('name', '').strip()
	detail = request.POST.get('detail', '').strip()
	wishing = request.POST.get('wishing', '').strip()
	remark = request.POST.get('remark', '').strip()
	not_winning_desc = request.POST.get('not_winning_desc', '').strip()
	
	level2info = {}
	
	for key in request.POST:
		if key.find('|') == -1:
			continue
		print key
		key_name, level = key.split('|')
		value = request.POST[key]
		
		if level in level2info:
			level2info[level][key_name] = value
		else:
			level2info[level] = {key_name: value}

	
	if id > 0:
		shakes = Shake.objects.filter(id=id)
		shakes.update(owner=request.user, name=name, detail=detail, not_winning_desc=not_winning_desc, wishing=wishing, remark=remark)
		if shakes.count() > 0:
			shake = shakes[0]
		else:
			response = create_response(500)
			response.data.msg=u"该摇一摇不存在"
			return response.get_response()
	else:
		shake = Shake.objects.create(owner=request.user, name=name, detail=detail, not_winning_desc=not_winning_desc, wishing=wishing, remark=remark)
	
	ShakeDetail.objects.filter(shake=shake).delete()
	for level in level2info:
		detail_info = level2info[level]
		ShakeDetail.objects.create(
			shake = shake,
			start_at = detail_info['start_at'],
			end_at = detail_info['end_at'],
			play_count = detail_info['play_count'],
			total_money = detail_info['total_money'],
			random_price_start = detail_info['random_price_start'],
			random_price_end = detail_info['random_price_end'],
			fixed_price = detail_info['fixed_price'],
			fixed_price_number = detail_info['fixed_price_number'],
			residue_price = detail_info['total_money'],
			fixed_price_residue_number = detail_info['fixed_price_number']
			)
	
	response = create_response(200)
	return response.get_response()


########################################################################
# get_records: 获取中奖记录
########################################################################
@login_required
def get_records(request):
	user = request.user.get_profile()
	records = ShakeRecord.objects.filter(owner=request.user).order_by('-created_at')
	
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
		
	response = create_response(200)
	
	response.data.items = []
	for record in records:
		member = record.member
		one_record = JsonResponse()
		if member:
			one_record.username = member.username_for_html
			one_record.user_id = member.id
		else:
			one_record.username = u'未知'
			one_record.user_id = 0

		one_record.money = str(record.money)
		one_record.name = record.shake_detail.shake.name
		one_record.is_sended = record.is_sended
		one_record.created_at = record.created_at.strftime('%Y-%m-%d')
		one_record.id = record.id
		response.data.items.append(one_record)
	
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	return response.get_response()


########################################################################
# get_red_envelopes: 获取红包列表
########################################################################
@login_required
def get_red_envelopes(request):
	red_envelopes = RedEnvelope.objects.filter(owner=request.user, is_deleted=False)
	response = create_response(200)
	
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, red_envelopes = paginator.paginate(red_envelopes, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	
	response.data.items = []
	for red_envelope in red_envelopes:
		cur_red_envelope = JsonResponse()
		cur_red_envelope.id = red_envelope.id
		cur_red_envelope.name = red_envelope.name
		response.data.items.append(cur_red_envelope)
		
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	
	return response.get_response()


########################################################################
# delete_red_envelope: 删除红包
########################################################################
@login_required
def delete_red_envelope(request):
	id = request.POST['id']
	RedEnvelope.objects.filter(id=id).update(is_deleted=True)
	
	response = create_response(200)
	return response.get_response()
		

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)

