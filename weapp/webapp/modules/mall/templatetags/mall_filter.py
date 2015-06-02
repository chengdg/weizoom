# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from core import emotion

from datetime import datetime
from webapp.modules.mall.models import *

register = template.Library()

order_status2text = {
	ORDER_STATUS_NOT: u'待支付',
	ORDER_STATUS_CANCEL: u'已取消',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成'
}
@register.filter(name='get_order_status_text')
def get_order_status_text(order):
	return order_status2text[order.status]


order_status2text = {
	ORDER_STATUS_NOT: u'待支付',
	ORDER_STATUS_CANCEL: u'已取消',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成'
}
@register.filter(name='get_order_status_color')
def get_order_status_color(order):
	if order.status == ORDER_STATUS_NOT or order.status == ORDER_STATUS_PAYED_NOT_SHIP:
		return '#FF0000'
	elif order.status == ORDER_STATUS_SUCCESSED or order.status == ORDER_STATUS_PAYED_SHIPED:
		return 'green'
	elif order.status == ORDER_STATUS_CANCEL:
		return '#AFAFAF'
	else:
		return '#000000'


@register.filter(name='format_float')
def format_float(value):
	return '%.2f' % value


ORDER_PAY_ACTION = {
	'name': u'支付',
	'action': 'pay',
	'button_class': 'btn-success'	
}
ORDER_SHIP_ACTION = {
	'name': u'发货',
	'action': 'ship',
	'button_class': 'btn-success'	
}
ORDER_FINISH_ACTION = {
	'name': u'完成',
	'action': 'finish',
	'button_class': 'btn-success'	
}
ORDER_CANCEL_ACTION = {
	'name': u'取消',
	'action': 'cancel',
	'button_class': 'btn-danger'
}
@register.filter(name='get_order_actions')
def get_order_actions(order):
	if order.pay_interface_type == PAY_INTERFACE_COD and order.status == ORDER_STATUS_PAYED_NOT_SHIP:
		return [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
	if order.status == ORDER_STATUS_NOT:
		return [ORDER_PAY_ACTION, ORDER_CANCEL_ACTION]
	elif order.status == ORDER_STATUS_PAYED_NOT_SHIP:
		return [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
	elif order.status == ORDER_STATUS_PAYED_SHIPED:
		return [ORDER_FINISH_ACTION, ORDER_CANCEL_ACTION]
	elif order.status == ORDER_STATUS_SUCCESSED:
		return [ORDER_CANCEL_ACTION]
	elif order.status == ORDER_STATUS_CANCEL:
		return []


@register.filter(name='get_order_status_transition')
def get_order_status_transition(order):
	return '%s -> %s' % (STATUS2TEXT[order.from_status], STATUS2TEXT[order.to_status])

############################
# 计算可用积分兑换金额
############################
@register.filter(name='usable_money')
def usable_money(usable_integral, count_per_yuan):
	return round(float(usable_integral) / float(count_per_yuan), 2)

@register.filter(name='url_filter')
def url_filter(url):
	return url.replace('&', '%26')

@register.filter(name='round2')
def round2(value):
	return round(value, 2)

import json
@register.filter(name='json_dumps')
def json_dumps(obj):
	return json.dumps(obj)