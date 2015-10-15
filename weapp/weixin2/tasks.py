# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import

import time
from django.conf import settings
from django.db.models import F

from core.exceptionutil import unicode_full_stack

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from account import models as account_models
from modules.member.models import *
from datetime import datetime

from celery import task

from member.util import *
	
@task(bind=True, max_retries=5)
def task_send_mass_message(self, webapp_id, log_id, message_type, content, is_from_fans_list, group_id, member_ids):
	#try:
	"""
	task 群发消息
	"""
	user_profile = account_models.UserProfile.objects.get(webapp_id=webapp_id)
	openid_list = []
	if is_from_fans_list and member_ids:
		members = Member.objects.filter(webapp_id = webapp_id, is_subscribed = True, is_for_test = False, id__in = member_ids)
		for member in members:
			openid_list.append(member.member_open_id)
	else:
		if group_id == -1:
			openid_list = get_openid_list_by_webapp_id(webapp_id)
		else:
			openid_list = get_openid_list(group_id)
	if message_type == MESSAGE_TYPE_TEXT:
		result = send_mass_text_message_with_openid_list(user_profile, openid_list, content, log_id)
	else:
		result = send_mass_news_message_with_openid_list(user_profile, openid_list, material_id, log_id)

	if result is False:
		raise self.retry()
	# except:
	# 	notify_message = u"task task_send_mass_message, cause:\n{}".format(unicode_full_stack())
	# 	watchdog_error(notify_message)
	# 	raise self.retry()

