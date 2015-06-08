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
SECOND_NAV_NAME = 'shake'

########################################################################
# list_shake: 摇一摇列表
########################################################################
@login_required
def list_shake(request):
	user = request.user.get_profile()
	shakes = Shake.objects.filter(owner=request.user, is_deleted=False)
	#shake_ids = [l.id for l in shakes]
	#records = RedEnvelopeRecord.objects.filter(red_envelope_id__in=red_envelope_ids, prize_level__gt=0)

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'shakes': shakes
		#'records': records
	})
	return render_to_response('shake/editor/list_shake.html', c)


########################################################################
# edit_shake: 编辑摇一摇
########################################################################
@login_required
def edit_shake(request, id):
	if int(id) > 0:
		try:
			shake = Shake.objects.get(id=id)
		except:
			raise Http404('不存在该微信摇一摇')
		
		relations = ShakeDetail.objects.filter(shake=shake)
	else:
		relations = None
		shake = {'can_update': True}

	coupon_rules = get_coupon_rules(request.user)
	
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'shake': shake,
		'relations':relations,
		#'coupon_rules':coupon_rules
	})
	return render_to_response('shake/editor/edit_shake.html', c)

def delete_shake(request, id):
 	Shake.objects.filter(id=id).update(is_deleted=True)

 	return HttpResponseRedirect('/market_tools/shake/')

# ########################################################################
# # award_prize: 发奖
# ########################################################################
# @login_required
# def award_prize(request, id):
# 	RedEnvelopeRecord.objects.filter(id=id).update(is_awarded=True, awarded_at=datetime.today())
# 	try:
# 		return HttpResponseRedirect(request.META['HTTP_REFERER'])
# 	except:
# 		notify_msg = u"HTTP_REFERER cause:\n{}".format(unicode_full_stack())
# 		watchdog_error(notify_msg)
# 		return HttpResponseRedirect("/market_tools/red_envelope/")
	
