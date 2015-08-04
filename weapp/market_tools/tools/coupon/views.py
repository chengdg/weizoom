# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from core.jsonresponse import JsonResponse, create_response
from core import paginator, dateutil

from market_tools import export

from excel_response import ExcelResponse

from account.models import *
from models import *
from modules.member.module_api import get_member_by_id_list


COUNT_PER_PAGE = 20

FIRST_NAV_NAME = 'market_tools'
SECOND_NAV_NAME = 'coupon'


########################################################################
# list_coupons: 显示优惠券列表
########################################################################
@login_required
def list_coupons(request):
	coupon_rules = list(CouponRule.objects.filter(owner=request.user, is_active=True).order_by('-id'))
#	coupons = list(Coupon.objects.filter(owner=request.user).order_by('-id'))
#	member_ids = [c.member_id for c in coupons]
#	members = get_member_by_id_list(member_ids)
#	member_id2member = dict([(m.id, m) for m in members])
#	#获取coupon所属的rule的name
#	id2rule = dict([(rule.id, rule) for rule in CouponRule.objects.filter(owner=request.user)])
#
#	#统计是否有active的coupon
#	has_active_coupon = False
#	for coupon in coupons:
#		if coupon.status == COUPON_STATUS_UNUSED:
#			has_active_coupon = True
#		member_id = int(coupon.member_id)
#		if member_id in member_id2member:
#			coupon.member = member_id2member[member_id]
#		else:
#			coupon.member = ''
#		
#		coupon.rule_name = id2rule[coupon.coupon_rule_id].name
#
#	#识别不能被删除的coupon
#	#used_pool_id_set = set(Coupon.objects.filter(~Q(status=COUPON_STATUS_UNUSED)).values_list('coupon_pool_id', flat=True))
#	'''
#	used_rule_id_set = set(Coupon.objects.values_list('coupon_rule_id', flat=True))
#	for coupon_rule in coupon_rules:
#		coupon_rule.can_delete = True
#		if coupon_rule.id in used_rule_id_set:
#			coupon_rule.can_delete = False
#	'''
	
	#获取排行榜时间
	coupon_saller_data = CouponSallerDate.objects.filter(owner=request.user)
	if coupon_saller_data:
		coupon_saller_data = coupon_saller_data[0]
	else:
		coupon_saller_data = None

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
#		'coupons': coupons,
		'coupon_rules': coupon_rules,
#		'has_active_coupon': has_active_coupon,
		'coupon_saller_data': coupon_saller_data
	})
	return render_to_response('coupon/editor/coupons.html', c)


########################################################################
# create_coupon_rule: 创建优惠券池
########################################################################
@login_required
def create_coupon_rule(request):
	if request.method == 'GET':
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
		})
		return render_to_response('coupon/editor/edit_coupon_rule.html', c)
	else:
		is_valid_restrictions = request.POST.get('is_valid_restrictions', '0')
		if is_valid_restrictions=='0':
			valid_restrictions = -1
		else:
			valid_restrictions = request.POST.get('valid_restrictions', '0')
		CouponRule.objects.create(
			owner = request.user,
			name = request.POST.get('name', ''),
			money = request.POST.get('money', '0.0'),
			valid_days = request.POST.get('valid_days', '0'),
			valid_restrictions = valid_restrictions
		)

		return HttpResponseRedirect('/market_tools/coupon/')


########################################################################
# update_coupon_rule: 对优惠券规则进行更新操作
########################################################################
@login_required
def update_coupon_rule(request):
	rule_id = request.GET['rule_id']
	if request.method == 'GET':
		coupon_rule = CouponRule.objects.get(id=rule_id)

		#优惠券规则删除操作将优惠券规则置为不可用，不进行物理删除
		#每一个优惠券规则均可以被删除
		#if Coupon.objects.filter(coupon_rule=coupon_rule).count() > 0:
		#	coupon_rule.can_delete = False
		#lse:
		#coupon_rule.can_delete = True

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': SECOND_NAV_NAME,
			'coupon_rule': coupon_rule
		})
		return render_to_response('coupon/editor/edit_coupon_rule.html', c)
	else:
		CouponRule.objects.filter(id=rule_id).update(
			name = request.POST.get('name', ''),
		)

		return HttpResponseRedirect('/market_tools/coupon/')


########################################################################
# export_coupon_rule: 导出优惠劵规则
########################################################################
@login_required
def export_coupon_rule(request):
	coupon_rule_id = request.GET['rule_id']
	coupon_list  = [
		[u'优惠券', u'过期时间', u'抵扣金额']
	]
	coupons = Coupon.objects.filter(coupon_rule_id = coupon_rule_id)
	for coupon in coupons:
		coupon_list.append([
			coupon.coupon_id,
			coupon.expired_time,
			coupon.money
		])

	return ExcelResponse(coupon_list, output_name=u'优惠券'.encode('utf8'), force_csv=False)


########################################################################
# delete_coupon_rule: 删除优惠劵池
# 变更物理删除微逻辑删除
########################################################################
@login_required
def delete_coupon_rule(request):
	coupon_rule_id = request.GET['rule_id']
	CouponRule.objects.filter(id=coupon_rule_id).update(is_active=False)
	
	return HttpResponseRedirect('/market_tools/coupon/')


########################################################################
# delete_expired_coupon: 删除优惠劵池
########################################################################
@login_required
def delete_expired_coupon(request):
	Coupon.objects.filter(owner=request.user, status__in=[COUPON_STATUS_EXPIRED, COUPON_STATUS_DISCARD]).delete()
	
	return HttpResponseRedirect('/market_tools/coupon/')
