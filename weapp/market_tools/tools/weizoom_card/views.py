# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from watchdog.utils import watchdog_alert, watchdog_debug
from market_tools import export

from account.models import UserProfile

from models import *
from api_views import *
from module_api import *


MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'weizoom_card'

########################################################################
# list_weizoom_card: 显示微众钱包列表
########################################################################
@login_required
def list_weizoom_card(request):
	# c = RequestContext(request, {
	# 	'first_nav_name': MARKET_TOOLS_NAV,
	# 	'second_navs': export.get_second_navs(request),
	# 	'second_nav_name': SECOND_NAV_NAME,
	# })
	return HttpResponseRedirect('/apps/')


########################################################################
# create_weizoom_card_rule: 创建规则
########################################################################
@login_required
def create_weizoom_card_rule(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
	})
	return render_to_response('weizoom_card/editor/edit_weizoom_card_rule.html', c)


########################################################################
# weizoom_card_rule_detail: 显示核算详情
########################################################################
@login_required
def weizoom_card_rule_detail(request):
	id = request.GET['id']
	rule = WeizoomCardRule.objects.get(id=id)
	c = RequestContext(request, {
			'first_nav_name': MARKET_TOOLS_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'weizoom_card_rule': rule
		})
	return render_to_response('weizoom_card/editor/edit_weizoom_card_rule.html', c)


########################################################################
# list_adjust_accounts: 显示核算列表
########################################################################
@login_required
def list_adjust_accounts(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME
	})

	return render_to_response('weizoom_card/editor/list_adjust_accounts.html', c)

########################################################################
# detail_adjust_accounts: 显示核算明细列表
########################################################################
@login_required
def detail_adjust_accounts(request):
	args = {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'username': request.GET.get('username', None)
	}
	if args['username']:
		if 'start_date' in request.GET:
			args['start_date'] = request.GET.get('start_date', '2001-01-01')
		if 'end_date' in request.GET:
			args['end_date'] = request.GET.get('end_date', '2001-01-01')
		items = create_detail_adjust_accounts_infos(request)
		args['total'] = 0
		for item in items:
			args['total'] = args['total'] + float(item['money'])
		if args['total']:
			args['total'] = '%.2f' % args['total']
	c = RequestContext(request, args)
	return render_to_response('weizoom_card/editor/detail_adjust_accounts.html', c)


########################################################################
# weizoom_card_expense_record: 显示微众卡的消费记录
########################################################################
@login_required
def weizoom_card_expense_record(request, card_id):
	cards = WeizoomCard.objects.filter(id=card_id)
	if cards.count() == 0:
		watchdog_alert(u'微众卡的消费记录，不存在该微众卡号：{}'.format(card_num), user_id=request.user_profile.user_id)
		raise Http404(u"不存在该微众卡号")
	else:
		card = cards[0]
		expense_records = WeizoomCardHasOrder.objects.filter(card_id=card_id).order_by('created_at')
		for expense_record in expense_records:
			try:
				expense_record.true_order_id = get_order_id(expense_record.order_id)
			except:
				expense_record.true_order_id = None
				

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'card': card,
		'expense_records': expense_records
	})
	return render_to_response('weizoom_card/editor/weizoom_card_num_record.html', c)

########################################################################
# list_weizoom_card_accounts: 显示微众卡商户对应账号
########################################################################
@login_required
def list_weizoom_card_accounts(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
	})
	return render_to_response('weizoom_card/editor/list_weizoom_card_accounts.html', c) 
	
@login_required
def list_integral(request, user_id):
	user_profile = UserProfile.objects.get(user_id=user_id)

	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'user_profile':user_profile,
		'user_id':user_id
	})

	return render_to_response('weizoom_card/editor/adjust_accounts_integral.html', c) 
