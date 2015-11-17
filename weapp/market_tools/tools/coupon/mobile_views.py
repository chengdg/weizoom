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
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core.dateutil import get_today
from core.exceptionutil import full_stack, unicode_full_stack
from core import paginator

from mall.promotion.models import *
from modules.member.models import *
from mall.models import *
from mall.models import Order as mall_order_model

import util as coupon_util

from modules.member.module_api import get_member_by_id_list
from modules.member.member_decorators import member_required

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

def get_coupon(request):
	"""
	手机端领取优惠券
	"""
	msg = None
	rule = None
	promotion = None
	rule_id = request.GET.get('rule_id', '0')
	rules = CouponRule.objects.filter(id=rule_id, owner_id=request.webapp_owner_id)
	if len(rules) != 1:
		msg = '没有此优惠券，请重试'
	else:
		rule = rules[0]
		promotion = Promotion.objects.get(type=PROMOTION_TYPE_COUPON, detail_id=rule.id)
		if rule.remained_count == 0:
			msg = '该优惠券已领光'
		elif promotion.status >= PROMOTION_STATUS_FINISHED:
			msg = '该优惠券使用期已过，不能领取'
	try:
		is_subscribed = request.member.is_subscribed
	except:
		is_subscribed = False
	c = RequestContext(request, {
		'page_title': u'获取优惠券',
		'rule': rule,
		'promotion': promotion,
		'msg': msg,
		'is_subscribed': is_subscribed,
		'hide_non_member_cover': True
	})
	return render_to_response('%s/coupon/webapp/coupon.html' % TEMPLATE_DIR, c)


def get_usage(request):
	"""
	个人中心：优惠券列表
	"""
	coupons = coupon_util.get_my_coupons(request.member.id)
	used_coupons = []
	unused_coupons = []
	expired_coupons = []

	for c in coupons:
		c.consumer_name = ''
		if c.status == COUPON_STATUS_USED:
			used_coupons.append(c)

		if c.status == COUPON_STATUS_UNUSED:
			unused_coupons.append(c)

		if c.status == COUPON_STATUS_EXPIRED:
			expired_coupons.append(c)

	c = RequestContext(request, {
		'page_title': u'我的优惠券',
		'coupons': coupons,
		'used_coupons': used_coupons,
		'unused_coupons': unused_coupons,
		'expired_coupons': expired_coupons,
		'is_hide_weixin_option_menu': True
	})
	return render_to_response('%s/coupon/webapp/my_coupons.html' % TEMPLATE_DIR, c)
