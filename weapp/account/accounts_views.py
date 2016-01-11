# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import random
import json
try:
    import Image
except:
    from PIL import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from models import *
from weixin.user.models import WeixinMpUser
from core.jsonresponse import create_response, JsonResponse
from webapp.models import Workspace

FIRST_NAV_NAME = 'account'

#===============================================================================
# list_accounts : 显示创建的账号集合
#===============================================================================
@login_required
def list_accounts(request):
	profiles = UserProfile.objects.filter(manager_id=request.user.id)
	user_ids = [profile.user_id for profile in profiles]
	created_users = [user for user in User.objects.filter(id__in=user_ids) if user.id != request.user.id]

	created_user_ids = [user.id for user in created_users]
	user2moduleinfo = {}
	for workspace in Workspace.objects.filter(owner_id__in=created_user_ids):
		moduleinfo = user2moduleinfo.get(workspace.owner_id, None)
		if not moduleinfo:
			moduleinfo = {'ids':[], 'names': []}
			user2moduleinfo[workspace.owner_id] = moduleinfo
		moduleinfo['ids'].append(workspace.source_workspace_id)
		moduleinfo['names'].append(workspace.name)

	for created_user in created_users:
		moduleinfo = user2moduleinfo.get(created_user.id, None)
		if moduleinfo:
			created_user.installed_modules = ', '.join(moduleinfo['names'])
			created_user.installed_module_ids = json.dumps(moduleinfo['ids'])
		else:
			created_user.installed_modules = ''
			created_user.installed_module_ids = '[]'

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'created_users': created_users
	})
	return render_to_response('account/created_accounts.html', c)


#===============================================================================
# delete_account : 删除创建的账号
#===============================================================================
@login_required
def delete_account(request):
	user = User.objects.get(id=request.GET['user_id'])
	delete_system_user(user)
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
