# -*- coding:utf-8 -*-

import time
import os
import json
from datetime import timedelta, datetime, date

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from core import emotion
from utils import component_template_util

register = template.Library()

@register.filter(name='load_app_views_and_dialogs')
def load_app_views_and_dialogs(app):
	app_dir = os.path.join(settings.PROJECT_HOME, '../apps/customerized_apps', app)
	if not os.path.isdir(app_dir):
		return ''

	items = ["<!-- start app medias for app %s -->" % app]
	views_dir = os.path.join(app_dir, 'static/js/view')
	if os.path.isdir(views_dir):
		pass

	dialogs_dir = os.path.join(app_dir, 'static/js/dialog')
	if os.path.isdir(dialogs_dir):
		for dialog_dir in os.listdir(dialogs_dir):
			#判断是否是合法的dialog目录
			dialog_js_path = os.path.join(dialogs_dir, dialog_dir, 'dialog.js')
			if not os.path.isfile(dialog_js_path):
				continue

			#读取dialog.js			
			src = open(dialog_js_path, 'rb')
			js_content = src.read()
			src.close()
			items.append("\t<!-- start %s/dialog.js -->" % dialog_dir)
			items.append('<script type="text/javascript">');
			items.append(js_content)
			items.append('</script>');
			items.append("\t<!-- finish %s/dialog.js -->" % dialog_dir)

			#读取dialog.html
			dialog_html_path = os.path.join(dialogs_dir, dialog_dir, 'dialog.html')
			src = open(dialog_html_path, 'rb')
			html_content = src.read()
			src.close()
			items.append("\t<!-- start %s/dialog.html -->" % dialog_dir)
			items.append(html_content)
			items.append("\t<!-- finish %s/dialog.html -->" % dialog_dir)

	if len(items) > 1:
		items.append("<!-- finish app medias for app %s -->" % app)
		return '\n'.join(items)
	else:
		return ''


@register.filter(name='load_app_components_handlebar_templates')
def load_app_components_handlebar_templates(component_category):
	components_dir = '%s/../termite/static/termite_js/app/component/%s' % (settings.PROJECT_HOME, component_category)
	handlebar_template = component_template_util.generate_handlebar_template(components_dir)
	return handlebar_template


@register.filter(name='load_app_components')
def load_app_components(app_components):
	app_components = json.loads(app_components)
	items = ["<!-- start app components -->"]
	components_dir = os.path.join(settings.PROJECT_HOME, '../termite/static/termite_js/app/component')
	for app_component in app_components:
		category, component_name = app_component.split('.')
		component_dir = os.path.join(components_dir, category, component_name)
		if os.path.isdir(component_dir):
			print '[app] %s is not a valid app componet' % app_component

		for file_name in os.listdir(component_dir):
			if file_name.endswith('.js'):
				src = open(os.path.join(component_dir, file_name), 'rb')
				content = src.read()
				src.close()

				items.append("\t<!-- start %s/%s/%s -->" % (category, component_name, file_name))
				items.append('<script type="text/javascript">');
				items.append(content)
				items.append('</script>');
				items.append("\t<!-- finish %s/%s/%s -->" % (category, component_name, file_name))

	items.append("<!-- finish app components %s -->")
	return '\n'.join(items)
