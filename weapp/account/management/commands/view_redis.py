# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from utils import cache_util
from bson import json_util
import json

class Command(BaseCommand):
	help = "init mall counter for all user"
	args = ''
	
	def handle(self, key, **options):
		print key
		value = cache_util.get_cache(key)
		if value:
			print json.dumps(value, default=json_util.default, indent=True)
		else:
			print 'no value'
		
