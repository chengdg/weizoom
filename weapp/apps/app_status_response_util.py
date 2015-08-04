# -*- coding: utf-8 -*-

__author__ = 'chuter'


from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response

#TODO? 重新设计页面，增加针对webapp的页面设计
def show_inactive_app(request, app):
	return show_app_status(request, app, u'已经下线')

def show_stopped_app(request, app):
	return show_app_status(request, app, u'已经停止')

def show_updating_app(request, app):
	return show_app_status(request, app, u'正在更新')	

def show_app_status(request, app, status_info):
	c = RequestContext(request, {
		'status' : status_info,
		'msg' : '显示具体提示信息'
	})
	return render_to_response('apps/app_status.html', c)

