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

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.message.handler.event_handler import *

from channel_qrcode_util import *


"""
"""
class ChannelQrcodeHandler(MessageHandler):

	def name(self):
		return "ChannelQrcodeHandler"

	def handle(self, context, is_from_simulator=False):
		message = context.message

		if message.is_optimization_message:
			print 'ChannelQrcodeHandler only handle is_optimization_message = true'
			return None

		username = message.fromUserName
		user_profile = context.user_profile
		member = context.member

		if not hasattr(context.message, 'event'):
			return None

		if not hasattr(context.message, 'ticket') or context.message.ticket is None:
			return None
		ticket = context.message.ticket

		if not hasattr(context.message, 'eventKey') or context.message.eventKey is None or ticket == '':
			return None

		if member and (hasattr(member, 'is_new') is False):
			member.is_new = False

		# if hasattr(context, 'is_member_qrcode') and context.is_member_qrcode is False:
		# 	return None

		if user_profile.user_id in [467,154] and \
			check_new_channel_qrcode_ticket(ticket, user_profile):
			if member.is_new:
				create_new_channel_qrcode_has_memeber(user_profile, context.member, ticket, member.is_new)
			return None

		if ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id).count() > 0:
			channel_qrcode = ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id)[0]
			create_channel_qrcode_has_memeber_restructure(channel_qrcode, user_profile, context.member, ticket, member.is_new)
			msg_type, detail = get_response_msg_info_restructure(channel_qrcode, user_profile)
			if msg_type != None:
				from_weixin_user = self._get_from_weixin_user(message)
				#token = self._get_token_for_weixin_user(user_profile, from_weixin_user, is_from_simulator)
				if msg_type == 'text' and detail:
					if is_from_simulator:
						return generator.get_text_response(username, message.toUserName, emotion.change_emotion_to_img(detail), username, user_profile)
					else:
						return generator.get_text_response(username, message.toUserName, detail, username, user_profile)
				if msg_type == 'news' and get_material_news_info(detail):
					news = get_material_news_info(detail)
					return generator.get_news_response(username, message.toUserName, news, username)
		# elif check_channel_qrcode_ticket(ticket, user_profile):
		# 	#if member.is_new:
		# 	create_channel_qrcode_has_memeber(user_profile, context.member, ticket, member.is_new)

		# 	msg_type, detail = get_response_msg_info(ticket, user_profile)

		# 	if msg_type != None:
		# 		from_weixin_user = self._get_from_weixin_user(message)
		# 		#token = self._get_token_for_weixin_user(user_profile, from_weixin_user, is_from_simulator)
		# 		if msg_type == 'text' and detail:
		# 			if is_from_simulator:
		# 				return generator.get_text_response(username, message.toUserName, emotion.change_emotion_to_img(detail), username, user_profile)
		# 			else:
		# 				return generator.get_text_response(username, message.toUserName, detail, username, user_profile)
		# 		if msg_type == 'news' and get_material_news_info(detail):
		# 			news = get_material_news_info(detail)
		# 			return generator.get_news_response(username, message.toUserName, news, username)

		return None

