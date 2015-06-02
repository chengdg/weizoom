# -*- coding: utf-8 -*-

__author__ = 'bert'

from weixin.message.handler.keyword_handler import *
import time
from datetime import timedelta, datetime, date
import os
import json
import hashlib
import MySQLdb

from BeautifulSoup import BeautifulSoup

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.test import Client
from django.db.models import Q

from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.message.handler.event_handler import *
from weixin.user.models import get_token_for
from core.exceptionutil import full_stack, unicode_full_stack
from util import *
"""
"""
class UpdateMemberGroupHandler(MessageHandler):
	
	def name(self):
		return "UpdateMemberGroupHandler handler"


	def handle(self, context, is_from_simulator=False):
		message = context.message
		username = message.fromUserName
		user_profile = context.user_profile
		#如果是微信服务器推送的消息 则不进行更新分组
		if hasattr(context.message, 'sentCount') and hasattr(context.message, 'totalCount'):
			return None
		
		member = context.member
		try:
			if member and member.is_subscribed and member.is_for_test is False:
				openid = member.member_open_id
				if openid:
					all_groups = get_all_group(user_profile)
					member_group_id = get_member_group_id(user_profile, openid)
					create_relation_in_weapp(member, all_groups, member_group_id)
		except:
			notify_message = u"更新会员分组信息失败，社交账户信息: cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_message)

		return None
