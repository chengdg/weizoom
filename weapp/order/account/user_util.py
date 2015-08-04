# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import order_settings
from watchdog.utils import watchdog_info

def get_request_freight_user(request):
	#假设经过了freightSessionMiddleware中间件的处理
	return request.freight_user if hasattr(request, 'freight_user') else None

def get_session_freight_user_name():
	return order_settings.FREIGHT_USER_SESSION_KEY

def get_session_is_remove_freight_user_name():
	return order_settings.IS_REMOVE_FREIGHT_USER_SESSION_KEY

def get_freight_user_from_cookie(request):
	return request.COOKIES.get(get_session_freight_user_name())


def get_is_remove_freight_from_cookie(request):
	return request.COOKIES.get(get_session_is_remove_freight_user_name(), False)

def save_session_freight_user(response, user_id):
	sign = '%s' % user_id
	response.set_cookie(get_session_freight_user_name(), sign, max_age=3600*24)
#	watchdog_info(u"freight login success save_session sign: %s, name: %s" % (sign, get_session_freight_user_name()))


def delete_session_freight_user(response):
	response.set_cookie(get_session_is_remove_freight_user_name(), True, max_age=3600*24)


def logout_freight_user(response):
	delete_session_freight_user(response)