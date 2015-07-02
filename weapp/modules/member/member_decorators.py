# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect
from webapp.models import Workspace
from models import *

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

	#	elif 
				
# WEBAPP_USER_CENTER_URI = 'module=user_center&model=user_info&action=get&workspace_id=user_center'
# def binding_required(function=None, ignore_wechat_login=True):
# 	def _dec(view_func):
# 		def _view(request, *args, **kwargs):
# 			ignore_wechat_login = _view.ignore_wechat_login
# 			if ignore_wechat_login is True:
# 				ignore_wechat_login = False if request.GET.get('wechat_login', '0') == '1' else True

# 				if hasattr(request, 'member') and request.member and ignore_wechat_login is False:
# 					MemberInfo.objects.filter(member_id=request.member.id).update(is_passed=True)

# 			if ignore_wechat_login is False:
# 				redirect_to = ''
# 			else:
# 				if request.member:
# 					member_info = MemberInfo.get_member_info(request.member.id)
# 					if WEBAPP_USER_CENTER_URI in request.get_full_path():
# 						if member_info.is_passed or member_info.is_binded:
# 							redirect_to = ''
# 						else:
# 							redirect_to = "/workbench/jqm/preview/?module=user_center&model=binding_page&action=get&webapp_owner_id={}".format(
# 									request.user_profile.user_id
# 								)
# 					else:
# 						redirect_to = ''
# 				else:
# 					redirect_to = "/workbench/jqm/preview/?module=user_center&model=binding_page&action=get&webapp_owner_id={}".format(
# 									request.user_profile.user_id
# 								)

# 			if redirect_to:
# 				return HttpResponseRedirect(redirect_to) 
# 			else:
# 				return view_func(request, *args, **kwargs)

# 		_view.__doc__ = view_func.__doc__
# 		_view.__dict__ = view_func.__dict__
# 		_view.__dict__['ignore_wechat_login'] = ignore_wechat_login

# 		return _view

# 	if function is None:
# 		return _dec
# 	else:
# 		return _dec(function)