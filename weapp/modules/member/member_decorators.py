# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect
from webapp.models import Workspace

def member_required(function=None, redirect_to=None, is_format_webapp_id_in_url=True):
	def _dec(view_func):
		def _view(request, *args, **kwargs):
			if not hasattr(request, 'member') or request.member is None:
				redirect_to = _view.redirect_to

				if redirect_to is None:
					#redirect_to = "http://{}/".format(request.META['HTTP_HOST'])
					project_id = 0
					for workspace in Workspace.objects.filter(owner_id=request.webapp_owner_id):
						if workspace.inner_name == 'home_page':
							project_id = workspace.template_project_id
					redirect_to = "/workbench/jqm/preview/?project_id=%d" % project_id

					work_space_id = request.REQUEST.get('workspace_id', '')
					redirect_to = "{}&workspace_id={}&webapp_owner_id={}".format(
							redirect_to,
							work_space_id,
							request.user_profile.user_id
						)

				if _view.is_format_webapp_id_in_url:
					redirect_to = redirect_to.format(request.user_profile.webapp_id)

				return HttpResponseRedirect(redirect_to) 
			# else:
			# TODO 处理跳转？？
			return view_func(request, *args, **kwargs)

		_view.__doc__ = view_func.__doc__
		_view.__dict__ = view_func.__dict__
		_view.__dict__['redirect_to'] = redirect_to
		_view.__dict__['is_format_webapp_id_in_url'] = is_format_webapp_id_in_url

		_view.__name__ = view_func.__name__

		return _view

	if function is None:
		return _dec
	else:
		return _dec(function)