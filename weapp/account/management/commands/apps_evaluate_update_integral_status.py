# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from apps.customerized_apps.evaluate import models as evaluate_models

class Command(BaseCommand):
	help = 'start evaluate update integral status task'
	args = ''

	def handle(self, **options):
		"""
		更新所有已经审核通过或者置顶的评价积分发放状态
		"""
		try:
			print 'start update evaluate integral status'
			evaluate_models.ProductEvaluates.objects(status__in=[evaluate_models.STATUS_PASSED, evaluate_models.STATUS_TOP]).update(set__has_increase_integral=True)
			print 'stop update evaluate integral status'
		except:
			print 'update evaluate integral status error'
