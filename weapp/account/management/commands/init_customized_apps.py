# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module

from apps.models import CustomizedApp, CustomizedAppInfo, CustomizedappStatus


class Command(BaseCommand):
	help = "init all customized apps for all user"
	args = ''
	
	def handle(self, **options):
		admin = User.objects.get(username='admin')
		module_list = ['lottery', 'survey', 'event', 'vote', 'sign','red_envelope', 'powerme','exsurvey', 'red_packet', 'group', 'shvote']
		for module_name in module_list:
			try:
				import_module("{}.{}".format('apps.customerized_apps', module_name))
				if CustomizedApp.objects.filter(name=module_name).count() == 0:
					print 'create customized app ', module_name

					app = CustomizedApp.objects.create(
						owner = admin,
						name = module_name,
						display_name = module_name,
						status = CustomizedappStatus.RUNNING,
						last_version = -1,
						updated_time = datetime.today()
					)

					CustomizedAppInfo.objects.create(
						owner = admin,
						customized_app = app,
						app_name = module_name,
						remark_name = 'customized_app',
						repository_path = '',
						repository_username = '',
						repository_passwd = ''
					)
				else:
					print 'ignore customized app ', module_name
			except:
				pass