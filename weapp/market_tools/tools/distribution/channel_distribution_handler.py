# -*- coding: utf-8 -*-

from weixin.message.handler.message_handler import MessageHandler
from apps.customerized_apps.rebate import models as rebate_models
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember


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

		# #检查是否返利活动中有这个
		# if rebate_models.Rebate.objects(ticket=ticket, status=rebate_models.STATUS_RUNNING):
		# 	print 'apps.Rebate has the same ticket: %s, so let rebate handler handle it' % ticket
		# 	return None

		# 一 将信息添加到ChannelDistributionQrcodeHasMember中
		# 二 将扫码的会员添加到新分组中
		channel_distribution_qrcode_has_member = ChannelDistributionQrcodeHasMember.objects.filter(member_id=member)
		if channel_distribution_qrcode_has_member:  # 如果这个会员已经绑定到别人的二维码下:
			return None
		else:
			qrcode = ChannelDistributionQrcodeSettings.objects.filter(ticket=ticket)  # 得到ticket绑定的二维码数据
			if qrcode:
				ChannelDistributionQrcodeHasMember.objects.create(
					channel_qrcode_id = qrcode[0].id,
					member_id = member,
				)

			else:
				return None


		return None