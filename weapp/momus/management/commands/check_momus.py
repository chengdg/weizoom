# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
	help = "check momus"
	args = ''

	def restart_server(self):
		#修改restart_server.py，出发runserver的重启
		file_path = os.path.join(settings.PROJECT_HOME, '../momus/restart_server.py')
		buf = []
		src_file = open(file_path, 'rb')
		for line in src_file:
			line = line.strip()
			if line:
				buf.append(line)
		src_file.close()

		if 'check_momus' in buf[-1]:
			buf = buf[:-1]
		else:
			buf.append('#restart by check_momus')

		dst_file = open(file_path, 'wb')
		for line in buf:
			print >> dst_file, line
		dst_file.close()

		print 'restart server...'
		import time
		time.sleep(2)
		print 'restart server successfully'

	
	def handle(self, **options):
		from momus.loader import loader
		loader.check()
		self.restart_server()

