# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.models import Workspace, Project

class Command(BaseCommand):
	help = "check user's products"
	args = ''
	
	def handle(self, **options):
		manager = User.objects.get(username='manager')
		manager_workspaces = list(Workspace.objects.filter(owner=manager))
		name2mworkspace = dict([(w.inner_name, w) for w in manager_workspaces])
		id2mworkspace = dict([(w.id, w) for w in manager_workspaces])

		manager_projects = list(Project.objects.filter(owner=manager))
		name2mproject = dict([('%s:%s' % (id2mworkspace[p.workspace_id].inner_name, p.inner_name), p) for p in manager_projects])

		id2workspace = dict([(w.id, w) for w in Workspace.objects.all()])
		print '********** process worksapce **********'
		for workspace in Workspace.objects.all():
			if workspace.owner_id == manager.id:
				continue

			source_workspace = name2mworkspace[workspace.inner_name]
			if workspace.source_workspace_id != source_workspace.id:
				print "workspace(%d) source_workspace_id(%d) != manager's workspace id(%d)" % (workspace.id, workspace.source_workspace_id, source_workspace.id)
				Workspace.objects.filter(id=workspace.id).update(source_workspace_id=source_workspace.id)


		id2project = dict([(p.id, p) for p in Project.objects.all()])
		print '********** process project **********'
		for project in Project.objects.all():
			if project.owner_id == manager.id:
				continue

			workspace = id2workspace[project.workspace_id]
			name = '%s:%s' % (workspace.inner_name, project.inner_name)
			source_project = name2mproject[name]

			if project.source_project_id != source_project.id:
				print "project(%d) source_project_id(%d) != manager's project id(%d)" % (project.id, project.source_project_id, source_project.id)	
				Project.objects.filter(id=project.id).update(source_project_id=source_project.id)

		print 'finish'