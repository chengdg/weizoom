# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.modules.mall.models import Product, ProductSwipeImage

from webapp.models import GlobalNavbar, Workspace

class Command(BaseCommand):
	help = "init global navbar for all user"
	args = ''
	
	def handle(self, **options):
		for user in User.objects.all():
			if user.username == 'admin' or user.username == 'manager':
				continue

			#如果用户还没有global navbar，创建之
			if GlobalNavbar.objects.filter(owner=user).count() == 0:
				try:
					print '[create] %s' % user.username
					home_page_workspace = Workspace.objects.get(owner=user, inner_name='home_page')
					mall_workspace = Workspace.objects.get(owner=user, inner_name='mall')
					user_center_workspace = Workspace.objects.get(owner=user, inner_name='user_center')

					#准备webapp global navbar的模板
					src = open(os.path.join(settings.PROJECT_HOME, '..', 'webapp/resource/init_global_navbar.json'), 'rb')
					webapp_global_navbar_template = src.read()
					src.close()

					context = {
						"webapp_owner_id": user.id, 
						"home_page_workspace_id": home_page_workspace.id,
						"mall_workspace_id": mall_workspace.id,
						"user_center_workspace_id": user_center_workspace.id
					}
					webapp_global_navbar_content = webapp_global_navbar_template % context

					GlobalNavbar.objects.create(
						owner = user,
						content = webapp_global_navbar_content,
						is_enable = True
					)
				except:
					print '[skip] %s' % user.username
			else:
				print '[ignore] %s' % user.username

