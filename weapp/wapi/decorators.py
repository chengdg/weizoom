#coding: utf8
"""
WAPI检查是否有权限的decorator

"""

from functools import wraps
from django.utils.decorators import available_attrs

from weapp import settings


from core.jsonresponse import create_response
from wapi.models import OAuthToken
import datetime as dt


def failure_response(msg='No access granted!'):
	response = create_response(400)
	response.errMsg = msg
	return response.get_response()


def check_access_token(required_params=None):
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to the log-in page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""

	def decorator(view_func):
		def _wrapped_view(request, *args, **kwargs):
			access_token = request.REQUEST.get('access_token')
			if access_token is None:
				return failure_response(msg="The access-token is required.")
			try:
				# 由token确认用户信息
				relations = OAuthToken.objects.filter(token=access_token, expire_time__gt=dt.datetime.now())
				if relations.count()>0:
					#request.user = relations[0].user
					request.REQUEST['user'] = relations[0].user
					response = view_func(request, *args, **kwargs)
					return response
				msg = "Invalid access token."
			except Exception as e:
				# TODO: 函数异常
				msg = "Exception: {}".format(e)
			return failure_response(msg=msg)
		return _wrapped_view
	return decorator


def auth_required(function=None):
	"""
	检查是否有access_token
	"""
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
