# -*- coding: utf-8 -*-

__author__ = 'chuter'

from weixin.user.models import get_token_for
from django.conf import settings

from weixin.user.models import WeixinUser
from weixin.message.qa.models import *

from core import emotion
from weixin.message import generator

from django.conf import settings

EMPTY_RESPONSE_CONTENT = ''

class MessageHandler(object):
	"""
	给定微信push过来的消息处理的上下文环境进行消息的处理实现:
	如果不对消息进行处理直接返回None。如果要进行消息回复，返回
	正确的响应(HttpResponse)。如果不需要进行回复，只在server端
	针对用户的输入进行相应操作（例如统计等），则返回None。
	"""

	def handle(self, context, is_from_simulator=False):
		raise NotImplementedError

	def _get_token_for_weixin_user(self, user_profile, weixin_user_name, is_from_simulator):
		if is_from_simulator:
			if 'develop' == settings.MODE:
				token = get_token_for(user_profile.webapp_id, weixin_user_name)
			else:
				token = ''
		else:
			token = get_token_for(user_profile.webapp_id, weixin_user_name)

		return token

	def _get_from_weixin_user(self, message):
		return WeixinUser.objects.get(username=message.fromUserName)

	def _build_response_to_weixin_user(self, user_profile, message, response_rule, is_from_simulator):
		if settings.IS_MESSAGE_OPTIMIZATION:
			return self._build_optimization_response(user_profile, message, response_rule, is_from_simulator)
		else:
			return self._build_not_optimization_response(user_profile, message, response_rule, is_from_simulator)

	
	def _build_optimization_response(self, user_profile, message, response_rule, is_from_simulator):
		#from_weixin_user = self._get_from_weixin_user(message)
		#token = self._get_token_for_weixin_user(user_profile, from_weixin_user.username, is_from_simulator)

		response = None

		if response_rule.is_news_type:
			response = generator.get_news_response(message.fromUserName, message.toUserName, response_rule.newses, message.fromUserName)
		elif response_rule.type == TEXT_TYPE or response_rule.type == MENU_TYPE:
			if is_from_simulator:
				response = generator.get_text_response(message.fromUserName, message.toUserName, emotion.change_emotion_to_img(response_rule.answer), message.fromUserName, user_profile)
			else:
				response = generator.get_text_response(message.fromUserName, message.toUserName, response_rule.answer, message.fromUserName, user_profile)
		elif response_rule.type == FOLLOW_TYPE:
			if response_rule.material_id > 0:
				response = generator.get_news_response(message.fromUserName, message.toUserName, response_rule.newses, message.fromUserName)
			else:
				if is_from_simulator:
					response = generator.get_text_response(message.fromUserName, message.toUserName, emotion.change_emotion_to_img(response_rule.answer), message.fromUserName, user_profile)
				else:
					response = generator.get_text_response(message.fromUserName, message.toUserName, response_rule.answer, message.fromUserName, user_profile)
		
		return response


	def _build_not_optimization_response(self, user_profile, message, response_rule, is_from_simulator):
		from_weixin_user = self._get_from_weixin_user(message)
		token = self._get_token_for_weixin_user(user_profile, from_weixin_user.username, is_from_simulator)

		response = None

		if response_rule.is_news_type:
			response = generator.get_news_response(from_weixin_user.username, message.toUserName, response_rule.newses, token)
		elif response_rule.type == TEXT_TYPE or response_rule.type == MENU_TYPE:
			if is_from_simulator:
				response = generator.get_text_response(from_weixin_user.username, message.toUserName, emotion.change_emotion_to_img(response_rule.answer), token, user_profile)
			else:
				response = generator.get_text_response(from_weixin_user.username, message.toUserName, response_rule.answer, token, user_profile)
		elif response_rule.type == FOLLOW_TYPE:
			if response_rule.material_id > 0:
				response = generator.get_news_response(from_weixin_user.username, message.toUserName, response_rule.newses, token)
			else:
				if is_from_simulator:
					response = generator.get_text_response(from_weixin_user.username, message.toUserName, emotion.change_emotion_to_img(response_rule.answer), token, user_profile)
				else:
					response = generator.get_text_response(from_weixin_user.username, message.toUserName, response_rule.answer, token, user_profile)
		
		return response


	def _process_recorde_message(self, context, response_rule, from_weixin_user, is_from_simulator):
		new_context = {}
		new_context['member_id'] = context.member.id if context.member else -1
		new_context['message'] = context.message.__dict__ if context.message else None
		new_context['user_profile_id'] = context.user_profile.id if context.user_profile else None
		
		request = context.request
		post = {}
		post.update(request.POST)
		current_request_dict = {
			"POST":post
		}

		new_context['response_rule_id'] = response_rule.id if response_rule else -1
		#new_context['from_weixin_user_id'] = from_weixin_user.id if from_weixin_user else -1
		new_context['from_user_name'] = context.message.fromUserName
		
		new_context['is_from_simulator'] = is_from_simulator
		new_context['request'] = current_request_dict

		from weixin.message.message_handler.tasks import recorde_message, _recorde_message
		# if settings.TASKQUEUE_ENABLED:
		#增加response_rule参数，duhao 2015-04-30
		new_context['response_rule'] = response_rule.format_to_dict() if response_rule else None
		recorde_message.delay(new_context)
