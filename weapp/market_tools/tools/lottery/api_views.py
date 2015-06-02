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
from market_tools.prize.models import Prize


########################################################################
# edit_lottery: 编辑/新建抽奖
########################################################################
@login_required
def edit_lottery(request):
	id = int(request.POST.get('id', 0))
	name = request.POST.get('name', '').strip()
	detail = request.POST.get('detail', '').strip()
	expend_integral = int(request.POST.get('expend_integral', 0))
	daily_play_count = request.POST.get('daily_play_count', 0)
	type = int(request.POST.get('type', 0))
	start_at = request.POST.get('start_at', '').strip()
	end_at = request.POST.get('end_at', '').strip()
	expected_participation_count = request.POST.get('expected_participation_count', 1000)
	not_win_desc = request.POST.get('not_win_desc', '').strip()

	level2info = {}

	for key in request.POST:#处理奖项和中奖率的问题
		if not key.startswith('prize_'):
			continue

		key_name, level = key.split('|')
		value = request.POST[key]

		if level in level2info:
			level2info[level][key_name] = value
		else:
			level2info[level] = {key_name: value}


	if id:
		lottery = Lottery.objects.filter(id=id)
		lottery.update(owner=request.user, name=name, detail=detail, type=type,daily_play_count=daily_play_count, expend_integral=expend_integral,
					start_at=start_at, end_at=end_at, expected_participation_count=expected_participation_count)
		lottery = lottery[0]
		relations = LotteryHasPrize.objects.filter(lottery=lottery)
		prize_ids = [r.prize_id for r in relations]
		Prize.objects.filter(id__in=prize_ids).delete()
		relations.delete()
	else:
		current_time = datetime.today()
		start_at = datetime.strptime(start_at, '%Y-%m-%d')

		status = LOTTERY_STATUS_NO_START
		if start_at <= current_time:
			status = LOTTERY_STATUS_RUNING

		lottery = Lottery.objects.create(owner=request.user, name=name, detail=detail, type=type,daily_play_count=daily_play_count, expend_integral=expend_integral,
					start_at=start_at, end_at=end_at, status=status, expected_participation_count=expected_participation_count,not_win_desc=not_win_desc)

	for level in level2info:
		prize_info = level2info[level]
		prize = Prize.objects.create(name=prize_info['prize_name'], level=level,odds=prize_info['prize_odds'], 
					detail=prize_info['prize_name'], count=prize_info['prize_count'])
		LotteryHasPrize.objects.create(lottery=lottery, prize=prize, prize_type=prize_info['prize_type'],
					prize_source=prize_info['prize_source'])

	response = create_response(200)
	return response.get_response()


########################################################################
# get_records: 获取中奖记录
########################################################################
@login_required
def get_records(request):
	user = request.user.get_profile()
	lotteries = Lottery.objects.filter(owner=request.user, is_deleted=False)
	lottery_ids = [l.id for l in lotteries]

	#处理搜索
	query = request.GET.get('query', None)
	if query:
		query_hex = byte_to_hex(query)
		records = LotteryRecord.objects.filter(lottery_id__in=lottery_ids, prize_level__gt=0, prize_number=query_hex)
	else:
		records = LotteryRecord.objects.filter(lottery_id__in=lottery_ids, prize_level__gt=0)

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	response = create_response(200)

	response.data.items = []
	for record in records:
		one_record = JsonResponse()
		one_record.username = record.member.username_for_html
		one_record.user_id = record.member.id
		one_record.prize_number = record.prize_number
		one_record.prize_money = str(record.prize_money)
		one_record.lottery_name = record.lottery_name
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


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)
