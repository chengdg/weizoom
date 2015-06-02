# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from watchdog.utils import watchdog_fatal, watchdog_error

from shengjing.models import *

from shengjing.settings import FIRST_NAV_NAME
from shengjing.settings import LEFT_NAVS as HOME_SECOND_NAVS

from apps.register import api, view_func

########################################################################
# settings_page: 显示商品分类列表
########################################################################
@login_required
@view_func(resource='score', action='get')
def get_integral_strategy_settings(request):
	settings , _ = ShengjingIntegralStrategySttings.objects.get_or_create(webapp_id=request.user.get_profile().webapp_id)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': HOME_SECOND_NAVS,
		'second_nav_name': 'integral_settings',
		'settings': settings,
	})

	return render_to_response('editor/edit_integral.html' , c)


