# -*- coding: utf-8 -*-

import os
import subprocess
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from weixin.user.models import *
from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
from core.upyun_util import upload_qrcode_url_to_upyun
weixin_http_client = WeixinHttpClient()
from account.models import UserProfile
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from weixin.util import refresh_auth_token, get_authorizer_info


class Command(BaseCommand):
	help = "init global navbar for all user"
	args = ''

	def handle(self, **options):
		for component in ComponentInfo.objects.filter(is_active=True):
			weixin_api = WeixinApi(None, weixin_http_client)
			from weixin.message.message_handler.tasks import record_call_weixin_api
			# 获取第三方平台的component_access_token
			try:
				result = weixin_api.get_component_token(component.app_id, component.app_secret, component.component_verify_ticket)
				if result.has_key('errcode'):
					if result['errcode'] == -1 or result['errcode'] == 995995:
						result, success = self.__get_component_token_retry(weixin_api, component)
					else:
						success = False
						watchdog_error('call weixin api: get_component_token , result:{}'.format(result))
				else:
					success = True
			except:
				result, success = self.__get_component_token_retry(weixin_api, component)
			if result != None:
				record_call_weixin_api.delay('get_component_token', success)
			else:
				continue

			component_access_token = result['component_access_token']
			component.component_access_token = component_access_token
			component.save()
			mp_user = None
			#更新appid token


			weixin_api = WeixinApi(component_access_token, weixin_http_client)
			update_fail_auth_appid = []
			for auth_appid in ComponentAuthedAppid.objects.filter(is_active=True, component_info=component):
				self.__update_auth_appid(auth_appid, weixin_api, component, update_fail_auth_appid)

			print u"更新失败重试数" + str(len(update_fail_auth_appid))
			if update_fail_auth_appid:
				for auth_appid in update_fail_auth_appid:
					self.__update_auth_appid(auth_appid, weixin_api, component)


	def __update_auth_appid(self, auth_appid = None, weixin_api = None, component = None, error_auth_appid = []):
		return_msg, mp_user = refresh_auth_token(auth_appid, weixin_api, component)
		if return_msg:
			if return_msg == 'error':
				error_auth_appid.append(auth_appid)
			else:
				get_authorizer_info(auth_appid, weixin_api, component, mp_user)


	def __get_component_token_retry(self, weixin_api=None, component = None):
		try:
			result = weixin_api.get_component_token(component.app_id, component.app_secret, component.component_verify_ticket)
			print 'justing,retry :\n{}'.format(result)
			#watchdog_info('call weixin api: get_component_token , result:{}'.format(result))
			if result.has_key('errcode'):
				success = False
				watchdog_error('call weixin api: get_component_token , result:{}'.format(result))
			else:
				success = True
			return result, success
		except:
			return None, False