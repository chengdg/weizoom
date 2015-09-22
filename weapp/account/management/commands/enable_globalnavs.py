# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from termite2 import models as termite_models
from termite import pagestore as pagestore_manager

class Command(BaseCommand):
	help = "enable global navbar for all user"
	args = ''
	
	def handle(self, **options):		
		print '----- start '
		for user in User.objects.all():
			if user.username == 'admin' or user.username == 'manager':
				continue

			navbars = termite_models.TemplateGlobalNavbar.objects.filter(owner=user, is_enable=False)
			if navbars.count() > 0:
				
				pagestore = pagestore_manager.get_pagestore('mongo')
				project_id = 'fake:wepage:%s:navbar' % user.id
				page_id = 'navbar'
				navbar_page = pagestore.get_page(project_id, page_id)

				if navbar_page is None:
					navbar = navbars[0]
					navbar.is_enable = True
					navbar.save()

					print u'正在开启底部导航 username = {}'.format(user.username)

		print '----- end enable global navbar'