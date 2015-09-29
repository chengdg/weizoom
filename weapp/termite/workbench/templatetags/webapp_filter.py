# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date
import json

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from workbench.models import *

from datetime import datetime
from termite import pagestore as pagestore_manager
from webapp.models import Project, GlobalNavbar
from account.models import UserProfile

register = template.Library()


@register.filter(name='get_global_navs')
def get_global_navs(request):
	try:
		global_navbar = GlobalNavbar.objects.get(owner_id=request.webapp_owner_id)
	except:
		global_navbar = GlobalNavbar()
		global_navbar.is_enable = False

	if global_navbar.is_enable:
		data = json.loads(global_navbar.content)
		navs = []
		data.sort(lambda x,y: cmp(x['index'], y['index']))
		for menu in data:
			answer = menu['answer']
			if len(menu['items']) > 0:
				#有item的menu
				nav = {
					'id': menu['id'],
					'text': menu['name'],
					'target': 'javascript:void(0);',
					'type': 'js',
					'menutype': 'menu-container',
					'items': []
				}
				menuitems = menu['items']
				menuitems.sort(lambda x,y: cmp(y['index'], x['index']))
				for menuitem in menu['items']:
					target = menuitem['answer']['data']
					if target.startswith('javascript:') or target.startswith('http:'):
						url_type = 'js'
					else:
						url_type = 'url'
					nav['items'].append({
						'id': menuitem['id'],
						'text': menuitem['name'],
						'target': menuitem['answer']['data'],
						'type': url_type,
						'menutype': 'menuitem'
					})

				navs.append(nav)
			else:
				#无item的menu
				target = menu['answer']['data']
				if target.startswith('javascript:') or target.startswith('http:'):
					url_type = 'js'
				else:
					url_type = 'url'
				navs.append({
					'id': menu['id'],
					'text': menu['name'],
					'target': menu['answer']['data'],
					'menutype': 'menu',
					'type': url_type
				})
				
		return {
			"is_standard_global_nav": True,
			"navs": navs
		}
	else:
		pagestore = pagestore_manager.get_pagestore(request)

		#获得home_page workspace中的模板project
		webapp_owner_id = request.webapp_owner_id
		workspace = Workspace.objects.get(owner_id=webapp_owner_id, inner_name='home_page')
		template_project_name = workspace.template_name
		template_projects = Project.objects.filter(owner_id=webapp_owner_id, workspace=workspace, inner_name=template_project_name)

		if template_projects.count() == 0:
			return {
				"is_standard_global_nav": False,
				"navs": []
			}

		template_project = template_projects[0]
		#在首页中寻找导航信息
		navs = []
		#获得首页
		pages = list(pagestore.get_pages(str(template_project.id)))
		if len(pages) > 0:
			pages.sort(lambda x,y: cmp(x['display_index'], y['display_index']))
			index_page = pages[0]

			for component in index_page['component']['components']:
				if 'jqm.nav_icon_grid' == component['type']:
					for nav_button_component in component['components']:
						model = nav_button_component['model']
						text = model['text']
						target = model['target']

						#added by chuter
						if target is None or len(target) == 0:
							continue

						target = json.loads(target)['data']
						if target.startswith('javascript:') or target.startswith('http:') or target.startswith('static_nav:'):
							url_type = 'js'
						else:
							url_type = 'url'
						if target.startswith('static_nav:'):
							target = get_static_nav(request, target.split(':')[-1])
						navs.append({
							'text': text,
							'target': target,
							'type': url_type
						})
					break

		return {
			"is_standard_global_nav": False,
			"navs": navs
		}


@register.filter(name='get_static_nav')
def get_static_nav(request, nav_name):
	if nav_name == 'user_center':
		url = '/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%(webapp_owner_id)d&project_id=0'
	elif nav_name == 'shopping_cart':
		url = '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&project_id=0&webapp_owner_id=%(webapp_owner_id)d'
	elif nav_name == 'order_list':
		url = '/workbench/jqm/preview/?module=mall&model=order_list&action=get&workspace_id=mall&project_id=0&webapp_owner_id=%(webapp_owner_id)d&type=0'
	elif nav_name == 'product_list':
		url = '/workbench/jqm/preview/?module=mall&model=products&action=list&workspace_id=mall&project_id=0&webapp_owner_id=%(webapp_owner_id)d'
	elif nav_name == 'article_list':
		url = '/workbench/jqm/preview/?module=cms&model=category&action=get&workspace_id=cms&project_id=0&webapp_owner_id=%(webapp_owner_id)d'
	elif nav_name == 'homepage':
		webapp_owner_id = request.webapp_owner_id
		if request.webapp_owner_id:
			workspace = Workspace.objects.get(owner_id=webapp_owner_id, inner_name='home_page')
			project = Project.objects.get(owner_id=webapp_owner_id, workspace=workspace, inner_name=workspace.template_name)
			url = '/workbench/jqm/preview/?project_id=%d' % project.id
		else:
			url = '/workbench/jqm/preview/?project_id=0'

	context = {
		'webapp_owner_id': request.webapp_owner_id
	}
	return url % context


@register.filter(name='to_json_str')
def to_json_str(obj):
	return obj


@register.filter(name='get_back_homepage_url')
def get_back_homepage_url(request, homepage_workspace_info):
	"""
	当启用新版微页面时，打开的微页面设置的首页，如果不是，返回删除列表页面

	author: liupeiyu
	"""
	back_homepage_url = u'/workbench/jqm/preview/?woid={}&module=mall&model=products&action=list'.format(request.webapp_owner_id)

	profiles = UserProfile.objects.filter(user_id=request.webapp_owner_id)
	if profiles.count() > 0:
		if profiles[0].is_use_wepage:
		 	back_homepage_url = u'/termite2/webapp_page/?{}'.format(homepage_workspace_info)
		 	print back_homepage_url

	return back_homepage_url

