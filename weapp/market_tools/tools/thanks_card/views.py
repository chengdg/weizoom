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

from account.models import *
from models import *
from webapp.modules.mall.models import *
from market_tools import export

COUNT_PER_PAGE = 20
MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'thanks_card'
########################################################################
# list_channel_qrcode_settings: 显示感恩贺卡列表页面
########################################################################
@login_required
def get_thanks_cards(request):
	webapp_id = request.user_profile.webapp_id
	has_order = (Order.objects.filter(webapp_id = webapp_id, type=THANKS_CARD_ORDER).count() > 0)
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		'has_order': has_order
	})
	return render_to_response('thanks_card/editor/thanks_card_orders.html', c)


########################################################################
# edit_thanks_card: 感恩贺卡设置
########################################################################
@login_required
def edit_thanks_card(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
	})
	return render_to_response('thanks_card/editor/edit_thanks_card.html', c)