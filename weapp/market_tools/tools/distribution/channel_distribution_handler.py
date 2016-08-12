# -*- coding: utf-8 -*-

import json
from weixin.message.handler.message_handler import MessageHandler
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember
from modules.member.models import MemberHasTag
from modules.member.integral import increase_member_integral
from market_tools.tools.coupon.util import consume_coupon

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
				# 发放优惠券
				award_prize_info = json.loads(qrcode[0].award_prize_info)
				if award_prize_info['type'] == u"优惠券":
					coupon_id = award_prize_info['id']  # 优惠券id
					consume_coupon(qrcode[0].owner.id, coupon_id, member.id)
				elif award_prize_info['type'] == u"积分":
					# 发放积分
					award = award_prize_info['id']  # 扫码奖励积分
					increase_member_integral(member, award, u'推荐扫码奖励')
			else:
				return None
		return None
