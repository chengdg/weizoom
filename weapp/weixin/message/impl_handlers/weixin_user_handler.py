# -*- coding: utf-8 -*-

__author__ = 'chuter'

from weixin.message.handler.message_handler import MessageHandler

from weixin.user.models import WeixinUser, get_token_for

from utils.string_util import byte_to_hex

"""
处理微信消息中的微信用户，如果该用户信息在系统库中还不存在
则进行创建相应记录，保证后续的处理时对应的微信账号肯定是存在的
"""

class WeixinUserHandler(MessageHandler):

	def handle(self, context, is_from_simulator=False):
		user_profile = context.user_profile
		weixin_user = self._handle_weixin_user(user_profile,
											   context.message.fromUserName,
											   is_from_simulator)
		context.weixin_user = weixin_user
		return None

	def _handle_weixin_user(self, user_profile, weixin_user_name, is_from_simulator):
		weixin_account_token = get_token_for(user_profile.webapp_id, weixin_user_name, is_from_simulator)
		existed_weixin_users = WeixinUser.objects.filter(username=weixin_user_name)

		if existed_weixin_users.count() == 0: #不存在时创建
			weixin_user_icon = ''
			weixin_user_nick_name = ''
			if weixin_user_name == 'zhouxun':
				weixin_user_nick_name = u'周迅'
				weixin_user_icon = '/static/img/zhouxun_43.jpg'
			elif weixin_user_name == 'yangmi':
				weixin_user_nick_name = u'杨幂'
				weixin_user_icon = '/static/img/yangmi_43.jpg'
			else:
				pass
			try:
				return WeixinUser.objects.create(
					username = weixin_user_name, 
					webapp_id = user_profile.webapp_id, 
					nick_name = byte_to_hex(weixin_user_nick_name), 
					weixin_user_icon = weixin_user_icon
				)
			except:
				try:
					return WeixinUser.objects.get(username=weixin_user_name)
				except:
					return WeixinUser.objects.create(
						username = weixin_user_name, 
						webapp_id = user_profile.webapp_id, 
						nick_name = byte_to_hex(weixin_user_nick_name), 
						weixin_user_icon = weixin_user_icon
						)
				
		else:
			return existed_weixin_users[0]