# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json
import urllib2

from datetime import datetime
from datetime import timedelta

from core.exceptionutil import unicode_full_stack

from models import WeixinMpUserAccessToken
from watchdog.utils import watchdog_fatal, watchdog_error


ACCESS_TOKEN_UPDATE_MAX_RETRY_TIMES = 5
ACCESS_TOKEN_UPDATE_URL_TMPL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
ACCESS_TOKEN_ATTR = 'access_token'
ACCESS_TOKEN_EXPIRES_IN_ATTR = 'expires_in'

def _get_access_token_update_response(update_url):
	assert (update_url)

	return json.loads(urllib2.urlopen(update_url).read())

def _update_mpuser_access_token(access_token):
	if access_token is None:
		return

	new_token_info = self._get_new_token_info(access_token.app_id, access_token.app_secret)
	if None == new_token_info:
		return

	if not new_token_info.has_key(self.ACCESS_TOKEN_ATTR):
		self.__notify(u"failed to update access token for user({}), response:\n{}".format(access_token.mpuser.username, json.dumps(new_token_info)))

	new_access_token = new_token_info[self.ACCESS_TOKEN_ATTR].strip()
	expires_span = new_token_info[self.ACCESS_TOKEN_EXPIRES_IN_ATTR]

	try:
		self._update_access_token_record(access_token, new_access_token, expires_span)
	except:
		full_stack_str = self._get_full_stack_unicode()
		self.__notify(u"failed to update access token in db for user({}), cause:\n{}".format(access_token.mpuser.username, full_stack_str))

def _get_new_token_info(app_id, app_secret):
	if app_id is None or app_secret is None:
		return None

	update_url = ACCESS_TOKEN_UPDATE_URL_TMPL.format(app_id, app_secret)
	update_response_data = None
	try:
		update_response_data = _get_access_token_update_response(update_url)
	except:
		full_stack_str = unicode_full_stack()
		watchdog_fatal(u"failed to update access token for app_id({}), cause:\n{}".format(app_id, full_stack_str))

		#self.LOG.warn(u"最多重试{}次进行更新".format(self.MaxRetryTimes))

		for retry_time in xrange(ACCESS_TOKEN_UPDATE_MAX_RETRY_TIMES):
			try:
				update_response_data = _get_access_token_update_response(update_url)
			except:
				full_stack_str = unicode_full_stack()
				watchdog_fatal(u"failed to update access token for appid:({}), cause:\n{}".format(app_id, full_stack_str))

	return update_response_data

def _update_access_token_record(access_token, new_access_token, expires_span):
	assert (access_token and new_access_token)

	now = datetime.now()
	next_expire_time = now + timedelta(seconds=expires_span)
	access_token.expire_time = next_expire_time
	access_token.access_token = new_access_token
	access_token.is_active = True
	access_token.update_time = now

	access_token.save()

def update_access_token(access_token):
	if access_token is None:
		return False

	if type(access_token) is not WeixinMpUserAccessToken:
		raise ValueError(u'access_token must be WeixinMpUserAccessToken')

	new_token_info = _get_new_token_info(access_token.app_id, access_token.app_secret)
	if None == new_token_info:
		False

	if new_token_info.has_key(ACCESS_TOKEN_ATTR):
		#watchdog_error(u"failed to update access token for user({}), response:\n{}".format(access_token.mpuser.username, json.dumps(new_token_info)))
		try:
			new_access_token = new_token_info[ACCESS_TOKEN_ATTR].strip()
			expires_span = new_token_info[ACCESS_TOKEN_EXPIRES_IN_ATTR]
		
			_update_access_token_record(access_token, new_access_token, expires_span)
			return True
		except:
			full_stack_str = unicode_full_stack()
			watchdog_fatal(u"failed to update access token in db for user({}), cause:\n{}".format(access_token.mpuser.username, full_stack_str))

	return False

def __get_weixin_update_access_token_response(app_id, app_secret):
	update_url = WEIXIN_ACCESS_TOKEN_UPDATE_URL_TMPL.format(app_id, app_secret)
	try:
		return weixin_http_client.get(update_url)
	except:
		notify_msg = u"failed to update access token with (appid:'{}', app_secret:'{}'), cause:\n{}".format(app_id, app_secret, unicode_full_stack())
		watchdog_fatal(notify_msg)

		for retry_time in xrange(3): #重试3次
			try:
				return weixin_http_client.get(update_url)
			except:
				notify_msg = u"failed to update access token with (appid:'{}', app_secret:'{}'), cause:\n{}".format(app_id, app_secret, unicode_full_stack())
				watchdog_fatal(notify_msg)

		return None

def get_new_access_token(app_id, app_secret):
	if app_id is None or app_secret is None:
		return None

	from core.wxapi.weixin_api import WeixinApiResponse
	
	weixin_response_json = _get_new_token_info(app_id, app_secret)
	if weixin_response_json is None:
		return None, None, None
	
	weixin_response = WeixinApiResponse(weixin_response_json)
	if weixin_response.is_failed():
		return None, None, weixin_response
	else:
		new_access_token = weixin_response_json[ACCESS_TOKEN_ATTR].strip()
		expires_span = weixin_response_json[ACCESS_TOKEN_EXPIRES_IN_ATTR]
		return new_access_token, expires_span, None