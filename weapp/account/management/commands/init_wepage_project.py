# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.models import Project
from termite2.project import Project as ProjectResource

class FakeRequest(object):
	def __init__(self):
		pass

class Command(BaseCommand):
	help = "init wepage project for existed user"
	args = ''
	
	def handle(self, **options):
		for user in User.objects.all():
			if user.username == 'admin':
				continue
			if Project.objects.filter(owner=user, type='wepage').count() > 0:
				print '[%s] already have wepage project, skip.' % user.username
				continue
			profile = None
			try:
				profile = user.get_profile()
			except:
				profile = None
			if not profile:
				continue
				
			if profile.manager_id > 2:
				print '[%s] is sub account, skip.'
				continue

			print '[%s] create new wepage project.' % user.username
			request = FakeRequest()
			post = {
				'source_template_id': -1
			}
			request.POST = post
			user.is_manager = False
			request.user = user
			ProjectResource.api_put(request)

			Project.objects.filter(type='wepage').update(is_active=True, is_enable=True, site_title=u'空白页面', inner_name='wepage_empty')


