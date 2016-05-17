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
		@args: grant  ==== 发卡
			   check  ==== 处理待发卡记录
		"""
		print ('rebate timer task start...')

		l = len(args)
		if l == 1:
			if args[0] == 'grant':
				self.__grant()
			elif args[0] == 'check':
				self.__check()
		elif l == 0:
			self.__grant()
			self.__check()
		else:
			print "invalid command %s" % ','.join(args)

		print ('rebate timer task end...')

	def __grant(self):
		start_time = time.time()
		#处理发放微众卡的任务
		handle_rebate_core()
		end_time = time.time()
		diff = (end_time-start_time)*1000
		print ('grant card...expend %s' % diff)

	def __check(self):
		start_time = time.time()
		#检查暂存的记录是否有满足条件
		handle_wating_actions()
		end_time = time.time()
		diff = (end_time-start_time)*1000
		print (u'check...expend %s' % diff)