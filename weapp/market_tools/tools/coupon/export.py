# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from webapp import views as webapp_views

from models import *
import util as coupon_util 
from settings import TOOL_NAME

def get_link_targets(request):
	response = create_response(200)
	pages = []
	for coupon_rule in coupon_util.get_coupon_rules(request.user):
		pages.append({'text': coupon_rule.name, 'value': './?module=market_tool:coupon&model=coupon&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%s&project_id=0&rule_id=%s'
			% (request.webapp_owner_id ,coupon_rule.id)})

	response.data = [
		{
			'name': u'优惠券规则',
			'data': pages
		}
	]
	return response.get_response()

########################################################################
# get_webapp_usage_link: 获得webapp使用情况的链接
########################################################################
def get_webapp_usage_link(webapp_owner_id, member):
	workspace_template_info = 'workspace_id=market_tool:coupon&webapp_owner_id=%d&project_id=0' % webapp_owner_id

	info = '%d' % coupon_util.get_can_use_coupon_count(member.id)
	return {
		'name': u'我的优惠券',
		'link': './?module=market_tool:coupon&model=usage&action=get&%s' % workspace_template_info,
		'info': info
	}