# -*- coding: utf-8 -*-

__author__ = "bert"

from models import *
from market_tools.prize.module_api import *
from weixin.message.material.models import News

from watchdog.utils import watchdog_warning, watchdog_error
from core.exceptionutil import full_stack, unicode_full_stack
from modules.member.models import *
from modules.member.integral import increase_member_integral
from market_tools.tools.coupon.util import consume_coupon

def check_channel_qrcode_ticket(ticket, user_profile):
	return True if ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id).count() > 0 else False

def create_channel_qrcode_has_memeber(user_profile, member, ticket, is_new_member):
	try:
		channel_qrcodes = ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id)
		print("channel_qrcodes: {}, ticket: {}, owner_id: {}".format(channel_qrcodes, ticket, user_profile.user_id))
		if channel_qrcodes.count() > 0:
			channel_qrcode = channel_qrcodes[0]

			if (is_new_member is False) and channel_qrcode.re_old_member == 0:
				return

			if ChannelQrcodeHasMember.objects.filter(channel_qrcode=channel_qrcode, member=member).count() == 0:
				ChannelQrcodeHasMember.objects.filter(member=member).delete()
				ChannelQrcodeHasMember.objects.create(channel_qrcode=channel_qrcode, member=member, is_new=is_new_member)
			else:
				return

			if member:
				prize_info = PrizeInfo.from_json(channel_qrcode.award_prize_info)
				award(prize_info, member, CHANNEL_QRCODE)

			try:
				if channel_qrcode.grade_id > 0:
					Member.update_member_grade(member.id, channel_qrcode.grade_id)
			except:
				notify_message = u"渠道扫描异常update_member_grade error, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)
	except:
		notify_message = u"渠道扫描异常create_channel_qrcode_has_memeber error, cause:\n{}".format(unicode_full_stack())
		watchdog_warning(notify_message)


def get_response_msg_info(ticket, user_profile):
	channel_qrcode_settings = ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id)
	if channel_qrcode_settings.count() > 0:
		channel_qrcode_setting = channel_qrcode_settings[0]

		if channel_qrcode_setting.reply_type == 0:
			return None, None
		elif channel_qrcode_setting.reply_type == 1:
			return 'text', channel_qrcode_setting.reply_detail
		elif channel_qrcode_setting.reply_type == 2:
			return 'news', channel_qrcode_setting.reply_material_id
		else:
			return None, None

########################################################################
# get_material_news_info: 返回消息
########################################################################
def get_material_news_info(material_id):
	try:
		material_id = int(material_id)
		news = list(News.objects.filter(material_id=material_id, is_active=True))
		return news
	except:
		notify_message = u"渠道扫描异常 get_material_news_info error, cause:\n{}".format(unicode_full_stack())
		watchdog_warning(notify_message)
		return None


#新渠道扫码
def check_new_channel_qrcode_ticket(ticket, user_profile):
	return True if MemberChannelQrcode.objects.filter(ticket=ticket, owner_id=user_profile.user_id).count() > 0 else False

def create_new_channel_qrcode_has_memeber(user_profile, member, ticket, is_new_member):
	try:
		new_channel_qrcodes = MemberChannelQrcode.objects.filter(ticket=ticket, owner_id=user_profile.user_id)
		print("new_channel_qrcodes: {}, ticket: {}, owner_id: {}".format(new_channel_qrcodes, ticket, user_profile.user_id))
		if new_channel_qrcodes.count() > 0:
			new_channel_qrcode = new_channel_qrcodes[0]
			qrcode_award = MemberChannelQrcodeAwardContent.objects.get(owner_id=user_profile.user_id)

			if MemberChannelQrcodeHasMember.objects.filter(member_channel_qrcode=new_channel_qrcode, member=member).count() == 0:
				MemberChannelQrcodeHasMember.objects.create(member_channel_qrcode=new_channel_qrcode, member=member, is_new=is_new_member)
			else:
				return

			if member:
				_add_award_to_member(user_profile,
					qrcode_award.scanner_award_type,
					qrcode_award.scanner_award_content,
					member,
					CHANNEL_QRCODE
					)
				_add_award_to_member(user_profile,
					qrcode_award.share_award_type,
					qrcode_award.share_award_content,
					new_channel_qrcode.member,
					BRING_NEW_CUSTOMER_VIA_QRCODE
					)

	except:
		notify_message = u"渠道扫描异常create_channel_qrcode_has_memeber error, cause:\n{}".format(unicode_full_stack())
		watchdog_warning(notify_message)

def _add_award_to_member(user_profile, award_type, award_content, member, integral_type):
	if award_type:
		if award_content == AWARD_COUPON:
			consume_coupon(user_profile.user.id, award_content, member.id)
		elif award_content == AWARD_INTEGRAL:
			try:
				increase_member_integral(member, award_content, integral_type)
			except:
				notify_msg = u"新推广扫码-微信会员二维码扫描增加积分失败1 cause:\n{}".format(unicode_full_stack())
				watchdog_fatal(notify_msg)