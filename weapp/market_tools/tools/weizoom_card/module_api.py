# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import copy
import shutil
import random

from itertools import chain

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from tools.regional import views as regional_util
from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import dateutil, core_setting
from tools.express import util as express_util

from models import *
from mall.models import Order,belong_to, ORDER_STATUS_CANCEL
from watchdog.utils import watchdog_alert


#############################################################################
# is_weizoom_card_use_permission_by_owner_id: 根据owner_id获取微众卡使用权限
#############################################################################
from weixin.user.models import WeixinMpUser, MpuserPreviewInfo, ComponentAuthedAppidInfo


def is_weizoom_card_use_permission_by_owner_id(owner_id):
	try:
		return AccountHasWeizoomCardPermissions.objects.get(owner_id = owner_id).is_can_use_weizoom_card
	except:
		return False
	
	
#############################################################################
# get_order_id: 获取定单使用的微众卡的id
#############################################################################
def get_order_id(order_id):
	return Order.objects.get(order_id=order_id).id


def return_weizoom_card_money(order):
	"""
	订单取消，回退微众卡余额
	"""
	if WeizoomCardHasOrder.objects.filter(order_id=order.order_id).count() > 0:
		for weizoom_card_has_order in WeizoomCardHasOrder.objects.filter(order_id=order.order_id):
			return_money = weizoom_card_has_order.money
			# if weizoom_card_has_order.money < 0:
			# 	return_money = -weizoom_card_has_order.money

			weizoom_cards = WeizoomCard.objects.filter(id=weizoom_card_has_order.card_id)

			if weizoom_cards.count() > 0:
				weizoom_card = weizoom_cards[0]
				weizoom_card.money = weizoom_card.money + return_money
				if weizoom_card.status != WEIZOOM_CARD_STATUS_INACTIVE:
					weizoom_card.status=WEIZOOM_CARD_STATUS_USED
				weizoom_card.save()

			# 创建记录
			create_weizoom_card_log(
				weizoom_card_has_order.owner_id, 
				order.order_id, 
				WEIZOOM_CARD_LOG_TYPE_BUY_RETURN, 
				weizoom_card_has_order.card_id, 
				-weizoom_card_has_order.money
			)

def check_weizoom_card(name, password,webapp_user=None,member=None,owner_id=None,webapp_id=None):
	msg = None
	weizoom_card = {}
	weizoom_card = WeizoomCard.objects.filter(weizoom_card_id=name, password=password)

	if len(weizoom_card) == 1:
		weizoom_card = weizoom_card[0]
		weizoom_card_rule = WeizoomCardRule.objects.get(id=weizoom_card.weizoom_card_rule_id)
		rule_id = weizoom_card.weizoom_card_rule.id
		# print rule_id, owner_id
		today = datetime.today()
		if weizoom_card.is_expired:
			msg = u'微众卡已过期'
		elif weizoom_card.expired_time < today:
			weizoom_card.is_expired = True
			weizoom_card.save()
			msg = u'微众卡已过期'
		elif weizoom_card.status == WEIZOOM_CARD_STATUS_INACTIVE:
			msg = u'微众卡未激活'
		elif owner_id and weizoom_card_rule.card_attr:
			#专属卡
			#是否为新会员专属卡
			mpuser_name = u''
			authed_appid = ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id=weizoom_card_rule.belong_to_owner)
			if authed_appid.count()>0:
				if authed_appid[0].nick_name:
					mpuser_name = authed_appid[0].nick_name
			if weizoom_card_rule.is_new_member_special:
				if member and member.is_subscribed:
					orders = belong_to(webapp_id)
					orders = orders.filter(webapp_id=webapp_id,webapp_user_id=webapp_user.id).exclude(status=ORDER_STATUS_CANCEL)
					has_order = orders.count() >0
					#判断是否首次下单
					if has_order:
						order_ids = [order.order_id for order in orders]
						#不是首次下单，判断该卡是否用过
						has_use_card = WeizoomCardHasOrder.objects.filter(card_id=weizoom_card.id,order_id__in=order_ids).count()>0
						if not has_use_card:
							msg = u'该卡为新会员专属卡'
					if owner_id != weizoom_card_rule.belong_to_owner:
						msg = u'该卡为'+mpuser_name+'商家专属卡'
				else:
					msg = u'该卡为新会员专属卡'
			else:
				if owner_id != weizoom_card_rule.belong_to_owner:
					msg = u'该卡为'+mpuser_name+'商家专属卡'
		elif owner_id and rule_id in [23, 36] and owner_id != 157:
			WeizoomCardRule.objects.get(id=rule_id)
			if '吉祥大药房' in weizoom_card.weizoom_card_rule.name:
				msg = u'抱歉，该卡仅可在吉祥大药房微站使用！'
		elif owner_id and rule_id in [99,] and owner_id != 474:
			WeizoomCardRule.objects.get(id=rule_id)
			if '爱伲' in weizoom_card.weizoom_card_rule.name:
				msg = u'抱歉，该卡仅可在爱伲咖啡微站使用！'
		# else:
		# 	WeizoomCardUsedAuthKey.objects.get_or_create(weizoom_card_id=weizoom_card.id, auth_key=request.COOKIES[core_setting.WEIZOOM_CARD_AUTH_KEY])
	else:
		msg = u'卡号或密码错误'
	return msg, weizoom_card


def use_weizoom_card(weizoom_card, final_price=0):
	"""
	使用微众卡抵扣
	参数 request、卡号、密码、订单金额
	返回微众卡id、使用金额，如果为None则抵扣成功
	"""
	# webapp_owner_id = request.webapp_owner_id
	# auth_key=request.COOKIES[core_setting.WEIZOOM_CARD_AUTH_KEY]

	# if WeizoomCardUsedAuthKey.is_can_pay(auth_key, weizoom_card.id):
	if final_price >= weizoom_card.money:
		use_price = float(weizoom_card.money)
		weizoom_card.money = 0
		status = WEIZOOM_CARD_STATUS_EMPTY
	else:
		use_price = final_price
		weizoom_card.money = float(weizoom_card.money) - use_price
		status = WEIZOOM_CARD_STATUS_USED
	weizoom_card.status = status
	weizoom_card.save()
	# else: 
	# 	msg = u'交易已过期'

	# WeizoomCardUsedAuthKey.objects.filter(auth_key=auth_key, weizoom_card_id=weizoom_card.id).delete()

	return use_price

#############################################################################
# create_weizoom_card_log: 创建微众卡日志
#############################################################################
def create_weizoom_card_log(owner_id, order_id, event_type, card_id, money, member_integral_log_id=0):
	try:		
		if money != 0:			
			if event_type in TYPE_ZERO:
				money = 0

			WeizoomCardHasOrder.objects.create(		
				owner_id = owner_id,
				card_id = card_id,
				order_id = order_id,
				money = money,
				event_type = event_type,
				member_integral_log_id = member_integral_log_id
			)
	except:
		notify_msg = u"创建微众卡日志失败, card_id={},order_id={},event_type={}, money={}, cause:\n{}".format(card_id,order_id,event_type, money, unicode_full_stack())
		watchdog_alert(notify_msg)
