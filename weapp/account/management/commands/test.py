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
		if a.count() <= 0:
			app_models.TestA(
				li = [0.43, 1.2423,3567]
			).save()
		r = app_models.TestA.objects(li__exact=1.2)
		print r.count(), '+++++++++++++++'

		print 'test end...'