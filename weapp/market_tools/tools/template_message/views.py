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
SECOND_NAV_NAME = 'template_message'

########################################################################
# list_template_message: 显示模板消息列表
########################################################################
@login_required
def list_template_message(request):
    industries = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user).values('industry', 'type').distinct()
    industry = {}
    for indus in industries:
        industry_name = TYPE2INDUSTRY.get(indus['industry'], '')
        if indus['type'] == MAJOR_INDUSTRY_TYPE:
            industry['major'] = industry_name
        elif indus['type'] == DEPUTY_INDUSTRY_TYPE:
            industry['deputy'] = industry_name
    c = RequestContext(request, {
        'first_nav_name': MARKET_TOOLS_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': SECOND_NAV_NAME,
        'industry': industry
    })
    return render_to_response('template_message/editor/list_template_message.html', c)


########################################################################
# edit_template_message_detail: 编辑模板消息详细信息
########################################################################
@login_required
def edit_template_message_detail(request):
    template_detail_id = int(request.GET.get('template_detail_id'))
    message_detail = MarketToolsTemplateMessageDetail.objects.get(id=template_detail_id)
    c = RequestContext(request, {
        'first_nav_name': MARKET_TOOLS_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': SECOND_NAV_NAME,
        'message_detail': message_detail
    })
    return render_to_response('template_message/editor/edit_template_message_detail.html', c)