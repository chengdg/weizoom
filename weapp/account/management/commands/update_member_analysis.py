# -*- coding: utf-8 -*-

import os
import subprocess


from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from modules.member.models import *
from account.models import *
from account.util import *
from core.wxapi import get_weixin_api
import datetime

class Command(BaseCommand):
	help = "update member analysis"
	args = 'webapp_id'
	
	def handle(self,*args, **options):
		print options
		print args

		date_time = datetime.datetime.now() + datetime.timedelta(days=-1)
		date_time = date_time.strftime("%Y-%m-%d")
		print date_time
		user_profiles = UserProfile.objects.filter(is_mp_registered=True)
		for user_profile in user_profiles:
			print user_profile.webapp_id
			try:
				mp_user = get_binding_weixin_mpuser(user_profile.user_id)
				if mp_user is None:
					continue

				mpuser_access_token = get_mpuser_accesstoken(mp_user)
				if mpuser_access_token is None:
					continue

				if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
					weixin_api = get_weixin_api(mpuser_access_token)
					summary_result = weixin_api.api_get_user_summary(date_time, date_time)


					cumulate_result = weixin_api.api_get_user_cumulate(date_time, date_time)
					print cumulate_result
						
					if summary_result.has_key('list'):
						MemberAnalysis.objects.filter(owner_id=user_profile.user_id, date_time=date_time).delete()
						member_analysis = MemberAnalysis.objects.create(owner_id=user_profile.user_id, date_time=date_time)
						total_new_user = 0
						total_cancel_user = 0
						for summary_data in summary_result['list']:
							new_user = summary_data['new_user']
							cancel_user = summary_data['cancel_user']
							MemberAnalysisDetail.objects.create(
								member_analysis = member_analysis,
								user_source = summary_data['user_source'],
								new_user = new_user,
								cancel_user = cancel_user
								)
							total_new_user = total_new_user + new_user
							total_cancel_user = total_cancel_user + cancel_user
						member_analysis.cancel_user = total_cancel_user
						member_analysis.new_user = total_new_user
						member_analysis.net_growth = total_new_user - total_cancel_user
						member_analysis.save()

						if cumulate_result.has_key('list'):
							cumulate_user = cumulate_result['list'][0]['cumulate_user']
							member_analysis.cumulate_user = cumulate_user
							member_analysis.save()
			except:
				print 'error:', user_profile.webapp_id
		


			


