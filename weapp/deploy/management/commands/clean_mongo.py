# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from pymongo import Connection

from weapp import settings

class Command(BaseCommand):
	help = "clean mongodb"
	args = ''
	
	def handle(self, **options):
		#清理mongo
		print '************* start clear MONGODB(%s:%s) *************' % (settings.PAGE_STORE_SERVER_HOST, settings.PAGE_STORE_SERVER_PORT)
		connection = Connection(settings.PAGE_STORE_SERVER_HOST, settings.PAGE_STORE_SERVER_PORT)
		connection.drop_database(settings.PAGE_STORE_DB)
		print '************* finish clear MONGODB *************'
