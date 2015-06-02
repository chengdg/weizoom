#coding:utf8
"""@package services.start_promotion_service.tasks
start_promotion_service 的Celery task实现

"""
import json
import urllib2

from django.conf import settings
from core.exceptionutil import unicode_full_stack
from datetime import datetime

from mall.promotion import models as promotion_models
from mall import models as mall_models

from celery import task
# from utils import cache_util

from datetime import datetime, timedelta

from core.exceptionutil import unicode_full_stack

# from settings import *

from weixin.user.models import WeixinMpUserAccessToken

from watchdog.utils import watchdog_fatal, watchdog_notice, watchdog_warning

MaxRetryTimes = 5
WATCHDOG_TYPE = 'ACCESSTOKEN_UPDATE_SERVICE'
WEIXIN_ACCESS_TOKEN_UPDATE_URL_TMPL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
ACCESS_TOKEN_ATTR = 'access_token'
ACCESS_TOKEN_EXPIRES_IN_ATTR = 'expires_in'

UPDATE_TIME_SPAN_SECONDS = 5 # 更新间隔为5分钟


@task
def update_mp_token(request0, args):
	"""
	将promotion的状态改为"进行中"的服务

	@param request 无用，为了兼容
	@param args dict类型
	"""
	print 'start service @%s', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	need_to_update_access_token_users = _get_access_tokens_need_to_update()

	for access_token in need_to_update_access_token_users:
		try:
			#print 'update token username',access_token.mpuser.username
			_update_mpuser_access_token(access_token)
		except:
			mpuser_owner = access_token.mpuser.owner
			notify_message = u"failed to update access_token for user:{}, cause:\n{}".format(access_token.mpuser.username, unicode_full_stack())
			watchdog_fatal(notify_message)
			print notify_message
	return "OK"

def _get_access_tokens_need_to_update():
	"""获取当前access_token已经失效的，或者当前有效，但会在下一次更新之前就会失效的进行更新"""
	invalid_access_tokens = WeixinMpUserAccessToken.objects.filter(is_active=False)

	next_update_time = datetime.now() + timedelta(minutes=UPDATE_TIME_SPAN_SECONDS)
	to_expire_access_token = WeixinMpUserAccessToken.objects.filter(expire_time__lt=next_update_time, is_active=True)

	need_to_update_access_tokens = []
	if invalid_access_tokens:
		need_to_update_access_tokens.extend(invalid_access_tokens)
	if to_expire_access_token:
		need_to_update_access_tokens.extend(to_expire_access_token)

	return [to_update_access_token for to_update_access_token in need_to_update_access_tokens \
			if _is_access_token_can_update(to_update_access_token)]

def _is_access_token_can_update(access_token):
	assert (access_token)
	return access_token.app_id and access_token.app_secret


def _update_mpuser_access_token( access_token):
	assert (access_token)

	new_token_info = _get_new_token_info(access_token)
	if None == new_token_info:
		return

	if not new_token_info.has_key(ACCESS_TOKEN_ATTR):
		watchdog_warning(u"failed to update access token for user({}), response:\n{}".format(access_token.mpuser.username, json.dumps(new_token_info)))
	else:
		new_access_token = new_token_info[ACCESS_TOKEN_ATTR].strip()
		expires_span = new_token_info[ACCESS_TOKEN_EXPIRES_IN_ATTR]

		_update_access_token_record(access_token, new_access_token, expires_span)

def _get_new_token_info(access_token):
	assert (access_token)

	update_url = WEIXIN_ACCESS_TOKEN_UPDATE_URL_TMPL.format(access_token.app_id, access_token.app_secret)

	update_response_data = None
	try:
		update_response_data = _get_access_token_update_response(update_url)
	except:
		watchdog_notice(u"failed to update access token for user({}), cause:\n{}".format(access_token.mpuser.username, unicode_full_stack()))
		for retry_time in xrange(MaxRetryTimes):
			try:
				update_response_data = _get_access_token_update_response(update_url)
			except:
				watchdog_notice(u"failed to update access token for user({}), cause:\n{}".format(access_token.mpuser.username, unicode_full_stack()))

	return update_response_data

def _get_access_token_update_response(update_url):
	assert (update_url)

	return _decode_json_str(urllib2.urlopen(update_url).read())

def _decode_json_str(str):
	assert (str)

	return json.loads(str)

def _update_access_token_record(access_token, new_access_token, expires_span):
	assert (access_token and new_access_token)

	next_expire_time = datetime.now() + timedelta(seconds=expires_span)
	access_token.expire_time = next_expire_time
	access_token.access_token = new_access_token
	access_token.is_active = True

	access_token.save()

