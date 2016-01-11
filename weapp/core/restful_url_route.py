# -*- coding: utf-8 -*-

__author__ = 'robert'

APP2URL = {}

def api(function=None, app=None, resource=None, action='GET', mobile=False):
	def _dec(api_view_func):
		def wrapper(request, *args, **kwargs):
			# request.GET._mutable = True
			# request.GET.update({"real_app_name": app_name, "real_module": module})
			# request.GET._mutable = False
			return api_view_func(request, *args, **kwargs)

		wrapper.__doc__ = api_view_func.__doc__
		wrapper.__dict__ = api_view_func.__dict__
		wrapper.__dict__['resource'] = resource
		wrapper.__dict__['action'] = action.upper()

		wrapper.__name__ = api_view_func.__name__

		if mobile:
			real_resource = 'mobile_{}'.format(resource)
		else:
			real_resource = resource

		view_module_name = api_view_func.__module__
		url = 'api/%s/%s/' % (resource, action)
		APP2URL.setdefault(app, {})[url] = api_view_func

		return wrapper

	if function is None:  
		return _dec
	else:
		return _dec(function)


def mobile_api(function=None, resource=None, action='GET'):
	return api(function, resource, action, True)


def view(function=None, app=None, resource=None, action='GET', mobile=False):
	def _dec(_view_func):
		def wrapper(request, *args, **kwargs):
			#request.GET._mutable = True
			#request.GET.update({"real_app_name": app_name, "real_module": module})
			#request.GET._mutable = False
			return _view_func(request, *args, **kwargs)

		wrapper.__doc__ = _view_func.__doc__
		wrapper.__dict__ = _view_func.__dict__
		wrapper.__dict__['resource'] = resource
		wrapper.__dict__['action'] = action.upper()

		wrapper.__name__ = _view_func.__name__

		if mobile:
			real_resource = 'mobile_{}'.format(resource)
		else:
			real_resource = resource

		view_module_name = _view_func.__module__
		url = '%s/%s/' % (resource, action)
		APP2URL.setdefault(app, {})[url] = _view_func

		return wrapper

	if function is None:
		return _dec
	else:
		return _dec(function)


def mobile_view_func(function=None, resource=None, action='GET'):
	return view_func(function, resource, action, True)