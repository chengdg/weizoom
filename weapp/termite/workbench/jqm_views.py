# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
try:
    import Image
except:
    from PIL import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from watchdog.utils import watchdog_alert, watchdog_emergency, watchdog_error, watchdog_info
from webapp.models import Workspace
from weixin.user.models import set_share_img
from models import *
from termite.core.jsonresponse import create_response, JsonResponse
from termite.core import paginator
import pagerender
import apps
import jqm_api_views as api_views
from termite import pagestore as pagestore_manager
from account.models import UserProfile
from mall.models import PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY


def show_design_page(request):
	"""
	显示设计页面
	"""
	project_id = request.GET['project_id']
	page_id = request.GET.get('page_id', None)
	project = Project.objects.get(id=project_id)
	
	if not page_id:
		c = RequestContext(request, {
			'project_id': project_id
		})
	
		return render_to_response('workbench/wait_design_page.html', c)
	else:
		html = api_views.create_page(request, return_html_snippet=True)

		if request.project.source_project_id != 0:
			project_css = 'project_%d.css' % request.project.source_project_id
		else:
			project_css = 'project_%s.css' % project_id

		c = RequestContext(request, {
			'project_id': project_id,
			'project_css': project_css,
			'page_html_content': html
		})

		if project.inner_name == 'dress':
			return render_to_response('workbench/jqm_design_page.html', c)
		elif 'wepage_' in project.inner_name:
			return render_to_response('workbench/wepage_design_page.html', c)
		else:
			return render_to_response('workbench/new_jqm_design_page.html', c)


#===============================================================================
# show_alipay_callback_page : 处理支付宝的回调行为
#===============================================================================
def show_alipay_callback_page(request, module, model, action, webapp_owner_id, pay_interface_related_config_id):
	request.user_profile = UserProfile.objects.get(user_id=webapp_owner_id)

	new_get = dict()
	for key, value in request.GET.items():
		new_get[key] = value
	new_get['module'] = module
	new_get['model'] = model
	new_get['action'] = action
	new_get['related_config_id'] = pay_interface_related_config_id
	new_get['pay_interface_type'] = PAY_INTERFACE_ALIPAY
	request.GET = new_get
	request.page_type = 'webapp'
	return show_preview_page(request)


#===============================================================================
# show_tenpay_callback_page : 处理财付通的回调行为
#===============================================================================
def show_tenpay_callback_page(request, module, model, action, webapp_owner_id, pay_interface_related_config_id):
	request.user_profile = UserProfile.objects.get(user_id=webapp_owner_id)

	new_get = dict()
	for key, value in request.GET.items():
		new_get[key] = value
	new_get['module'] = module
	new_get['model'] = model
	new_get['action'] = action
	new_get['related_config_id'] = pay_interface_related_config_id
	new_get['pay_interface_type'] = PAY_INTERFACE_TENPAY
	request.GET = new_get

	return show_preview_page(request)


#===============================================================================
# show_wxpay_callback_page : 处理微信支付的回调行为
#===============================================================================
def show_wxpay_callback_page(request, module, model, action, webapp_owner_id, pay_interface_related_config_id):
	request.user_profile = UserProfile.objects.get(user_id=webapp_owner_id)

	new_get = dict()
	for key, value in request.GET.items():
		new_get[key] = value
	new_get['module'] = module
	new_get['model'] = model
	new_get['action'] = action
	new_get['related_config_id'] = pay_interface_related_config_id
	new_get['pay_interface_type'] = PAY_INTERFACE_WEIXIN_PAY
	request.GET = new_get
	request.page_type = 'webapp'
	return show_preview_page(request)


#===============================================================================
# show_preview_page : 显示预览的移动页面
#===============================================================================
def show_preview_page(request):
	#确定使用的模板
	#workspace = Workspace.objects.get(owner_id=request.user_profile.user_id, inner_name='home_page')
	template_name = request.user_profile.backend_template_name

	#设置分享图片为默认头像
	set_share_img(request)
	
	if not template_name:
		template_name = 'default'
	request.template_name = template_name
	if request.project:
		request.homepage_template_name = request.project.inner_name
	else:
		request.homepage_template_name = request.user_profile.homepage_template_name
	if request.page_type == 'home_page':
		html = api_views.create_page(request, return_html_snippet=True)

		#TODO: 去除显式的16
		if request.webapp_owner_id == 16:
			c = RequestContext(request, {
				'page_title': u'微众商城',
				'page_html_content': html,
				'hide_non_member_cover': True #非会员也可使用该页面
			})
		else:
			c = RequestContext(request, {
				'page_title': u'微站首页',
				'page_html_content': html,
				'hide_non_member_cover': True #非会员也可使用该页面
			})

		return render_to_response('workbench/new_jqm_preview_page.html', c)
	elif request.page_type == 'webapp':
		module_name = request.GET['module']
		model = request.GET['model']
		action = request.GET.get('action', 'get')

		if 'ignore_template' in request.REQUEST:
			module_path = 'webapp.modules.%s.webapp_no_template.views' % module_name
		else:
			module_path = 'webapp.modules.%s.mobile_views' % module_name
		
		module = __import__(module_path, {}, {}, ['*',])
		function_name = '%s_%s' % (action, model)
		function = getattr(module, function_name)

		if settings.IN_DEVELOP_MODE:
			print 'call webapp view function "%s" in %s' % (function_name, module.__file__)

		return function(request)
	elif request.page_type == 'market_tool':
		module_name = request.GET['module'].split(':')[1]
		model = request.GET['model']
		action = request.GET.get('action', 'get')

		module_path = 'market_tools.tools.%s.mobile_views' % module_name
		module = __import__(module_path, {}, {}, ['*',])
		function_name = '%s_%s' % (action, model)
		function = getattr(module, function_name)

		if settings.IN_DEVELOP_MODE:
			print 'call market_tool mobile view function "%s" in %s' % (function_name, module.__file__)

		return function(request)
	elif request.page_type == 'apps':
		return apps.get_mobile_response(request)
	else:
		pass		


#===============================================================================
# show_production_page : 显示实际页面
#===============================================================================
def show_production_page(request):
	1/0
	project_id = request.GET['project_id']
	
	html = api_views.create_page(request, return_html_snippet=True)
	c = RequestContext(request, {
		'project_id': project_id,
		'page_html_content': html
	})
	return render_to_response('workbench/jqm_preview_page.html', c)
