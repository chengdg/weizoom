#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import paginator

from modules.member.models import *
from core import resource
import export

COUNT_PER_PAGE = 20

class MemberSpread(resource.Resource):
	app = 'member'
	resource = 'member_spread'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBER_SPREAD,
		})

		return render_to_response('member/editor/member_spread.html', c)