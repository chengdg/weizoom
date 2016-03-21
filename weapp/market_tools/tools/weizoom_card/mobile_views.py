# -*- coding: utf-8 -*-
from card.card_view import WEIZOOM_CARD_BELONG_TO_OWNER

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
from market_tools.tools.card_exchange import mobile_views
from mall.promotion.card_exchange import CardExchange
from modules.member.models import MemberInfo
from market_tools.tools.weizoom_card import models as card_models

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_weizoom_card_login(request):
	user_id = request.user_profile.user_id
	user = User.objects.filter(id=user_id)
	username = None
	if user.count() > 0:
		username = user[0].username
	if username and username == 'fulilaile':
		member_id = request.member.id
		webapp_id = request.user_profile.webapp_id
		#判断是不是退出登录
		# is_quit = request.GET.get('is_quit',0)
		member_has_card = promotion_models.CardHasExchanged.objects.filter(webapp_id = webapp_id,owner_id = member_id)
		if member_has_card.count() > 0:
			#已经兑换过微众卡，直接进入卡列表
			c = get_weizoom_card_exchange_list(request)
			return c
		else:
			#没有兑换过微众卡，直接进入兑换页面
			member_integral = request.member.integral
			phone_number = ''
			try:
				member_info = MemberInfo.objects.get(member_id = member_id)
				member_is_bind = member_info.is_binded
				if member_is_bind:
					phone_number = member_info.phone_number
			except:
				member_is_bind = False
			card_exchange_dic = CardExchange.get_can_exchange_cards(request,webapp_id)

			weizoom_card_id = 0
			cur_user_has_exchange_card = promotion_models.CardHasExchanged.objects.filter(webapp_id = webapp_id,owner_id = member_id)
			# user_has_exchange_card = False
			if cur_user_has_exchange_card.count() > 0 :
				# user_has_exchange_card = True
				card_id = cur_user_has_exchange_card[0].card_id
				try:
					weizoom_card_id = card_models.WeizoomCard.objects.get(id = card_id).weizoom_card_id
				except:
					weizoom_card_id = None

			prize_list = card_exchange_dic['prize']
			if weizoom_card_id:
				for p in prize_list:
					card_number = p['card_number']
					s_w_id = int(card_number.split('-')[0])
					e_w_id = int(card_number.split('-')[1])
					if int(weizoom_card_id) >= s_w_id and int(weizoom_card_id) <= e_w_id:
						p['is_selected'] = True
					else:
						p['is_selected'] = False

			c = RequestContext(request, {
				'card_exchange_rule': card_exchange_dic,
				'member_is_bind': member_is_bind,
				'member_integral': member_integral,
				'phone_number': phone_number,
				# 'user_has_exchange_card': user_has_exchange_card
			})

			return render_to_response('card_exchange/templates/card_exchange/webapp/m_card_exchange.html', c)
	else:
		c = RequestContext(request, {
				'page_title': u'微众卡',
				'is_hide_weixin_option_menu': True,
				'normal': True
			})
		return render_to_response('%s/weizoom_card/webapp/weizoom_card_login.html' % TEMPLATE_DIR, c)

def get_weizoom_card_exchange_list(request):
	"""
	兑换卡列表
	"""
	member_id = request.member.id
	webapp_id = request.user_profile.webapp_id
	card_details_dic = {}
	card_details_list = []
	member_has_cards = promotion_models.CardHasExchanged.objects.filter(webapp_id = webapp_id,owner_id = member_id).order_by('-created_at')
	total_money = 0
	count = member_has_cards.count()
	phone_number = MemberInfo.objects.get(member_id = member_id).phone_number
	
	card_details_dic['phone_number'] = phone_number
	count = member_has_cards.count()
	for card in member_has_cards:
		card_id = card.card_id
		cur_card = card_models.WeizoomCard.objects.get(id = card_id)
		total_money += cur_card.money
		is_expired = cur_card.is_expired
		status = cur_card.status
		if is_expired or status == card_models.WEIZOOM_CARD_STATUS_INACTIVE:
			count -= 1
		card_details_list.append({
			'card_id': cur_card.weizoom_card_id,
			'remainder': '%.2f' % cur_card.money,
			'money': '%.2f' % cur_card.weizoom_card_rule.money,
			'time': card.created_at.strftime("%Y-%m-%d"),
			'type': u'兑换平台',
			'is_expired': is_expired,
			'status': status 
		})

	card_details_dic['total_money'] = '%.2f' % total_money
	card_details_dic['count'] = count
	card_details_dic['card'] = card_details_list
	
	c = RequestContext(request, {
		'page_title': u'微众卡',
		'cards': card_details_dic,
		# 'card_orders': weizoom_card_orders_list
	})
	return render_to_response('card_exchange/templates/card_exchange/webapp/m_card_exchange_list.html', c)


def get_card_exchange_detail(request):
	"""
	兑换卡详情
	"""
	card_id = request.GET.get('card_id',None)
	integral_each_yuan = IntegralStrategySttings.get_integral_each_yuan(request.user_profile.webapp_id)
	weizoom_card_orders_list = search_card_money(request,card_id,integral_each_yuan)
	card = WeizoomCard.objects.get(id=card_id)
	valid_restrictions = card.weizoom_card_rule.valid_restrictions
	c = RequestContext(request, {
		'card_orders': weizoom_card_orders_list,
		'weizoom_card': card,
		'valid_restrictions': '%.2f' % valid_restrictions
	})

	return render_to_response('%s/weizoom_card/webapp/weizoom_card_change_info.html' % TEMPLATE_DIR, c)

