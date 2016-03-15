# -*- coding: utf-8 -*-

__author__ = 'bert'

import os
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack
from core import core_setting
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from models import *

from modules.member.models import IntegralStrategySttings
from mall.models import Product,OrderHasProduct,Order
from mall.promotion import models as promotion_models

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_weizoom_card_login(request):
	member_id = request.member.id
	webapp_id = request.user_profile.webapp_id
	#判断是不是退出登录
	is_quit = request.GET.get('is_quit',0)
	member_has_card = promotion_models.CardHasExchanged.objects.filter(webapp_id = webapp_id,owner_id = member_id)
	
	if member_has_card.count() > 0 and is_quit == 0:
		card_id = member_has_card[0].card_id
		weizoom_card = WeizoomCard.objects.get(id=card_id)
		weizoom_card_orders_list = search_card_money(request,card_id)
		c = RequestContext(request, {
			'page_title': u'微众卡',
			'is_hide_weixin_option_menu': True,
			'weizoom_card': weizoom_card,
			'card_orders': weizoom_card_orders_list
		})
		return render_to_response('%s/weizoom_card/webapp/weizoom_card_change_info.html' % TEMPLATE_DIR, c)
	else:
		c = RequestContext(request, {
			'page_title': u'微众卡',
			'is_hide_weixin_option_menu': True
		})
		return render_to_response('%s/weizoom_card/webapp/weizoom_card_login.html' % TEMPLATE_DIR, c)

def get_weizoom_card_change_money(request):
	card_id = request.GET.get('card_id', -1)
	weizoom_card_orders_list = []
	member_id = request.member.id
	member_has_card = promotion_models.CardHasExchanged.objects.filter(card_id = card_id,owner_id = member_id)
	if member_has_card.count() > 0 :
		member_has_card = member_has_card[0]
		weizoom_card_orders_list.append({
			'created_at': member_has_card.created_at,
			'money': '%.2f' % WeizoomCard.objects.get(id=card_id).money,
			'product_name': u'兑换平台',
			'event_type': u'积分兑换'
		})
		
	integral_each_yuan = IntegralStrategySttings.get_integral_each_yuan(request.user_profile.webapp_id)
	# jz 2015-10-20
	# auth_key = request.COOKIES[core_setting.WEIZOOM_CARD_AUTH_KEY]
	# if WeizoomCard.objects.filter(id=card_id).count() > 0 and WeizoomCardUsedAuthKey.is_can_pay(auth_key, card_id) and integral_each_yuan:	

	if WeizoomCard.objects.filter(id=card_id).count() > 0 and integral_each_yuan:
		weizoom_card = WeizoomCard.objects.get(id=card_id)
		weizoom_card_orders = WeizoomCardHasOrder.objects.filter(card_id = card_id).exclude(order_id__in = [-1]).order_by('-created_at')
		orders = Order.objects.all()
		orders_has_product = OrderHasProduct.objects.all()
		for order in weizoom_card_orders:
			cur_order_id = orders.get(order_id = order.order_id).id
			weizoom_card_orders_has_product = orders_has_product.filter(order_id = cur_order_id)
			product_name_str = ''
			for a in weizoom_card_orders_has_product:
				product_name = a.product.name
				product_name_str = product_name_str + str(product_name)+ ','
			event_type = order.event_type
			weizoom_card_orders_list.append({
				'created_at': order.created_at,
				'money': '%.2f' % order.money,
				'product_name': product_name_str,
				'event_type': event_type
			})

	if len(weizoom_card_orders_list) <= 0:
		c = RequestContext(request, {
			'page_title': u'微众卡',
			'is_hide_weixin_option_menu': True
		})

		return render_to_response('%s/weizoom_card/webapp/weizoom_card_login.html' % TEMPLATE_DIR, c)

	change_integral = weizoom_card.money * integral_each_yuan
	if change_integral > int(change_integral):
		change_integral = int(change_integral) + 1
	change_integral = int(change_integral)
	is_can_pay = True if change_integral > 0 else False
	c = RequestContext(request, {
		'page_title': u'微众卡',
		'is_hide_weixin_option_menu': True,
		'weizoom_card': weizoom_card,
		'is_can_pay': is_can_pay,
		'change_integral': change_integral,
		'card_orders': weizoom_card_orders_list
	})
	return render_to_response('%s/weizoom_card/webapp/weizoom_card_change_info.html' % TEMPLATE_DIR, c)

def search_card_money(request,card_id):

	integral_each_yuan = IntegralStrategySttings.get_integral_each_yuan(request.user_profile.webapp_id)
	# jz 2015-10-20
	# auth_key = request.COOKIES[core_setting.WEIZOOM_CARD_AUTH_KEY]
	# if WeizoomCard.objects.filter(id=card_id).count() > 0 and WeizoomCardUsedAuthKey.is_can_pay(auth_key, card_id) and integral_each_yuan:
	weizoom_card_orders_list = []
	if WeizoomCard.objects.filter(id=card_id).count() > 0 and integral_each_yuan:
		weizoom_card = WeizoomCard.objects.get(id=card_id)
		weizoom_card_orders = WeizoomCardHasOrder.objects.filter(card_id = card_id).exclude(order_id__in = [-1]).order_by('-created_at')
		orders = Order.objects.all()
		orders_has_product = OrderHasProduct.objects.all()
		for order in weizoom_card_orders:
			cur_order_id = orders.get(order_id = order.order_id).id
			weizoom_card_orders_has_product = orders_has_product.filter(order_id = cur_order_id)
			product_name_str = ''
			for a in weizoom_card_orders_has_product:
				product_name = a.product.name
				product_name_str = product_name_str + str(product_name)+ ','
			event_type = order.event_type
			weizoom_card_orders_list.append({
				'created_at': order.created_at,
				'money': '%.2f' % order.money,
				'product_name': product_name_str,
				'event_type': event_type
			})
	else:
		weizoom_card_orders_list = []

	return weizoom_card_orders_list

