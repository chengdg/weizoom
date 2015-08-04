# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
from django.conf import settings

from models import *

def get_login_tmpl(request, default_login_tmpl='account/login.html'):
	#首先判断是不是访问用户定制化的首页
	is_request_for_custermized_page = False
	request_host = request.META['HTTP_HOST']

	if request_host != settings.DOMAIN:
		#如果请求的域名和系统设定的自身域名不同，则认为是访问定制化首页
		is_request_for_custermized_page = True

	custermized_login_tmpl = None
	if is_request_for_custermized_page:
		custermized_login_tmpl = __get_customized_login_tmpl(request_host)

	login_tmpl = default_login_tmpl
	if custermized_login_tmpl is not None:
		login_tmpl = custermized_login_tmpl
	
	return login_tmpl

def __get_customized_login_tmpl(request_host):
	target_login_file_root_dir_name = request_host.replace('.', '_')
	target_login_file_root = os.path.join(settings.CUSTOMERIZED_TEMPLATES_DIR, target_login_file_root_dir_name)
	target_login_file_path = os.path.join(target_login_file_root, 'login.html')

	if os.path.exists(target_login_file_path):
		return "{}/login.html".format(target_login_file_root_dir_name)
	else:
		return None

def is_can_login(user):
	if is_sub_user(user):
		if is_actived_sub_user(user):
			return True
		else:
			return False
	else:
		True

def is_sub_user(user):
	 return UserHasSubUser.objects.filter(sub_user=user).count() > 0	

def is_actived_sub_user(user):
	return UserHasSubUser.objects.filter(sub_user=user, is_active=True).count() > 0

def get_father_user(user):
	return UserHasSubUser.objects.filter(sub_user=user, is_active=True)[0].user

def get_current_user_and_request(user, request):
	if is_sub_user(user):
		if is_actived_sub_user(user):
			request.sub_user = user
			user = get_father_user(user)
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			return user, request
		else:
			return None, request
	else:
		request.sub_user = None
		return user, request