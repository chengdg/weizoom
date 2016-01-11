# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from modules.member.models import *
from account.models import *



class Command(BaseCommand):
	help = "update member nick_name  user_icon"
	args = 'webapp_id'
	
	def handle(self,*args, **options):
		print options
		print args

		if len(args) != 1:
			print ' need webapp_id!'
			return 
		if UserProfile.objects.filter(webapp_id=args[0]).count() == 0:
			print 'invalid webapp_id' 
			return 

		user_profile = UserProfile.objects.get(webapp_id=args[0])
		members = Member.objects.filter(is_for_test=False, webapp_id=args[0])
		from modules.member.member_info_util import member_basic_info_updater
		for member in members:
			try:
				member_basic_info_updater(user_profile, member)
			except:
				pass
			
