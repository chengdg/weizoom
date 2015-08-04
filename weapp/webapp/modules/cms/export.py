# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from webapp import views as webapp_views

from models import *

NAV = {
	'section': u'文章管理',
	'navs': [
		{
			'name': 'cms-category',
			'title': u'文章分类',
			'url': '/cms/editor/categories/',
		},
		{
			'name': 'cms-article',
			'title': u'文章列表',
			'url': '/cms/editor/articles/',
		},
		{
			'name': 'cms-special-article',
			'title': u'特殊页面',
			'url': '/cms/editor/special_articles/',
		}
	]
}


PAGES = [
	{
		'name': Category._meta.verbose_name,
		'value': Category._meta.module_name
	},
	{
		'name': Article._meta.verbose_name,
		'value': Article._meta.module_name
	}
]

########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.user.username == 'manager':
		second_navs = []
		second_navs.append(NAV)
		second_navs.append({
			'section': u'项目',
			'navs': [{
				'name': u'项目管理',
				'url': '/webapp/',
				'title': u'项目管理'
			}]
		})
	else:
		second_navs = webapp_views.get_modules_page_second_navs(request)

	return second_navs


########################################################################
# get_link_targets: 获得cms中可连接的数据对象
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=cms&webapp_owner_id=%d' % request.workspace.owner_id
	has_data_category_filter = (request.GET.get('data_category_filter', None) != None)

	#获得category集合
	if has_data_category_filter:
		categories = []
	else:
		categories = [{
			'text': u'全部', 
			'value': './?module=cms&model=category&rid=0&%s' % workspace_template_info
		}]
	for category in Category.objects.filter(owner=request.user):
		categories.append({
			'text': category.name, 
			'value': './?module=cms&model=category&rid=%d&%s' % (category.id, workspace_template_info),
			'meta': {
				'id': category.id,
				'name': category.name,
				'type': 'article_category'
			}
		})

	if not has_data_category_filter:
		#获得article集合
		articles = []
		for article in Article.objects.filter(owner=request.user).order_by('-display_index'):
			articles.append({
				'text': article.title, 
				'value': './?module=cms&model=article&article_id=%d&%s' % (article.id, workspace_template_info)
			})

		#获得page集合
		pages = [
			{'text': u'文章列表页', 'value': './?module=cms&model=category&rid=0&%s' % workspace_template_info}
		]

		if request.user.is_manager:
			pages.extend([
				{'text': u'编辑链接提示', 'value': 'javascript:W.alertEditTemplateLinkTarget();'},
				{'text': u'【静态链接】首页', 'value': 'static_nav:homepage'},
				{'text': u'【静态链接】商品列表', 'value': 'static_nav:product_list'},
				{'text': u'【静态链接】文章列表', 'value': 'static_nav:article_list'},
				{'text': u'【静态链接】个人中心', 'value': 'static_nav:user_center'},
				{'text': u'【静态链接】购物车', 'value': 'static_nav:shopping_cart'},
				{'text': u'【静态链接】订单列表', 'value': 'static_nav:order_list'},
			])

		if settings.MODE == 'develop':
			pages.append({
				'text': u'【Demo页】微站首页',
				'value': './?module=cms&model=demo_home_page&action=get"'
			})

		response.data = [
			{
				'name': u'文章分类',
				'data': categories
			}, {
				'name': u'文章',
				'data': articles
			}, {
				'name': u'页面',
				'data': pages
			}
		]
	else:
		response.data = [
			{
				'name': u'文章分类',
				'data': categories
			}
		]
	return response.get_response()