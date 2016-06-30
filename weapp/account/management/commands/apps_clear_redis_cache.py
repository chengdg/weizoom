# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand, CommandError

from utils.cache_util import SET_CACHE, delete_cache, delete_pattern
from apps.customerized_apps.powerme import models as app_models
from modules.member.models import Member


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, *args, **options):
		"""

		@param args:
			None: 清空所有以apps_开头的redis缓存
			args[0]: 清空所有以apps_args[0]_开头的redis缓存
			args[1]: 清空所有以apps_args[0]_args[1]_开头的redis缓存
		注:签到的缓存key用的是weapp_owner_id, 其他活动用的是主表的id
		@param options:
		@return:
		"""
		print 'clear apps redis cache start...'
		l = len(args)
		if l == 1:
			apps_name = args[0]
			patten = "apps_%s_*" % apps_name
			delete_pattern(patten)
			print 'delete all cache those match patten', patten
		elif l == 2:
			apps_name = args[0]
			apps_id = args[1]
			patten = "apps_%s_%s*" % (apps_name, apps_id)
			delete_pattern(patten)
			print 'delete all cache those match patten', patten
		else:
			patten = "apps_*"
			delete_pattern(patten)
			print 'delete all apps cache'
		print 'clear apps redis cache end...'