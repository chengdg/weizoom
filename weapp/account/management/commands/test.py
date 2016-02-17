# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand, CommandError

from utils.cache_util import SET_CACHE, delete_cache, delete_pattern
from apps.customerized_apps.powerme import models as app_models


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, **options):
		"""
		@param args:
		@param options:
		@return:
		"""
		print 'test start...'
		a = app_models.TestA.objects()
		if a.count() > 0:
			a = a.first()
		else:
			a = app_models.TestA()
			a.save()
		r = a.update(add_to_set__li=1)
		print r, '+++++++++++++++'

		print 'test end...'