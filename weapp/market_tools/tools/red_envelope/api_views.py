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


########################################################################
# edit_red_envelope: 编辑/新建红包
########################################################################
@login_required
def edit_red_envelope(request):
	id = int(request.POST.get('id', 0))
	name = request.POST.get('name', '').strip()
	total_award_value = request.POST.get('total_award_value', '').strip()
	desc = request.POST.get('desc', '').strip()
	is_non_member = request.POST.get('is_non_member', 0)
	logo_url = request.POST.get('logo_url', '').strip()
	expected_participation_count = request.POST.get('expected_participation_count', 1000)
	
	level2info = {}
	
	for key in request.POST:
		if not key.startswith('prize_'):
			continue

		key_name, level = key.split('|')
		value = request.POST[key]
		
		if level in level2info:
			level2info[level][key_name] = value
		else:
			level2info[level] = {key_name: value}

	
	if id > 0:
		red_envelopes = RedEnvelope.objects.filter(id=id)
		red_envelopes.update(owner=request.user, name=name, logo_url=logo_url,
					is_non_member=is_non_member,
					total_award_value=total_award_value, desc=desc,
					expected_participation_count=expected_participation_count)

		if red_envelopes.count() > 0:
			red_envelope = red_envelopes[0]
		else:
			response = create_response(500)
			response.data.msg=u"该红包不存在"
			return response.get_response()

		relations = RedEnvelopeHasPrize.objects.filter(red_envelope=red_envelope)
		prize_ids = [r.prize_id for r in relations]
		Prize.objects.filter(id__in=prize_ids).delete()
		relations.delete()
	else:
		red_envelope = RedEnvelope.objects.create(owner=request.user, name=name, logo_url=logo_url,
				is_non_member=is_non_member,
				total_award_value=total_award_value, desc=desc,
				expected_participation_count=expected_participation_count)
		
	for level in level2info:
		prize_info = level2info[level]
		prize = Prize.objects.create(name=prize_info['prize_name'], level=level, odds=prize_info['prize_odds'], 
					detail=prize_info['prize_name'], count=prize_info['prize_count'])
		RedEnvelopeHasPrize.objects.create(red_envelope=red_envelope, prize=prize, prize_type=prize_info['prize_type'],
					prize_source=prize_info['prize_source'])
	
	response = create_response(200)
	return response.get_response()


########################################################################
# get_records: 获取中奖记录
########################################################################
@login_required
def get_records(request):
	user = request.user.get_profile()
	red_envelopes = RedEnvelope.objects.filter(owner=request.user, is_deleted=False)
	red_envelope_ids = [r.id for r in red_envelopes]
	
	#处理搜索
	query = request.GET.get('query', None)
	if query:
		query_hex = byte_to_hex(query)
		records = RedEnvelopeRecord.objects.filter(red_envelope_id__in=red_envelope_ids, prize_level__gt=0, prize_number=query_hex)
	else:
		records = RedEnvelopeRecord.objects.filter(red_envelope_id__in=red_envelope_ids, prize_level__gt=0)
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
		
	response = create_response(200)
	
	response.data.items = []
	for record in records:
		member = WebAppUser.get_member_by_webapp_user_id(record.webapp_user_id)
		one_record = JsonResponse()
		if member:
			one_record.username = member.username_for_html
			one_record.user_id = member.id
		else:
			one_record.username = u'未知'
			one_record.user_id = 0
		one_record.prize_number = record.prize_number
		one_record.red_envelope_name = record.red_envelope_name
		one_record.prize_money = str(record.prize_money)
		one_record.prize_name = record.prize_name
		one_record.prize_type = record.prize_type
		one_record.prize_detail = record.prize_detail
		one_record.created_at = record.created_at.strftime('%Y-%m-%d')
		one_record.awarded_at = record.awarded_at.strftime('%Y-%m-%d')
		one_record.is_awarded = record.is_awarded
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

