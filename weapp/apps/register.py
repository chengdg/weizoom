# -*- coding: utf-8 -*-

__author__ = 'chuter'

from apps.apps_manager import manager

def api(function=None, resource=None, action='GET', mobile=False):
	def _dec(api_view_func):
		items = api_view_func.__module__.split('.')
		app_name = items[-3]
		module = items[-2]

		def warpper(request, *args, **kwargs):
			request.GET._mutable = True
			request.GET.update({"real_app_name": app_name, "real_module": module})
			request.GET._mutable = False
			return api_view_func(request, *args, **kwargs)

		warpper.__doc__ = api_view_func.__doc__
		warpper.__dict__ = api_view_func.__dict__
		warpper.__dict__['resource'] = resource
		warpper.__dict__['action'] = action.upper()

		warpper.__name__ = api_view_func.__name__

		if mobile:
			real_resource = 'mobile_{}'.format(resource)
		else:
			real_resource = resource

		view_module_name = api_view_func.__module__
		manager.register_api_func(
				view_module_name,
				#api_view_func,
				warpper,
				real_resource,
				action
			)

		return warpper

	if function is None:  
		return _dec
	else:
		return _dec(function)


def mobile_api(function=None, resource=None, action='GET'):
	return api(function, resource, action, True)


def view_func(function=None, resource=None, action='GET', mobile=False):
	def _dec(_view_func):
		items = _view_func.__module__.split('.')
		app_name = items[-3]
		module = items[-2]
		def warpper(request, *args, **kwargs):
			request.GET._mutable = True
			request.GET.update({"real_app_name": app_name, "real_module": module})
			request.GET._mutable = False
			return _view_func(request, *args, **kwargs)

		warpper.__doc__ = _view_func.__doc__
		warpper.__dict__ = _view_func.__dict__
		warpper.__dict__['resource'] = resource
		warpper.__dict__['action'] = action.upper()

		warpper.__name__ = _view_func.__name__

		if mobile:
			real_resource = 'mobile_{}'.format(resource)
		else:
			real_resource = resource

		view_module_name = _view_func.__module__
		manager.register_view_func(
				view_module_name,
				#_view_func,
				warpper,
				real_resource,
				action
			)

		return warpper

	if function is None:
		return _dec
	else:
		return _dec(function)


def mobile_view_func(function=None, resource=None, action='GET'):
	return view_func(function, resource, action, True)