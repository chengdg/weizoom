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
import util as point_card_util 
from settings import TOOL_NAME


########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=market_tool:point_card&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id

	#获得页面
	pages = []
	pages.append({'text': u'积分充值', 'value': './?module=market_tool:point_card&model=usage&action=get&%s' % workspace_template_info})

	response.data = [
		{
			'name': u'积分充值',
			'data': pages
		}
	]
	return response.get_response()


########################################################################
# get_webapp_usage_link: 获得webapp使用情况的链接
########################################################################
def get_webapp_usage_link(webapp_owner_id, member):
	workspace_template_info = 'workspace_id=market_tool:point_card&webapp_owner_id=%d&project_id=0' % webapp_owner_id

	return {
		'name': u'积分充值',
		'link': './?module=market_tool:point_card&model=usage&action=get&%s' % workspace_template_info,
		'info': ''
	}