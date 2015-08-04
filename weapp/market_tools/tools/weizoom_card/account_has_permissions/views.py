# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required

from market_tools import export


MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'weizoom_card'

########################################################################
# edit_weizoom_card_account_permission: 编辑使用微众卡用户的权限
########################################################################
@login_required
def edit_weizoom_card_account_permission(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME
	})
	return render_to_response('weizoom_card/editor/edit_account_has_permissions.html', c)