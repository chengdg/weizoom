# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from core import emotion

from datetime import datetime

register = template.Library()

@register.filter(name='is_system_manager')
def is_system_manager(user):
	if user is None:
		return False
	else:
		return user.username == 'manager'

@register.filter(name='get_workspace_navs')
def get_workspace_navs(user):
	from webapp.models import Workspace, Project
	from termite import pagestore as pagestore_manager
	
	webapp_editor_navs = []
	pagestore = pagestore_manager.get_pagestore_by_type('mongo')
	for workspace in Workspace.objects.filter(owner=user):
		if 'viper:' in workspace.data_backend:
			project_id = workspace.data_backend.split(':')[-1]
			project = Project.objects.get(id=project_id)
			pages = pagestore.get_pages(project_id=project_id)
			webapp_editor_nav = {
				'section': workspace.name,
				'navs': []
			}
			for page in pages:
				page_id = page['page_id']
				page_model = page['component']['model']
				print page_model
				if page_model.get('is_free_page', 'no') == 'yes':
					url = '/workbench/viper/page/?project_id=%s&page_id=%s' % (project_id, page_id)
				else:
					url = '/workbench/viper/records/?project_id=%s&page_id=%s' % (project_id, page_id)
				webapp_editor_nav['navs'].append({
					'name': page_id,
					'url': url,
					'title': page['component']['model']['navName']
				})

			webapp_editor_navs.append(webapp_editor_nav)
		elif 'module:' in workspace.data_backend:
			webapp_template_info_module = 'webapp.modules.%s.webapp_template_info' % workspace.data_backend.split(':')[-1]
			module = __import__(webapp_template_info_module, {}, {}, ['*',])
			webapp_editor_navs.append({'section': workspace.name, 'navs':module.NAV['navs']})
		else:
			pass

	return webapp_editor_navs

@register.filter(name='get_site_domain')
def get_site_domain(user):
	if user:
		return user.get_profile().host
	else:
		return settings.DOMAIN


@register.filter(name='format_emotion')
def format_emotion(content):
	return emotion.change_emotion_to_img(content)

@register.filter(name='unify_datetime')
def unify_datetime(datetime):
	return datetime.strftime('%Y/%m/%d %H:%M')

@register.filter(name='scale')
def scale(option_count, poll_count):
	if poll_count == 0:
		return 0
	compute = float(option_count)/float(poll_count)*100
	return int(compute)


@register.filter(name='cr_calculate')
def cr_calculate(pv, buy_count):
	print 'pv %d' % pv
	print 'buy_count %d' % buy_count
	cr =  float(buy_count) / float(pv) * 100
	return "%.2f" % cr

@register.filter(name='quotation_mark_translate')
def quotation_mark_translate(data):
	data = data.replace("'",'\'')
	return data

@register.filter(name='ltgt_translate')
def ltgt_translate(data):
	data = data.replace("<",'&lt;')
	data = data.replace(">",'&gt;')
	return data
