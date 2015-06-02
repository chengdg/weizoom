# -*- coding: utf-8 -*-

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response

from models import *
from user_util import save_session_freight_user, logout_freight_user

def login(request):
	username = ''
	password = ''
	msg = ''
	if request.POST:
		username = request.POST.get('username','').strip()
		password = request.POST.get('password','').strip()
		data = FreightUser(username=username, password=password).is_login_success()
		if data['code'] == 'success':
			response = HttpResponseRedirect('/ft/')
			save_session_freight_user(response, data['user_id'])
			return response
		else:
			msg = data['msg']
	else:
		FreightUser().init_user_info()

	c = RequestContext(request, {
		"username": username,
	    "password": password,
	    'msg': msg
	})
	return render_to_response('order/login.html', c)


def logout(request):
	response = HttpResponseRedirect('/ft/account/login/')
	logout_freight_user(response)
	return response