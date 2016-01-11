# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings
from django.contrib.auth.models import Group, User
from core.exceptionutil import full_stack, unicode_full_stack
from core.sendmail import sendmail
from watchdog.utils import watchdog_warning, watchdog_error
from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken
from models import *
from utils import cache_util

def get_binding_weixin_mpuser(user):
	if isinstance(user, User):
		mpusers = WeixinMpUser.objects.filter(owner=user)
	else:
		mpusers = WeixinMpUser.objects.filter(owner_id=user)
	if mpusers.count() > 0:
		return mpusers[0]
	else:
		return None

def get_mpuser_accesstoken(mpuser):
	access_tokens = WeixinMpUserAccessToken.objects.filter(mpuser=mpuser)
	if access_tokens.count() > 0:
		return access_tokens[0]
	else:
		return None


def _send_email(user, emails, content_described, content):
	"""
	发送邮件
	:param user:
	:param emails:
	:param content_described:
	:param content:
	:return:
	"""
	try:
		for email in emails.split('|'):
			if email.find('@') > -1:
				sendmail(email, content_described, content)
	except:
		notify_message = u"发送邮件失败user_id（{}）, cause:\n{}".format(user.id,unicode_full_stack())
		watchdog_warning(notify_message)
