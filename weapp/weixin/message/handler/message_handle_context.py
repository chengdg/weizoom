# -*- coding: utf-8 -*-

__author__ = 'chuter'

"""
微信消息处理的上下文，包含了当前正在处理的消息和当前用户信息
"""

class MessageHandlingContext(object):
	def __init__(self, message, xml_message, user_profile, request=None):
		if None == user_profile:
			raise ValueError('user_profile can not be None')

		if None == message or None == xml_message:
			raise ValueError('message and xml_message can not be None neither')

		self.message = message
		self.xml_message = xml_message
		self.user_profile = user_profile
		self.request = request

		self.weixin_user = None
		self.member = None
		self.should_process = True