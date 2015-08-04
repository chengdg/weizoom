#coding: utf8
"""
WAPI检查是否有权限的decorator

"""

from functools import wraps
from django.utils.decorators import available_attrs

from weapp import settings
from core.jsonresponse import create_response

def failure_response():
	response = create_response(400)
	response.errMsg = 'No access granted!'
	return response.get_response()


def user_passes_test(test_func):
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to the log-in page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""

	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			access_token = request.REQUEST.get('access_token')
			if access_token is None:
				return failure_response()

			if test_func(access_token):
				return view_func(request, *args, **kwargs)
			return failure_response()
		return _wrapped_view
	return decorator

# TODO: 需要增加检查参数的decorator
	
def wapi_access_required(function=None):
	"""
	Decorator for views that checks that the user is using the inner secret key, 
	returning the failure response when the checking is not passed.
	"""
	actual_decorator = user_passes_test(
		lambda access_key: access_key == settings.WAPI_SECRET_ACCESS_TOKEN,
	)
	if function:
		return actual_decorator(function)
	return actual_decorator
