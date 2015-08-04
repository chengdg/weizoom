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
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error

MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'red_envelope'

########################################################################
# list_red_envelope: 显示红包列表
########################################################################
@login_required
def list_red_envelope(request):
	user = request.user.get_profile()
	red_envelopes = RedEnvelope.objects.filter(owner=request.user, is_deleted=False)
	red_envelope_ids = [l.id for l in red_envelopes]
	records = RedEnvelopeRecord.objects.filter(red_envelope_id__in=red_envelope_ids, prize_level__gt=0)

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'red_envelopes': red_envelopes,
		'records': records
	})
	return render_to_response('red_envelope/editor/list_red_envelope.html', c)


########################################################################
# edit_red_envelope_view: 编辑红包
########################################################################
@login_required
def edit_red_envelope_view(request, id):
	if int(id) > 0:
		try:
			red_envelope = RedEnvelope.objects.get(id=id)
		except:
			raise Http404('不存在该微信红包')
		
		relations = RedEnvelopeHasPrize.objects.filter(red_envelope=red_envelope)
		prize_ids = [r.prize_id for r in relations]
		prizes = Prize.objects.filter(id__in=prize_ids)
		id2prize = dict([(p.id, p) for p in prizes])
		red_envelope.prizes = []
		for r in relations:
			prize = id2prize[r.prize_id]
			prize.prize_source = r.prize_source
			prize.prize_type = r.prize_type
			red_envelope.prizes.append(prize)

		red_envelope.prizes.sort(lambda x,y: cmp(x.level, y.level))
		
		#转换为json
		response = JsonResponse()
		response.id = red_envelope.id
		response.name = red_envelope.name
		response.total_award_value = red_envelope.total_award_value
		response.desc = red_envelope.desc
		response.can_repeat = red_envelope.can_repeat
		response.daily_play_count = red_envelope.daily_play_count
		response.prizes = {}
		for prize in red_envelope.prizes:
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
		red_envelope = {'can_update': True}
		lottery_json = ''

	coupon_rules = get_coupon_rules(request.user)
	
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'red_envelope': red_envelope,
		'lottery_json':lottery_json,
		'coupon_rules':coupon_rules
	})
	return render_to_response('red_envelope/editor/edit_red_envelope.html', c)


########################################################################
# award_prize: 发奖
########################################################################
@login_required
def award_prize(request, id):
	RedEnvelopeRecord.objects.filter(id=id).update(is_awarded=True, awarded_at=datetime.today())
	try:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	except:
		notify_msg = u"HTTP_REFERER cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		return HttpResponseRedirect("/market_tools/red_envelope/")
	
