# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from django.http import HttpResponseRedirect

def cloud_housekeeper_required(function=None):
	def _dec(view_func):
		def _view(request, *args, **kwargs):
			if not hasattr(request, 'cloud_user') or request.cloud_user is None:
				redirect_to = _view.redirect_to.format(request.path)

				if redirect_to is None:
					redirect_to = "http://{}/cloud_housekeeper/home/".format(request.META['HTTP_HOST'])

				return HttpResponseRedirect(redirect_to)
			else:
				return view_func(request, *args, **kwargs)

		_view.__doc__ = view_func.__doc__
		_view.__dict__ = view_func.__dict__
		_view.__dict__['redirect_to'] = '/cloud_housekeeper/login/?next={}'

		_view.__name__ = view_func.__name__

		return _view

	if function is None:
		return _dec
	else:
		return _dec(function)