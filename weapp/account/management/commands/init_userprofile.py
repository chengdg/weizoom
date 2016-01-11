# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from mall.models import Product, ProductSwipeImage

from webapp.models import GlobalNavbar, Workspace
from account.models import UserProfile

class Command(BaseCommand):
	help = "init global navbar for all user"
	args = ''
	
	def handle(self, **options):
		for user in User.objects.all():
			if user.username == 'admin' or user.username == 'manager':
				continue

			#如果用户还没有global navbar，创建之
			try:
				home_page_workspace = Workspace.objects.get(owner=user, inner_name='home_page')
				print '[update] %s' % user.username
				UserProfile.objects.filter(user=user).update(
					homepage_template_name = home_page_workspace.template_name,
					backend_template_name = home_page_workspace.backend_template_name,
					homepage_workspace_id = home_page_workspace.id
				)
			except:
				print '[skip] %s' % user.username
