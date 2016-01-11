# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.models import Workspace, Project
import pagestore as pagestore_manager

class Command(BaseCommand):
	help = "check user's webapp project"
	args = ''
	pagestore = None

	#######################################################################
	# install_webapp_project: 为user安装webapp project
	#######################################################################
	def install_webapp_project(self, user, project_inner_name):
		inner_name = project_inner_name
		manager = User.objects.get(username='manager')

		manager_home_page_workspace = Workspace.objects.get(owner=manager, inner_name='home_page')
		manager_home_page_template_project = Project.objects.get(owner=manager, workspace=manager_home_page_workspace, inner_name=project_inner_name)
		page = Command.pagestore.get_first_page(str(manager_home_page_template_project.id))

		#为所有拥有该workspace的用户添加project
		print '********** process %s **********' % user.username
		for source_workspace in Workspace.objects.filter(owner=manager):
			try:
				project = Project.objects.get(owner=manager, workspace=source_workspace, inner_name=inner_name)
			except:
				if inner_name == 'datasource':
					continue
				else:
					raise
			full_project_name = '%s:%s' % (source_workspace.name, project.name)
			for workspace in Workspace.objects.filter(owner=user, source_workspace_id=source_workspace.id):
				is_new_created_page = True
				if Project.objects.filter(workspace=workspace, inner_name=inner_name).count() > 0:
					#更新
					print 'already have %s' % full_project_name
					is_new_created_page = False
					new_project = Project.objects.get(workspace=workspace, inner_name=inner_name)
					new_project_id = str(new_project.id)
				else:
					#创建
					print 'install %s' % full_project_name
					new_project = Project.objects.create(
						owner_id = workspace.owner_id,
						workspace = workspace,
						name = project.name,
						inner_name = project.inner_name,
						type = project.type,
						css = project.css,
						pagestore = project.pagestore,
						source_project_id = project.id,
						datasource_project_id = 0,
						template_project_id = 0
					)
					new_project_id = str(new_project.id)

				if project.type == 'jqm':
					print 'update jqm project %s' % full_project_name
					page_id = page['page_id']
					page_component = page['component']
					page_component['is_new_created'] = is_new_created_page
					Command.pagestore.save_page(new_project_id, page_id, page_component)


	#######################################################################
	# set_template_project: 为user设置template project
	#######################################################################
	def set_template_project(self, user):
		#获得home page的template project的inner name
		workspace = Workspace.objects.get(owner=user, inner_name='home_page')
		template_project = Project.objects.get(workspace=workspace, id=workspace.template_project_id)
		template_project_inner_name = template_project.inner_name

		for workspace in Workspace.objects.filter(owner=user):
			if workspace.inner_name == 'home_page':
				continue

			template_project = Project.objects.get(workspace=workspace, inner_name=template_project_inner_name)
			Workspace.objects.filter(id=workspace.id).update(template_project_id=template_project.id)


	def handle(self, **options):
		Command.pagestore = pagestore_manager.get_pagestore_by_type('mongo')

		manager = User.objects.get(username='manager')
		manager_projects = Project.objects.filter(owner=manager)
		manager_project_ids = set([p.id for p in manager_projects])
		id2project = dict([(p.id, p) for p in manager_projects])

		all_users = [user for user in User.objects.all() if (user.username != 'admin' and user.username != 'manager')]
		id2user = dict([(user.id, user) for user in all_users])

		#搜集user的project信息
		user2projects = {}
		for user in all_users:
			user_project_ids = set([p.source_project_id for p in Project.objects.filter(owner=user)])
			missing_project_ids = list(manager_project_ids - user_project_ids)
			if len(missing_project_ids) > 0:
				missing_projects = set()
				added_projects = set()
				for missing_project_id in missing_project_ids:
					missing_project = id2project[missing_project_id]
					if missing_project.inner_name in added_projects:
						continue
					else:
						missing_projects.add(missing_project)
						added_projects.add(missing_project.inner_name)
				user2projects[user.id] = missing_projects

		if len(user2projects) == 0:
			print 'no user should be update'
			return

		print u'缺失webapp project的用户为：'
		print '\tUSER\tPROJECTS'
		for user_id, projects in user2projects.items():
			print '\t', id2user[user_id].username, '\t',
			for project in projects:
				print project.name,
			print ''

		while True:
			print u'\npress "y" to install project for all user, "n" to exit'
			print '>>>',
			value = raw_input()
			if value == 'n':
				return
			if value == 'y':
				break

		for user_id, projects in user2projects.items():
			user = id2user[user_id]
			for project in projects:
				self.install_webapp_project(user, project.inner_name)
				self.set_template_project(user)

		print 'finish!'
