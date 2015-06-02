# -*- coding: utf-8 -*-

import os
import subprocess
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from weixin.user.models import *
#from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
#weixin_http_client = WeixinHttpClient()
from core.wxapi import get_weixin_api
import datetime
from account.models import UserProfile
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

class Command(BaseCommand):
	help = "load a specific userid for home page"
	args = '[user_id]'
	
	def handle(self, user_id, **options):
		user = User.objects.get(id=user_id)

		mp_user = get_binding_weixin_mpuser(user)
		if mp_user is None:
			return None

		if not mp_user.is_service or not mp_user.is_certified:
			return None
			
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
		weixin_api = get_weixin_api(mpuser_access_token)

		result = weixin_api.api_shakearound_device_aopplyid(3,u'测试')
		print result
