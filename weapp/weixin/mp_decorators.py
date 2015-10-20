# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.http import HttpResponseRedirect

def mp_required(function=None, redirect_to=None):
	def _dec(view_func):
		def _view(request, *args, **kwargs):
			if hasattr(request, 'user') and request.user:
				redirect_to = _view.redirect_to

				# user_profile = request.user.get_profile()
				user_profile = request.manager.get_profile()
				if user_profile and user_profile.is_mp_registered is False:
					redirect_to= '/new_weixin/mp_user/'
				# if redirect_to is None:
				# 	#redirect_to = "http://{}/".format(request.META['HTTP_HOST'])
				# 	project_id = 0
				# 	for workspace in Workspace.objects.filter(owner_id=request.webapp_owner_id):
				# 		if workspace.inner_name == 'home_page':
				# 			project_id = workspace.template_project_id
				# 	redirect_to = "/workbench/jqm/preview/?project_id=%d" % project_id

				# 	work_space_id = request.REQUEST.get('workspace_id', '')
				# 	redirect_to = "{}&workspace_id={}&webapp_owner_id={}".format(
				# 			redirect_to,
				# 			work_space_id,
				# 			request.user_profile.user_id
				# 		)

				# if _view.is_format_webapp_id_in_url:
				# 	redirect_to = redirect_to.format(request.user_profile.webapp_id)

					return HttpResponseRedirect(redirect_to) 
			# else:
			# TODO 处理跳转？？
			return view_func(request, *args, **kwargs)

		_view.__doc__ = view_func.__doc__
		_view.__dict__ = view_func.__dict__
		_view.__dict__['redirect_to'] = redirect_to
		#

		_view.__name__ = view_func.__name__

		return _view

	if function is None:
		return _dec
	else:
		return _dec(function)