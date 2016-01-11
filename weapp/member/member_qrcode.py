#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import paginator
#import sys
#from mall.models import Order, STATUS2TEXT

from modules.member.models import *
from watchdog.utils import watchdog_error
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from excel_response import ExcelResponse
from market_tools.tools.coupon.util import get_coupon_rules, get_my_coupons
# from market_tools.tools.member_qrcode import api_views as member_qrcode_api_views
# from market_tools.tools.member_qrcode.models import *
# from apps.customerized_apps.shengjing.models import *
from weixin2.models import get_opid_from_session
from core import resource
import export

COUNT_PER_PAGE = 20

class MemberQrcode(resource.Resource):
	app = 'member'
	resource = 'member_qrcode'

	@login_required
	def get(request):
		mpuser = get_system_user_binded_mpuser(request.user)

		if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
			should_show_authorize_cover = True
		else:
			should_show_authorize_cover = False

		coupon_rules = get_coupon_rules(request.user)
		member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner=request.user)
		member_qrcode_setting = member_qrcode_settings[0] if member_qrcode_settings.count() > 0 else None
		if member_qrcode_setting:
			award_contents = MemberQrcodeAwardContent.objects.filter(member_qrcode_settings=member_qrcode_setting)
			if award_contents.count() > 0:
				award_content = award_contents[0] if member_qrcode_setting.award_member_type == 1 else None
			else:
				award_content = None
		else:
			award_contents = None
			award_content = None
		member_grades = MemberGrade.get_all_grades_list(request)

		if member_grades and award_contents:

			for member_grade in member_grades:
				content = award_contents.filter(member_level=member_grade.id)[0] if award_contents.filter(member_level=member_grade.id).count() > 0 else None
				if content:
					member_grade.award_type = content.award_type
					member_grade.award_content = content.award_content
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBER_QRCODE,
			'member_grades': member_grades,
			'member_qrcode_settings': member_qrcode_setting,
			'coupon_rules': coupon_rules,
			'award_content': award_content,
			'member_grades': member_grades,
			'should_show_authorize_cover': should_show_authorize_cover,
			'is_hide_weixin_option_menu': True
		})

		return render_to_response('member/editor/member_qrcode.html', c)

	@login_required
	def api_post(request):
		response = member_qrcode_api_views.edit_member_qrcode_settings(request)
		return response