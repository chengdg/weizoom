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

from util import *
"""
"""
class SendMassMessageResultHandler(MessageHandler):
	
	def name(self):
		return "SendMassMessageResultHandler handler"

	def handle(self, context, is_from_simulator=False):
		message = context.message
		if message.is_optimization_message:
			print 'SendMassMessageResultHandler only handle is_optimization_message = False'
			return None

		username = message.fromUserName
		user_profile = context.user_profile

		if not hasattr(context.message, 'event'):
			return None

		if user_profile and hasattr(context.message, 'msgId') and context.message.msgId != '' and context.message.msgId != None and hasattr(context.message, 'sentCount') and context.message.sentCount != '' and context.message.sentCount != None:
			update_send_mass_msg_log(
									user_profile, 
									context.message.msgId,
									context.message.sentCount,
									context.message.totalCount,
									context.message.filterCount,
									context.message.errorCount,
									context.message.status
									)
		
		return None

