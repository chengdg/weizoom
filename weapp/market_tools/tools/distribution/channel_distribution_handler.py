# -*- coding: utf-8 -*-

from weixin.message.handler.message_handler import MessageHandler
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember
from modules.member.models import MemberHasTag

class ChannelDistributionQrcodeHandler(MessageHandler):

	def name(self):
		return "ChannelDistributionQrcodeHandler"

	def handle(self, context, is_from_simulator=False):
		message = context.message

		if message.is_optimization_message:
			print 'ChannelDistributionQrcodeHandler only handle is_optimization_message = true'
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

		#优化处理
		if hasattr(context, 'is_member_qrcode') and (context.is_member_qrcode is True):
			return None

		# 一 将信息添加到ChannelDistributionQrcodeHasMember中
		# 二 将扫码的会员添加到新分组中
		channel_distribution_qrcode_has_member = ChannelDistributionQrcodeHasMember.objects.filter(member_id=member.id)
		if channel_distribution_qrcode_has_member:  # 如果这个会员已经绑定到别人的二维码下:
			return None
		else:
			qrcode = ChannelDistributionQrcodeSettings.objects.filter(ticket=ticket)  # 得到ticket绑定的二维码数据
			if qrcode:
				ChannelDistributionQrcodeHasMember.objects.create(
					channel_qrcode_id = qrcode[0].id,
					member_id = member.id,
				)
				# 得到需要绑定的member分组
				group_id = qrcode[0].group_id
				# 添加到得到的分组
				MemberHasTag.add_tag_member_relation(member, [group_id])

			else:
				return None
		return None