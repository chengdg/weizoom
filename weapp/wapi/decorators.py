#coding: utf8
"""
WAPI检查是否有权限的decorator

"""

#from functools import wraps
#from django.utils.decorators import available_attrs

from weapp import settings
from django.contrib.auth.models import User

#from core.jsonresponse import create_response
from wapi.models import OAuthToken
import datetime as dt
import logging

"""
def failure_response(msg='No access granted!'):
	response = create_response(400)
	response.errMsg = msg
	return response.get_response()
"""

def check_access_token():
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to the log-in page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""

	def decorator(view_func):
		def _wrapped_view(request, *args, **kwargs):
			access_token = request.get('access_token')
			if settings.WAPI_ACCESS_TOKEN_REQUIRED and access_token is None:
				return {
					'message': "The access-token is required."
				}
			try:
				# 由token确认用户信息
				view_args = {}
				for key, value in request.items():
					view_args[key] = value
				if settings.MODE == 'develop' and not settings.WAPI_ACCESS_TOKEN_REQUIRED:
					# 调试用
					view_args['user'] = User.objects.get(username='bill')
					response = view_func(view_args, *args, **kwargs)
					return response
				else:
					relations = OAuthToken.objects.filter(token=access_token, expire_time__gt=dt.datetime.now())
					if relations.count()>0:
						view_args['user'] = relations[0].user
						response = view_func(view_args, *args, **kwargs)
						return response
					else:
						msg = "access_token is required"
				msg = "Invalid access token."
			except Exception as e:
				# TODO: 函数异常
				msg = "Exception: {}".format(e)
			return {
				'message': msg
			}
		return _wrapped_view
	return decorator


def auth_required(function=None):
	"""
	检查是否有access_token
	"""
	logging.info("function: {}".format(function))
	actual_decorator = check_access_token()
	if function:
		return actual_decorator(function)
	return actual_decorator



class ApiParamaterError(Exception):
	pass


def param_required(params=None):
	def wrapper(function):
		def inner(data):
			for param in params:
				if not param in data:
					raise ApiParamaterError('no parameter(%s)' % param)
			return function(data)

		return inner 

	return wrapper
