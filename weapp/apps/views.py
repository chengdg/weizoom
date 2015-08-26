# -*- coding: utf-8 -*-
import os
from weixin2 import export

__author__ = 'liupeiyu chuter'


from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from models import *
from product.models import UserHasProduct
from core.jsonresponse import create_response, JsonResponse
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_alert
from datetime import datetime

from apps_manager import manager
from app_status_response_util import *
from weixin2.export import get_customerized_apps

FIRST_NAV_NAME = 'apps'

def __get_first_nav_url(app_module):
	try:
		return app_module.settings.LEFT_NAVS[0]['navs'][0]['url']
	except:
		print unicode_full_stack().encode('utf-8')
		return None

@login_required
def show_app(request, app_name):
	try:
		app = CustomizedApp.objects.get(name=app_name)
	except:
		raise Http404(u"不存在该定制化APP")

	#检查app的当前状态
	if CustomizedappStatus.INACTIVE == app.status or \
		CustomizedappStatus.UNINSTALLED == app.status:
		return show_inactive_app(request, app)
	elif CustomizedappStatus.STOPEED == app.status or \
		CustomizedappStatus.STOPPING == app.status or \
		CustomizedappStatus.STARTING == app.status:
		return show_stopped_app(request, app)
	elif CustomizedappStatus.UPDATING == app.status:
		return show_updating_app(request, app)
	elif CustomizedappStatus.WITHERROR == app.status:
		#TODO 进行预警
		pass
	else:
		#正常运行
		pass
	
	app_module = manager.get_app_module(app)
	if app_module is None:
		raise Http404(u"不存在该定制化APP")

	first_nav_url = __get_first_nav_url(app_module)
	if first_nav_url is not None:
		return HttpResponseRedirect(first_nav_url)
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': app_module.settings.LEFT_NAVS,
			'app': app
		})
		return render_to_response('apps/apps_list.html', c)

@login_required
def list_apps(request):
	if request.user.is_manager:
		customized_app_infos = CustomizedAppInfo.objects.all().order_by('id')
		template_file = 'apps/apps_list.html'
	else:
		product = UserHasProduct.objects.get(owner=request.user).product
		market_tool_modules = ['markettool:'+item for item in product.market_tool_modules.split(',') if item]
		
		customized_app_infos = []
		customized_app = list(CustomizedApp.objects.filter(Q(owner=request.user) | Q(name__in=market_tool_modules)).order_by('id'))
		# customized_app_infos.extend(list(CustomizedAppInfo.objects.filter(remark_name='markettool'))) #合并market tool
		app_ids = [app.id for app in customized_app]
		id2appInfo = dict([(appInfo.customized_app_id, appInfo) for appInfo in CustomizedAppInfo.objects.filter(customized_app_id__in=app_ids)])
		for app in customized_app:
			app_info = id2appInfo[app.id]
			app_info.app = app
			if app_info.remark_name == 'markettool':
				app_info.type = u'营销工具'
				app_info.home_url = app_info.repository_path
			else:
				app_info.type = u'定制应用'
				app_info.home_url = '/apps/%s/home/' % app_info.app.name
			customized_app_infos.append(app_info)
		template_file = 'apps/user_apps_list.html'

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': None,
		'customized_app_infos': customized_app_infos,
	    'is_super_user': request.user.is_manager
	})
	return render_to_response(template_file, c)


@login_required
def add_app(request):
	all_users = []
	for user in User.objects.all():
		if user.username == 'manager':
			continue
		if user.username == 'admin':
			user.username = u'全部'
		all_users.append(user)
	if request.POST:
		app_name = request.POST.get('app_name','')
		app_display_name = request.POST.get('app_display_name', '')
		if not app_display_name:
			app_display_name = app_name
		owner_id = int(request.POST.get('user_id',0))
		customized_app = CustomizedApp.objects.create(
			owner_id=owner_id,
			name=app_name,
			display_name=app_display_name,
			updated_time=datetime.now(),
			status=CustomizedappStatus.INACTIVE
		)
		CustomizedAppInfo.objects.create(
			app_name=app_display_name,
			owner_id=owner_id,
			customized_app = customized_app,
			remark_name = request.POST.get('remark_name',''),
			principal = request.POST.get('principal',''),
			repository_path = request.POST.get('repository_path',''),
			repository_username = request.POST.get('repository_username',''),
			repository_passwd = request.POST.get('repository_passwd','')
		)

		return HttpResponseRedirect('/apps/')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': None,
		    'all_users': all_users
		})
		return render_to_response('apps/edit_app.html', c)


@login_required
def update_app(request, customized_app_info_id):
	all_users = []
	for user in User.objects.all():
		if user.username == 'manager':
			continue
		if user.username == 'admin':
			user.username = u'全部'
		all_users.append(user)

	try:
		customized_app_info = CustomizedAppInfo.objects.get(id=customized_app_info_id)
	except:
		notify_msg = u"定制化app修改时异常, customized_app_info_id={}, cause:\n{}".format(customized_app_info_id, unicode_full_stack())
		watchdog_alert(notify_msg)
		raise Http404('不存在该app')

	if request.POST:
		app_name = request.POST.get('app_name','')
		owner_id = int(request.POST.get('user_id',0))

		customized_app = customized_app_info.customized_app
		if owner_id == 0:
			owner_id = customized_app.owner_id
		customized_app.owner_id=owner_id
		customized_app.name=app_name
		customized_app.updated_time=datetime.now()
		customized_app.status=CustomizedappStatus.INACTIVE
		customized_app.save()

		customized_app_info.app_name=app_name
		customized_app_info.owner_id=owner_id
		customized_app_info.customized_app = customized_app
		customized_app_info.remark_name = request.POST.get('remark_name','')
		customized_app_info.principal = request.POST.get('principal','')
		customized_app_info.repository_path = request.POST.get('repository_path','')
		customized_app_info.repository_username = request.POST.get('repository_username','')
		customized_app_info.repository_passwd = request.POST.get('repository_passwd','')
		customized_app_info.save()

		return HttpResponseRedirect('/apps/')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': None,
			'all_users': all_users,
		    'customized_app_info': customized_app_info,
		    'is_super_user': request.user.is_manager
		})
		return render_to_response('apps/edit_app.html', c)

def list_new_apps(request):
	if request.user.is_manager:
		customized_app_infos = CustomizedAppInfo.objects.all().order_by('id')
		template_file = 'apps/apps_list.html'
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': None,
			'customized_app_infos': customized_app_infos,
		    'is_super_user': request.user.is_manager
		})
		return render_to_response(template_file, c)
	else:
		second_navs = export.get_customerized_apps(request)
		if second_navs:
			first_nav = second_navs[0]
			url = first_nav['navs'][0]['url']
			url_info = url.split('/')
			first_nav_name = url_info[1]
			app = url_info[2]
			second_nav_name = url_info[3]
			import imp
			fp, pathname, desc = imp.find_module('models', ['./apps/customerized_apps/'+app,])

			has_data = imp.load_module('models', fp, pathname, desc).event.objects.count()

			c = RequestContext(request, {
				'first_nav_name': first_nav_name,
				'second_navs': second_navs,
				'second_nav_name': second_nav_name,
				'has_data': has_data
			})

			return render_to_response(app+'/templates/editor/'+second_nav_name+'.html', c)
