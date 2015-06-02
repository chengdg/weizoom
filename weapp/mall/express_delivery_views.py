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

import models as mall_models
from models import *
import export
from core.restful_url_route import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV


########################################################################
# get_express_delivery: 获得快递公司列表
########################################################################
@view(app='mall', resource='express_delivery', action='get')
@login_required
def get_express_delivery(request):
	has_express_delivery = (ExpressDelivery.objects.filter(owner_id=request.user.id).count() > 0)
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_config_second_navs(request),
		'second_nav_name': export.MALL_CONFIG_EXPRESS_COMOANY_NAV,
		'has_express_delivery': has_express_delivery
	})

	return render_to_response('mall/editor/express_deliverys.html', c)

