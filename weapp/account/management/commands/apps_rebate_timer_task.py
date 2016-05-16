# -*- coding: utf-8 -*-

import time
from datetime import timedelta,datetime

from django.core.management.base import BaseCommand
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_error

from apps.customerized_apps.rebate.export import handle_rebate_core, handle_wating_actions

class Command(BaseCommand):
	help = 'start rebate stats task'
	args = ''

	def handle(self, *args, **options):
		"""
		"""
		try:
			print ('rebate timer task start...')
			start_time = time.time()
			#处理发放微众卡的任务
			handle_rebate_core()
			end_time = time.time()
			diff = (end_time-start_time)*1000
			print ('grant card...expend %s' % diff)
			#检查暂存的记录是否有满足条件
			handle_wating_actions()
			end_time = time.time()
			diff = (end_time-start_time)*1000
			print (u'check...expend %s' % diff)
		except Exception, e:
			print u'------grant fail--------------------------------'
			print e
			notify_msg = u"发放返利微众卡失败，cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)