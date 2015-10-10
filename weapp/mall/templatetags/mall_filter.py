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
from mall.models import *

register = template.Library()

# order_status2text = {
# 	ORDER_STATUS_NOT: u'待支付',
# 	ORDER_STATUS_CANCEL: u'已取消',
# 	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
# 	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
# 	ORDER_STATUS_PAYED_SHIPED: u'已发货',
# 	ORDER_STATUS_SUCCESSED: u'已完成'
# }
order_status2text = STATUS2TEXT
@register.filter(name='get_order_status_text')
def get_order_status_text(order):
	return order_status2text[order.status]


# order_status2text = {
# 	ORDER_STATUS_NOT: u'待支付',
# 	ORDER_STATUS_CANCEL: u'已取消',
# 	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
# 	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
# 	ORDER_STATUS_PAYED_SHIPED: u'已发货',
# 	ORDER_STATUS_SUCCESSED: u'已完成'
# }
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





@register.filter(name='get_order_status_transition')
def get_order_status_transition(order):
	return '%s -> %s' % (STATUS2TEXT[order.from_status], STATUS2TEXT[order.to_status])

############################
# 计算可用积分兑换金额
############################
@register.filter(name='usable_money')
def usable_money(usable_integral, count_per_yuan):
	try:
		return round(float(usable_integral) / float(count_per_yuan), 2)
	except:
		return 0

@register.filter(name='url_filter')
def url_filter(url):
	return url.replace('&', '%26')

@register.filter(name='round2')
def round2(value):
	return round(value, 2)

@register.filter(name='formate_width')
def formate_width(value):
	return 100/value

@register.filter(name='format_model_to_valid_selector')
def format_model_to_valid_selector(value):
	return value.replace(':', '-')


@register.filter(name="abs")
def absolute(value):
    """Return the absolute value."""
    try:
        return abs(value)
    except (ValueError, TypeError):
        return ""

# @register.filter(name='order_not_ship_count')
# def order_not_ship_count(count, request):
# 	return len(belong_to(request.manager.get_profile().webapp_id).filter(status=ORDER_STATUS_PAYED_NOT_SHIP))

