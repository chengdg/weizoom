# -*- coding: utf-8 -*-
"""@package mall.home_views
商品首页模块的实现文件
"""

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


import models as mall_models
from models import *
import export
from core import dateutil
from core.restful_url_route import *
from modules.member import models as member_models
from .notices_models import Notice

import export
from mall.promotion import models as promotion_models
COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_HOME_FIRST_NAV


def __get_to_be_shipped_order_infos(request):
	"""
	获取待发货订单信息
	返回数据格式如下:
	{
		"count": 20,
		"orders_list": [{
			"date": "2015-02-01",
			"items": [order1, order2]
		}, {
			......
		}]
	}
	"""
	webapp_id = request.user_profile.webapp_id
	total_to_be_shipped_order_count = Order.objects.belong_to(webapp_id).filter(status=ORDER_STATUS_PAYED_NOT_SHIP).filter(~Q(type='test')).count()
	orders = Order.objects.belong_to(webapp_id).filter(status=ORDER_STATUS_PAYED_NOT_SHIP).filter(~Q(type='test')).order_by('-id')[:10]
	order_ids = []
	id2order = {}
	for order in orders:
		order_ids.append(order.id)
		id2order[order.id] = order
		order.product_count = 0

	for relation in list(OrderHasProduct.objects.filter(order_id__in=order_ids)):
		id2order[relation.order_id].product_count += relation.number
	
	date2orders = {}
	for order in orders:
		date = order.created_at.strftime("%Y-%m-%d")
		date2orders.setdefault(date, []).append(order)

	orders_list = []
	for date, orders in date2orders.items():
		orders_list.append({
			"date": date,
			"items": orders
		})
	orders_list.sort(lambda x,y: cmp(y['date'], x['date']))

	return {
		"count": total_to_be_shipped_order_count,
		"orders_list": orders_list
	}


@view(app='mall', resource='outline', action='get')
@login_required
def get_outline(request):
	webapp_id = request.user_profile.webapp_id
	if not settings.IS_UNDER_BDD:
		if request.manager.id != request.user.id:
			# 子账号
			if len(request.user.permission_set) == 0:
				# 没有权限页面
				return render_to_response('mall/editor/outline_no_permission.html', RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': export.get_home_second_navs(request),
					'second_nav_name': export.MALL_HOME_INTEGRAL_NAV,}
				))
			else:
				first_url = export.get_first_navs(request.user)[0]['url']
				# print 'jz----', first_url, first_url.find('/mall/outline/get') < 0
				if first_url.find('/mall/outline/get') < 0:
					# 第一个有权限的一面，不是首页
					return HttpResponseRedirect(first_url)
		integral_strategy = member_models.IntegralStrategySttings.objects.get(webapp_id=webapp_id)
		if integral_strategy.use_ceiling == -1:
			# 需要进入积分引导页
			return HttpResponseRedirect('/mall/integral_strategy/get/')

	#获取待支付订单	
	to_be_shipped_orders = __get_to_be_shipped_order_infos(request)

	#获得昨日订单数据
	today = '%s 00:00:00' % dateutil.get_today()
	yesterday = '%s 00:00:00' % dateutil.get_yesterday_str('today')
	orders = Order.objects.belong_to(webapp_id).filter(created_at__range=(yesterday, today))
	statuses = set([ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED])
	#orders = [order for order in orders if (order.type != 'test') and (order.status != ORDER_STATUS_CANCEL)]
	orders = [order for order in orders if (order.type != 'test') and (order.status in statuses)]
	order_money = 0.0
	for order in orders:
		order_money += order.final_price + order.weizoom_card_money

	#获取会员数
	total_member_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True).count()
	members = member_models.Member.objects.filter(webapp_id=webapp_id, created_at__range=(yesterday, today))
	members = [member for member in members if member.is_subscribed]

	outline_counts = [{
		"count": len(orders),
		"description": "昨日下单数"
	}, {
		"count": order_money,
		"description": "昨日成交额"
	}, {
		"count": len(members),
		"description": "昨日新增会员"
	}, {
		"count": total_member_count,
		"description": "店铺会员总数"
	}]

	messages = Notice.objects.all().order_by('-id')[:5]

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_home_second_navs(request),
		'second_nav_name': export.MALL_HOME_OUTLINE_NAV,
		'order_info': to_be_shipped_orders,
		'outline_counts': outline_counts,
		'system_messages': messages
	})
	return render_to_response('mall/editor/outline.html', c)


@view(app='mall', resource='integral_strategy', action='get')
@login_required
def get_integral_strategy(request):
	webapp_id = request.user_profile.webapp_id
	integral_strategy = member_models.IntegralStrategySttings.objects.get(webapp_id=webapp_id)
	has_a_integral_strategy = True if promotion_models.Promotion.objects.filter(owner=request.manager, status=promotion_models. PROMOTION_STATUS_STARTED, type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE)  else False
	show_guide = False
	if integral_strategy.use_ceiling == -1:
		# 需要进入积分引导页
		show_guide = True
		integral_strategy.use_ceiling = 0
		member_models.IntegralStrategySttings.objects.filter(webapp_id=webapp_id).update(use_ceiling=0)
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV,
		'second_navs': export.get_home_second_navs(request),
		'second_nav_name': export.MALL_HOME_INTEGRAL_NAV,
		'integral_strategy': integral_strategy,
		'has_a_integral_strategy':  has_a_integral_strategy,
		'show_guide': show_guide
	})
	return render_to_response('mall/editor/integral_strategy.html', c)


@view(app='mall', resource='integral_strategy', action='update')
@login_required
def update_integral_strategy(request):
	webapp_id = request.user_profile.webapp_id
	member_models.IntegralStrategySttings.objects.filter(webapp_id=webapp_id).update(
		integral_each_yuan = request.POST['integral_each_yuan'],
		be_member_increase_count = request.POST['be_member_increase_count'],
		click_shared_url_increase_count = request.POST['click_shared_url_increase_count'],
		buy_award_count_for_buyer = request.POST['buy_award_count_for_buyer'],
		order_money_percentage_for_each_buy = request.POST['order_money_percentage_for_each_buy'],
		buy_via_shared_url_increase_count_for_author = request.POST['buy_via_shared_url_increase_count_for_author'],
		buy_via_offline_increase_count_for_author = request.POST['buy_via_offline_increase_count_for_author'],
		buy_via_offline_increase_count_percentage_for_author = request.POST['buy_via_offline_increase_count_percentage_for_author'],
		use_ceiling=request.POST['use_ceiling'] if request.POST['use_ceiling'] else 0,
		review_increase=request.POST['review_increase']
	)

	return HttpResponseRedirect('/mall/integral_strategy/get/')
