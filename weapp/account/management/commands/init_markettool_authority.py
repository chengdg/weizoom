# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from market_tools.models import MarketToolAuthority

class Command(BaseCommand):
	help = "init mall counter for all user"
	args = ''
	
	def handle(self, **options):
		for user in User.objects.all():
			if MarketToolAuthority.objects.filter(owner=user).count() > 0:
				continue

			print 'init market tool authority for user: ', user.username
			MarketToolAuthority.objects.create(owner=user)

