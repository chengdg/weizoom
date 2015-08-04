# -*- coding: utf-8 -*-

from datetime import timedelta, datetime, date

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required, permission_required

from shihuazhiye.settings import FIRST_NAV_NAME
from shihuazhiye.settings import LEFT_NAVS as HOME_SECOND_NAVS

from apps.register import view_func

from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack

########################################################################
# list_course: 课程编辑列表页
########################################################################
@login_required
@view_func(resource='product_list', action='get')
def list_course(request):
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': HOME_SECOND_NAVS,
		'second_nav_name': 'product_list'
	})
	return render_to_response('editor/list_product.html', c) 
