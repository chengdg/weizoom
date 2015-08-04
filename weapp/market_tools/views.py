# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from export import get_second_navs


FIRST_NAV_NAME = 'market_tools'

@login_required
def show_dashboard(request):
	#add by likunlun  营销工具返回第一个工具
	try:
		navs = get_second_navs(request)[0]['navs']
		first_nav = navs[0]
		first_nav_url = first_nav['url']
	
		return HttpResponseRedirect(first_nav_url)
	except:
		c = RequestContext(request, {
			'first_nav_name' : FIRST_NAV_NAME,
			'second_navs': get_second_navs(request),
			'second_nav_name': 'dashboard',
		})
		return render_to_response('market_tools/dashboard.html', c)