def get_weizoom_card_change_money(request):
	card_id = request.GET.get('card_id', -1)
	normal = request.GET.get('normal', 0)

	integral_each_yuan = IntegralStrategySttings.get_integral_each_yuan(request.user_profile.webapp_id)

	if normal:
		weizoom_card_info = {}
		weizoom_card = WeizoomCard.objects.filter(id=card_id)
		if weizoom_card.count() > 0 and integral_each_yuan:
			weizoom_card = weizoom_card[0]
			weizoom_card_info['weizoom_card_id'] = weizoom_card.weizoom_card_id
			weizoom_card_info['money'] = weizoom_card.money
			rule = WeizoomCardRule.objects.filter(id=weizoom_card.weizoom_card_rule_id)
			if rule.count() > 0:
				rule = rule[0]
				weizoom_card_info['valid_restrictions'] = rule.valid_restrictions if rule.valid_restrictions != -1 else ''
				weizoom_card_info['valid_time_from'] = rule.valid_time_from.strftime('%Y/%m/%d %H:%M')
				weizoom_card_info['valid_time_to'] = rule.valid_time_to.strftime('%Y/%m/%d %H:%M')
				shop_limit_list = rule.shop_limit_list.split(',') if rule.shop_limit_list != -1 else ''
				shop_black_list = rule.shop_black_list.split(',') if rule.shop_black_list != -1 else ''
				shop_list_name = u''
				if shop_limit_list:
					if shop_black_list:
						shop_list = set(shop_limit_list) - set(shop_black_list)
					else:
						shop_list = shop_limit_list
					shop_list_name = [u.store_name for u in UserProfile.objects.filter(user_id__in=shop_list)]
				else:
					if shop_black_list:
						owner_ids = [ahwcp.owner_id for ahwcp in AccountHasWeizoomCardPermissions.objects.filter(is_can_use_weizoom_card=True)]
						shop_list = set(owner_ids) - set(shop_black_list)
						shop_list_name = [u.store_name for u in UserProfile.objects.filter(user_id__in=shop_list)]
				weizoom_card_info['shop_list'] = ' '.join(shop_list_name)
				weizoom_card_info['shop_list_name'] = shop_list_name

			card_info_list = get_card_detail_normal(request,card_id)

		else:
			c = RequestContext(request, {
				'page_title': u'微众卡',
				'is_hide_weixin_option_menu': True,
				'normal': True
			})
			return render_to_response('%s/weizoom_card/webapp/weizoom_card_login.html' % TEMPLATE_DIR, c)

		c = RequestContext(request, {
			'page_title': u'微众卡',
			'is_hide_weixin_option_menu': True,
			'weizoom_card': weizoom_card_info,
			'card_orders': card_info_list
		})
		return render_to_response('%s/weizoom_card/webapp/weizoom_card_info_normal.html' % TEMPLATE_DIR, c)
	else:

		weizoom_card_orders_list = search_card_money(request,card_id,integral_each_yuan)

		# if len(weizoom_card_orders_list) <= 0:
		# 	c = RequestContext(request, {
		# 		'page_title': u'微众卡',
		# 		'is_hide_weixin_option_menu': True
		# 	})
	    #
		# 	return render_to_response('%s/weizoom_card/webapp/weizoom_card_login.html' % TEMPLATE_DIR, c)
		weizoom_card = WeizoomCard.objects.get(id=card_id)
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

def search_card_money(request,card_id,integral_each_yuan):
	weizoom_card_orders_list = []
	member_id = request.member.id
	member_has_card = promotion_models.CardHasExchanged.objects.filter(card_id = card_id,owner_id = member_id)
	if member_has_card.count() > 0 :
		member_has_card = member_has_card[0]
		weizoom_card_orders_list.append({
			'created_at': member_has_card.created_at,
			'money': '%.2f' % WeizoomCard.objects.get(id=card_id).weizoom_card_rule.money,
			'product_name': u'兑换平台',
			'event_type': u'积分兑换'
		})
	if WeizoomCard.objects.filter(id=card_id).count() > 0 and integral_each_yuan:
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
			if product_name_str:
				product_name_str = product_name_str[:-1]
			event_type = order.event_type
			weizoom_card_orders_list.append({
				'created_at': order.created_at,
				'money': '%.2f' % order.money,
				'product_name': product_name_str,
				'event_type': event_type
			})

	return weizoom_card_orders_list

def get_card_detail_normal(request,card_id):
	store_name = request.user_profile.store_name
	card_orders = WeizoomCardHasOrder.objects.filter(card_id=card_id).exclude(order_id__in=[-1]).order_by('-created_at')
	order_nums = [co.order_id for co in card_orders]
	orders = Order.objects.filter(order_id__in=order_nums)
	order_id2orders = {o.order_id: o for o in orders}
	order_ids = [o.id for o in orders]

	order_id2Product = {}
	for ohp in OrderHasProduct.objects.filter(order_id__in=order_ids):
		if not order_id2Product.get(ohp.order_id, None):
			order_id2Product[ohp.order_id] = [ohp]
		else:
			order_id2Product[ohp.order_id].append(ohp)
	card_info_list = []
	for order in card_orders:
		order_id = order_id2orders[order.order_id].id
		products = order_id2Product[order_id]
		product_name_list = []
		for p in products:
			product_name_list.append(p.product.name)

		card_info_list.append({
			'created_at': order.created_at,
			'money': '%.2f' % order.money,
			'product_name': u'[%s-商品] %s' % (store_name,','.join(product_name_list))
		})
	return card_info_list