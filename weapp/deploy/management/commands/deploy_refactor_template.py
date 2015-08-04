# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.models import Workspace, Project

class Command(BaseCommand):
	help = "create standard product model for existed product if necessary"
	args = ''
	
	def handle(self, **options):
		count = 0
		for workspace in Workspace.objects.all():
			if not workspace.inner_name == 'home_page':
				continue

			project = Project.objects.get(id=workspace.template_project_id)
			Workspace.objects.filter(id=workspace.id).update(template_name=project.inner_name)
			count += 1

		print '[finish] processed %d workspaces' % count
