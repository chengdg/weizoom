# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from watchdog.utils import watchdog_info


CLOUD_USER_SESSION_KEY = 'clouduid'

def get_request_cloud_user(request):
	#假设经过了CloudSessionMiddleware中间件的处理
	return request.cloud_user if hasattr(request, 'cloud_user') else None


def get_session_cloud_user_name():
	return CLOUD_USER_SESSION_KEY


def get_cloud_user_from_cookie(request):
	return request.COOKIES.get(get_session_cloud_user_name())


def save_session_cloud_user(response, user_id):
	sign = '%s' % user_id
	response.set_cookie(get_session_cloud_user_name(), sign, max_age=3600*24*24*24)
#	watchdog_info(u"freight login success save_session sign: %s, name: %s" % (sign, get_session_cloud_user_name()))


def delete_session_cloud_user(response):
	response.delete_cookie(get_session_cloud_user_name())


def logout_cloud_user(response):
	delete_session_cloud_user(response)

