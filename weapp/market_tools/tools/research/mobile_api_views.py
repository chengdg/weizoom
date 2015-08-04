# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core import chartutil

from core.alipay.alipay_submit import *
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
from core.alipay.alipay_notify import AlipayNotify
from core.alipay.alipay_submit import AlipaySubmit
from market_tools.tools.coupon.util import consume_coupon
from account.models import UserProfile
from account.views import save_base64_img_file_local_for_webapp
from models import *


########################################################################
# join_research:
########################################################################
def join_research(request):
	member = request.member
	webapp_user = request.webapp_user
	research_id = request.POST['research_id']

	try:
		research = Research.objects.get(id=research_id)
	except:
		response = create_response(500)
		response.errMsg = u'该调研不存在'
		response.innerErrMsg = full_stack()
		return response.get_response()	

	username = ''
	phone_number = ''
	if request.POST:
		try:
			items = ResearchItem.objects.filter(research=research)
			for item in items:
				input_name = '{}-{}'.format(item.id, item.type)
				if item.type == RESEARCHITEM_TYPE_IMAGE:
					file = request.POST[input_name]
					if file:
						value = save_base64_img_file_local_for_webapp(request, file)
					else:
						value = ''
				else:
					value = request.POST.get(input_name, '')

				if item.title == u'姓名':
					username = value
				if item.title == u'手机号':
					phone_number = value

				ResearchItemValue.objects.create(
					owner_id = request.webapp_owner_id,
					item = item,
					research = research,
					webapp_user = webapp_user,
					value = value
				)
				
			if member:
				try:
					member.update_member_info(username, phone_number)
				except:
					#不同步到会员
					pass
				
				#给予奖励
				#无奖励
				if research.prize_type == -1:
					pass
				#优惠券
				elif research.prize_type == 1:
					rule_id = research.prize_source
					# coupons = create_coupons(research.owner, rule_id, 1, member.id)
					consume_coupon(research.owner.id, rule_id, member.id)
				#积分
				elif research.prize_type == 3:
					prize_detail = research.prize_source
					#增加积分
					member.consume_integral(-int(prize_detail), u'参与调研，获得积分')
			
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'提交错误'
			response.innerErrMsg = full_stack()
			return response.get_response()
	else:
		response = create_response(500)
		response.errMsg = u'is not POST method'

	return response.get_response()