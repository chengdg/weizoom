# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack
from core import paginator

from models import *
from webapp.modules.mall.models import *
from webapp.modules.mall.models import Order as mall_order_model

import util as coupon_util

from modules.member.module_api import get_member_by_id_list
from modules.member.integral import increase_member_integral

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]


########################################################################
# get_usage: 充值
########################################################################
def get_usage(request):
	if request.POST:
		point_card_id = request.POST['point_card_id']
		password = request.POST['password']
		point_card = PointCard.objects.filter(owner_id=request.webapp_owner_id, point_card_id=point_card_id, password=password)
		if len(point_card)>0:
			point_card = point_card.filter(status=POINT_CARD_STATUS_UNUSED)
			if len(point_card)>0:
				webapp_user = request.webapp_user
				member = webapp_user.get_member_by_webapp_user_id(webapp_user.id)
				if member:
					increase_member_integral(member, point_card[0].point, u'积分充值')
					point_card[0].member_id = member.id
					point_card[0].status = POINT_CARD_STATUS_USED
					point_card[0].save()
				c = RequestContext(request, {
					'point' : point_card[0].point
				})
				return render_to_response('point_card/weapp/get_point_card_success.html', c) 
			else:
				c = RequestContext(request, {
					'errorMsg': u'该卡己被使用，请重新输入'
				})
			return render_to_response('point_card/weapp/get_point_card.html', c)
		else:
			c = RequestContext(request, {
				'errorMsg': u'卡号或密码错误，请重新输入'
			})
			return render_to_response('point_card/weapp/get_point_card.html', c)
	c = RequestContext(request, {
	})
	return render_to_response('point_card/weapp/get_point_card.html', c)