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
from models import *
from market_tools.prize.models import Prize
from market_tools.tools.coupon.util import get_coupon_rules
from market_tools import export


MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'lottery'


@login_required
def list_lottery(request):
	"""
	显示抽奖列表
	"""
	user = request.user.get_profile()
	lotteries = Lottery.objects.filter(owner=request.user, is_deleted=False)
	today = datetime.today()
	for lottery in lotteries:
		lottery.check_time()
		lottery.involved_count = LotteryRecord.objects.filter(lottery=lottery).values("id").count()
		start_at = lottery.start_at
	
		if today >= start_at:
			lottery.allowed_start = 1
		else:
			lottery.allowed_start = 0
	
		lottery.status_text = STATUS2TEXT[lottery.status]
		lottery.can_delete = False
		lottery.can_stop = False
		lottery.can_restart = False
		if lottery.status == LOTTERY_STATUS_NO_START:
			lottery.can_delete = True
		if lottery.status == LOTTERY_STATUS_RUNING:
			lottery.can_stop = True
		elif lottery.status == LOTTERY_STATUS_STOP:
			lottery.can_restart = True
		elif lottery.status == LOTTERY_STATUS_TIMEOUT:
			lottery.can_delete = True
	
	lottery_ids = [l.id for l in lotteries]
	records = LotteryRecord.objects.filter(lottery_id__in=lottery_ids, prize_level__gt=0)

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'lotteries': lotteries,
		'records': records
	})
	return render_to_response('lottery/editor/list_lottery.html', c)


########################################################################
# edit_lottery_view: 编辑抽奖
########################################################################
@login_required
def edit_lottery_view(request, id):
	id = int(id)
	if id:
		lottery = Lottery.objects.get(id=id)
		lottery.can_update = False
		if lottery.status == LOTTERY_STATUS_NO_START:
			lottery.can_update = True
		
		relations = LotteryHasPrize.objects.filter(lottery=lottery)
		prize_ids = [r.prize_id for r in relations]
		prizes = Prize.objects.filter(id__in=prize_ids)
		id2prize = dict([(p.id, p) for p in prizes])
		lottery.prizes = []
		for r in relations:
			prize = id2prize[r.prize_id]
			prize.prize_source = r.prize_source
			prize.prize_type = r.prize_type
			lottery.prizes.append(prize)
		
		lottery.prizes.sort(lambda x,y: cmp(x.level, y.level))
		
		#转换为json
		response = JsonResponse()
		response.id = lottery.id
		response.name = lottery.name
		response.detail = lottery.detail
		response.expend_integral = lottery.expend_integral
		response.can_repeat = lottery.can_repeat
		response.daily_play_count = lottery.daily_play_count
		response.type = lottery.type
		response.award_hour = lottery.award_hour
		response.not_win_desc = lottery.not_win_desc
		if lottery.award_type:
			response.award_type = lottery.award_type
		else:
			response.award_type = ''
		response.start_at = lottery.start_at.strftime("%Y-%m-%d")
		response.end_at = lottery.end_at.strftime("%Y-%m-%d")
		response.prizes = {}
		for prize in lottery.prizes:
			prize_json = {}
			prize_json['prize_source'] = prize.prize_source
			prize_json['prize_type'] = prize.prize_type
			prize_json['prize_name'] = prize.name
			prize_json['prize_level'] = prize.level
			prize_json['prize_odds'] = prize.odds
			prize_json['prize_count'] = prize.count
			response.prizes[prize.id] = prize_json
			
		lottery_json = response.get_json()
	else:
		lottery = {'can_update': True}
		lottery_json = ''

	coupon_rules = get_coupon_rules(request.user)
	
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'lottery': lottery,
		'lottery_json':lottery_json,
		'coupon_rules':coupon_rules
	})
	return render_to_response('lottery/editor/edit_lottery.html', c)


########################################################################
# stop_lottery: 停止活动
########################################################################
@login_required
def stop_lottery(request, id):
	Lottery.objects.filter(id=id).update(status=LOTTERY_STATUS_STOP)
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	

########################################################################
# start_lottery: 开启活动
########################################################################
@login_required
def start_lottery(request, id):
	Lottery.objects.filter(id=id).update(status=LOTTERY_STATUS_RUNING)
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# delete_lottery: 删除活动
########################################################################
@login_required
def delete_lottery(request, id):
	Lottery.objects.filter(id=id).delete()
	
	return HttpResponseRedirect('/market_tools/lottery/list/')


########################################################################
# award_prize: 发奖
########################################################################
@login_required
def award_prize(request, id):
	LotteryRecord.objects.filter(id=id).update(is_awarded=True, awarded_at=datetime.today())
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])