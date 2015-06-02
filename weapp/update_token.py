# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import sys
import upyun
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from django.conf import settings

import json
import urllib2

from datetime import datetime
from datetime import timedelta


from core.exceptionutil import unicode_full_stack


from weixin.user.models import WeixinMpUserAccessToken

from watchdog.utils import watchdog_fatal, watchdog_notice, watchdog_warning

WATCHDOG_TYPE = 'ACCESSTOKEN_UPDATE_SERVICE'

class Service(object):

	# LOG = Logger.get_logger()

	def __init__(self):
		self.MaxRetryTimes = 5

		self.WEIXIN_ACCESS_TOKEN_UPDATE_URL_TMPL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
		self.ACCESS_TOKEN_ATTR = 'access_token'
		self.ACCESS_TOKEN_EXPIRES_IN_ATTR = 'expires_in'

		self.UPDATE_TIME_SPAN_SECONDS = 5 # 更新间隔为5分钟

	def _decode_json_str(self, str):
		assert (str)

		return json.loads(str)

	def _get_access_token_update_response(self, update_url):
		assert (update_url)

		return self._decode_json_str(urllib2.urlopen(update_url).read())

	def _get_new_token_info(self, access_token):
		assert (access_token)

		update_url = self.WEIXIN_ACCESS_TOKEN_UPDATE_URL_TMPL.format(access_token.app_id, access_token.app_secret)
		#self.LOG.info(u"update access token for user({}) with url({})".format(access_token.mpuser.username, update_url))

		update_response_data = None
		try:
			update_response_data = self._get_access_token_update_response(update_url)
			#self.LOG.info(u'微信响应信息:' + json.dumps(update_response_data))
		except:
			watchdog_notice(u"failed to update access token for user({}), cause:\n{}".format(access_token.mpuser.username, unicode_full_stack()))

			#self.LOG.warn(u"最多重试{}次进行更新".format(self.MaxRetryTimes))

			for retry_time in xrange(self.MaxRetryTimes):
				try:
					update_response_data = self._get_access_token_update_response(update_url)
				except:
					watchdog_notice(u"failed to update access token for user({}), cause:\n{}".format(access_token.mpuser.username, unicode_full_stack()))

		return update_response_data

	def _update_access_token_record(self, access_token, new_access_token, expires_span):
		assert (access_token and new_access_token)

		next_expire_time = datetime.now() + timedelta(seconds=expires_span)
		access_token.expire_time = next_expire_time
		access_token.access_token = new_access_token
		access_token.is_active = True

		access_token.save()

	def _update_mpuser_access_token(self, access_token):
		assert (access_token)

		new_token_info = self._get_new_token_info(access_token)
		if None == new_token_info:
			return

		if not new_token_info.has_key(self.ACCESS_TOKEN_ATTR):
			watchdog_warning(u"failed to update access token for user({}), response:\n{}".format(access_token.mpuser.username, json.dumps(new_token_info)))

		new_access_token = new_token_info[self.ACCESS_TOKEN_ATTR].strip()
		expires_span = new_token_info[self.ACCESS_TOKEN_EXPIRES_IN_ATTR]

		self._update_access_token_record(access_token, new_access_token, expires_span)

	def _is_access_token_can_update(self, access_token):
		assert (access_token)
		return access_token.app_id and access_token.app_secret

	def _get_access_tokens_need_to_update(self):
		"""获取当前access_token已经失效的，或者当前有效，但会在下一次更新之前就会失效的进行更新"""
		invalid_access_tokens = WeixinMpUserAccessToken.objects.filter(is_active=False)

		next_update_time = datetime.now() + timedelta(minutes=self.UPDATE_TIME_SPAN_SECONDS)
		to_expire_access_token = WeixinMpUserAccessToken.objects.filter(expire_time__lt=next_update_time)

		need_to_update_access_tokens = []
		if invalid_access_tokens:
			need_to_update_access_tokens.extend(invalid_access_tokens)
		if to_expire_access_token:
			need_to_update_access_tokens.extend(to_expire_access_token)

		return [to_update_access_token for to_update_access_token in need_to_update_access_tokens \
				if self._is_access_token_can_update(to_update_access_token)]

	#==============================================================================
	# run : service的入口函数
	#==============================================================================
	def run(self):
		#add your service code below, use send_message_to(service_name, message, self.LOG) to send
		#message to specific service, and use log_exception(logger) to trace exception
		# self.LOG.info(u"run with arg : %s" % str(args))

		# self.LOG.info(u'获取需要更新access_token的微信公众号')
		need_to_update_access_token_users = self._get_access_tokens_need_to_update()

		for access_token in need_to_update_access_token_users:
			try:
				#self.LOG.info(u"username:{} expire_time:{}".format(access_token.mpuser.username, get_datetime_str(access_token.expire_time)))
				self._update_mpuser_access_token(access_token)
			except:
				mpuser_owner = access_token.mpuser.owner
				notify_message = u"failed to update access_token for user:{}, cause:\n{}".format(access_token.mpuser.username, unicode_full_stack())
				#self.LOG.error(notify_message)
				watchdog_fatal(notify_message, type=WATCHDOG_TYPE, user_id=mpuser_owner.id)
service = Service()
service.run()
