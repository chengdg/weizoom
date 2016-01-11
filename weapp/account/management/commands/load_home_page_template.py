# -*- coding: utf-8 -*-

import os
import subprocess
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simulator.models import *
import pagestore as pagestore_manager
from webapp.models import *

class Command(BaseCommand):
	help = "load a specific template for home page"
	args = '[template]'
	
	def handle(self, template, **options):
		manager = User.objects.get(username='manager')
		pagestore = pagestore_manager.get_pagestore_by_type('mongo')
		modules_dir = os.path.join(settings.PROJECT_HOME, '../webapp/modules')
		workspace = Workspace.objects.get(owner=manager, inner_name='home_page')
		project = Project.objects.get(workspace=workspace, inner_name=template)

		module_dir = os.path.join(modules_dir, 'viper_workspace_home_page')
		project_dir = os.path.join(module_dir, 'project_jqm_%s' % template)

		pages_data_file_path = os.path.join(project_dir, 'pages.json')
		pages_data_file = open(pages_data_file_path, 'rb')
		content = pages_data_file.read()
		pages_data_file.close()
		page_count = 0
		for page in json.loads(content):
			page_count += 1
			page_id = page['page_id']
			page_component = page['component']
			page_component['is_new_created'] = True
			pagestore.save_page(str(project.id), page_id, page_component)

		if page_count > 0:
			print 'create project\'s %d pages: %s' % (page_count, pages_data_file_path)
