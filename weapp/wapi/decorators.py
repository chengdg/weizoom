#coding: utf8
"""
WAPI检查是否有权限的decorator

"""

from functools import wraps
from django.utils.decorators import available_attrs

from weapp import settings
from core.jsonresponse import create_response

def failure_response(msg='No access granted!'):
	response = create_response(400)
	response.errMsg = msg
	return response.get_response()


def user_passes_test(test_func, required_params=None):
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to the log-in page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""

	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			#access_token = request.REQUEST.get('access_token')
			#if access_token is None:
			#	return failure_response()
			(is_valid, msg) = test_func(request, required_params)
			if is_valid:
				try:
					response = view_func(request, *args, **kwargs)
					return response
				except Exception as e:
					# TODO: 函数异常
					msg = "Exception: {}".format(e)
			return failure_response(msg=msg)
		return _wrapped_view
	return decorator

# TODO: 需要增加检查参数的decorator

def check_valid(request, required_params):
	# 检查access-token
	access_token = request.REQUEST.get('access_token')
	if access_token is None:
		return (False, "The access-token is required.")

	# 检查参数
	if required_params:
		for param in required_params:
			if not param in request.REQUEST:
				return (False, "`%s` is required." % param)

	return (True, None)


	
# def param_required(params=None, function=None):
# 	"""
# 	Decorator for views that checks that the user is using the inner secret key, 
# 	returning the failure response when the checking is not passed.
# 	"""
# 	actual_decorator = user_passes_test(
# 		#lambda access_key: access_key == settings.WAPI_SECRET_ACCESS_TOKEN,
# 		check_valid, params
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator

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
