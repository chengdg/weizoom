# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from user_util import *
from models import *


#===============================================================================
# FreightSessionMiddleware : 获取当前请求的用户信息
# view中的代码可直接通过request.operation_user获取当前请求的用户
#===============================================================================
class FreightSessionMiddleware(object):
	NEED_REMOVE_FREIGHT_USER_SESSION_FLAG = 'need_remove_freight_user_session'
	def process_request(self, request):
		request.freight_user = get_request_freight_user(request)
		if request.freight_user is None:
			user_id = get_freight_user_from_cookie(request)
			try:
				user = FreightUser.objects.get(id=user_id)
			except:
				request.META[self.NEED_REMOVE_FREIGHT_USER_SESSION_FLAG] = True
				user = None
			request.freight_user = user

		return None

	def process_response(self, request, response):
		sign = get_freight_user_from_cookie(request)
		is_remove_freight_user = get_is_remove_freight_from_cookie(request)

		if is_remove_freight_user:
			response.delete_cookie(get_session_freight_user_name())
			response.delete_cookie(get_session_is_remove_freight_user_name())
#			print '-----------------delete_cookie-----------'
		elif sign:
#			print '-----------------set_cookie-----------'
			response.set_cookie(get_session_freight_user_name(), sign, max_age=60*60*24*365)
		return response
