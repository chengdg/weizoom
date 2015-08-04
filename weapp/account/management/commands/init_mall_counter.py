# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from mall.models import MallCounter

class Command(BaseCommand):
	help = "init mall counter for all user"
	args = ''
	
	def handle(self, **options):
		for user in User.objects.all():
			if MallCounter.objects.filter(owner=user).count() > 0:
				continue

			print 'init mall counter for user: ', user.username
			MallCounter.objects.create(owner=user)

