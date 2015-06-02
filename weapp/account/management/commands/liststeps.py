# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.dispatch import Signal
from django.dispatch.dispatcher import receiver


class Command(BaseCommand):
	help = "change market tool to app"
	args = 'module'
	
	def handle(self, module, **options):
		steps_dir = 'features/steps'
		for file in os.listdir(steps_dir):
			if not file.startswith(module):
				continue
			if not file.endswith('.py'):
				continue
			buf = ["\n========== %s ==========" % file,]
			for line in open(os.path.join(steps_dir, file), 'rb'):
				if ('@when' in line) or ('@then' in line) or ('@given' in line) or ('@step' in line):
					buf.append(line.strip().replace('(', '\t').replace(')', '').replace('u"', '').replace('"', ''))
			print '\n'.join(buf).decode('utf-8')


