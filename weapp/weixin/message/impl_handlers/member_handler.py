# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf import settings

from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN

from weixin.message.handler.message_handler import MessageHandler
from weixin.user.models import get_token_for

from core.exceptionutil import unicode_full_stack

from modules.member.models import *
from modules.member.integral import increase_for_be_member_first
from modules.member.util import (get_member_by_binded_social_account, 
	create_member_by_social_account, create_social_account)

from watchdog.utils import watchdog_error, watchdog_fatal

"""
根据消息创建会员

如果用户对应的会员不存在则进行创建，该Handler必须置于
WeixinUserHandler之后
"""
class MemberHandler(MessageHandler):

	def handle(self, context, is_from_simulator=False):
		''' comment for preview
		if settings.MODE == 'deploy' and is_from_simulator:
			return None
		'''
			
		user_profile = context.user_profile
		weixin_user = context.weixin_user
		context.member = self._handle_member(user_profile, weixin_user, is_from_simulator)

		return None

	def _create_webapp_user(self, member):
		try:
			if WebAppUser.objects.filter(token = member.token, webapp_id = member.webapp_id, member_id = member.id).count() == 0:
				WebAppUser.objects.create(
					token = member.token,
					webapp_id = member.webapp_id,
					member_id = member.id
					)
		except:
			pass

	def __is_test_weixinuser(self, weixin_user_name):
		if settings.MODE == 'develop':
			return False
		else:
			return weixin_user_name.startswith('pc-weixin-user') or\
				weixin_user_name in ('weizoom', 'zhouxun', 'yangmi') or\
				len(weixin_user_name) < 16

	def _handle_member(self, user_profile, weixin_user, is_from_simulator):
		#是否已经存在会员信息，如果否则进行创建
		weixin_user_name = weixin_user.username
		token = get_token_for(user_profile.webapp_id, weixin_user_name, is_from_simulator)
		
		is_for_test = self.__is_test_weixinuser(weixin_user_name)

		social_accounts = SocialAccount.objects.filter(token=token)
		if social_accounts.count() > 0:
			social_account = social_accounts[0]
		else:
			social_account = create_social_account(user_profile.webapp_id, weixin_user_name, token, SOCIAL_PLATFORM_WEIXIN, is_for_test)

		member = get_member_by_binded_social_account(social_account)
		if member is None:
			#创建会员信息
			try:
				member = create_member_by_social_account(user_profile, social_account)
				#之后创建对应的webappuser
				# if MemberHasSocialAccount.objects.filter(account=social_account, member=member).count() == 0:
				# 	MemberHasSocialAccount.objects.create(account=social_account, member=member, webapp_id=social_account.webapp_id)
				self._create_webapp_user(member)
			except:
				notify_message = u"MemberHandler中创建会员信息失败，社交账户信息:('openid':{}), cause:\n{}".format(
					social_account.openid, unicode_full_stack())
				watchdog_fatal(notify_message)

			if member and hasattr(member, 'is_new') and member.is_new:
				try:
					increase_for_be_member_first(user_profile, member)
					member.is_new = True
				except:
					notify_message = u"MemberHandler中创建会员后增加积分失败，会员id:{}, cause:\n{}".format(
							member.id, unicode_full_stack())
					watchdog_error(notify_message)

		else:
			member.is_subscribed = True
			#member.save()
			#add by bert at 20150323  增加异步任务更新会员关注
			member.is_new = False

		if member and (hasattr(member, 'is_new') is False):
			member.is_new = False

		return member