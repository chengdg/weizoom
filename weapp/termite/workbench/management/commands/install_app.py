# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from account.models import UserProfile

class Command(BaseCommand):
	help = "install generated app"
	args = '[app name]'

	def __dump_file(self, file_path):
		f = open(file_path, 'rb')
		print f.read()
		f.close()
	
	def handle(self, app, **options):
		print '========== 1. clear db =========='
		cmd = 'python manage.py sqlclear %s > clear.sql' % app
		subprocess.call(cmd, shell=True)
		self.__dump_file('clear.sql')

		cmd = 'mysql -u termite --password=weizoom termite < clear.sql > db.log 2>&1'
		subprocess.call(cmd, shell=True)
		self.__dump_file('db.log')

		print '========== 2. sync db =========='
		cmd = 'python manage.py syncdb'
		subprocess.call(cmd, shell=True)

		print '=========== 3. change webapp_template =========='
		user = User.objects.get(username='test')
		profile = UserProfile.objects.get(user=user)
		profile.webapp_template = app
		profile.save()
		print profile.webapp_template
