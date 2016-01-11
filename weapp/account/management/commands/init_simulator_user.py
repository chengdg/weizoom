# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simulator.models import *

class Command(BaseCommand):
	help = "init mall counter for all user"
	args = ''
	
	def handle(self, **options):
		users = [{
			'name': 'zhouxun',
			'display_name': u'周迅'
		}, {
			'name': 'yangmi',
			'display_name': u'杨幂'
		}, {
			'name': 'bigs',
			'display_name': u'大S'
		}, {
			'name': 'leijun',
			'display_name': u'雷军'
		}, {
			'name': 'mayun',
			'display_name': u'马云'
		}, {
			'name': 'bill',
			'display_name': u'bill'
		}, {
			'name': 'tom',
			'display_name': u'tom'
		}]
		
		user2followers_list = [
			{'zhouxun': ['leijun', 'yangmi', 'bigs']},
			{'yangmi': ['leijun', 'zhouxun', 'bigs']},
			{'bigs': ['mayun', 'zhouxun', 'yangmi']},
			{'leijun': ['mayun', 'zhouxun']},
			{'mayun': ['leijun', 'zhouxun']},
		]

		#清空老数据
		SimulatorUserRelation.objects.all().delete()
		SharedMessage.objects.all().delete()
		SimulatorUser.objects.all().delete()

		#创建SimulatorUser
		name2user = {}
		for user in users:
			simulator_user = SimulatorUser.objects.create(
				name = user['name'],
				display_name = user['display_name']
			)

			name2user[user['name']] = simulator_user

		#创建SimulatorUser的关注关系
		for user2followers in user2followers_list:
			for user_name, follower_names in user2followers.items():
				for follower_name in follower_names:
					follower = name2user[follower_name]
					followed = name2user[user_name]

					SimulatorUserRelation.objects.create(
						follower = follower,
						followed = followed
					)
