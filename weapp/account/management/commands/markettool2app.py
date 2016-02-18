# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from market_tools import ToolModule
from market_tools.settings import TOOLS_ORDERING
from apps.models import CustomizedApp, CustomizedAppInfo, CustomizedappStatus
import logging

class Command(BaseCommand):
	help = "change market tool to app"
	args = ''
	
	def handle(self, **options):
		admin = User.objects.get(username='admin')
		apps = []
		for tool_module in ToolModule.all_tool_modules():
			if tool_module.module_name in TOOLS_ORDERING:
				order_index = TOOLS_ORDERING[tool_module.module_name]
			else:
				order_index = 100
			apps.append({
				"name": tool_module.module_name,
				"url": '/market_tools/%s/' % tool_module.module_name,
				"display_name": tool_module.settings.TOOL_NAME,
				"order_index": order_index
			})
			

		apps.sort(lambda x,y: cmp(x['order_index'], y['order_index']))
		for app in apps:
			app_name = 'markettool:%s' % app['name']
			app_display_name = app['display_name']
			app_url = app['url']
			if CustomizedApp.objects.filter(name=app_name).count() == 0:
				logging.info(u'create app {}'.format(app_display_name))
				app = CustomizedApp.objects.create(
					owner = admin,
					name = app_name, 
					display_name = app_display_name,
					status = CustomizedappStatus.MARKETTOOL,
					last_version = -1,
					updated_time = datetime.today()
				)

				CustomizedAppInfo.objects.create(
					owner = admin,
					customized_app = app,
					app_name = app_display_name,
					remark_name = 'markettool',
					repository_path = app_url,
					repository_username = '',
					repository_passwd = ''
				)
			else:
				logging.info(u'ignore app {}'.format(app_display_name))



