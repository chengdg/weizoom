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
from mall.promotion import models as promotion_models
from django.db.models import F, Q

def check_channel_qrcode_ticket(ticket, user_profile):
	return True if ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id).count() > 0 else False

def create_channel_qrcode_has_memeber(user_profile, member, ticket, is_new_member):
	try:
		channel_qrcodes = ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id)
		print("channel_qrcodes: {}, ticket: {}, owner_id: {}".format(channel_qrcodes, ticket, user_profile.user_id))
		if channel_qrcodes.count() > 0:
			channel_qrcode = channel_qrcodes[0]

			if channel_qrcode.bing_member_id == member.id:
				return

			if (is_new_member is False) and channel_qrcode.re_old_member == 0:
				return

			if ChannelQrcodeHasMember.objects.filter(channel_qrcode=channel_qrcode, member=member).count() == 0:
				ChannelQrcodeHasMember.objects.filter(member=member).delete()
				ChannelQrcodeHasMember.objects.create(channel_qrcode=channel_qrcode, member=member, is_new=is_new_member)
			else:
				return

			#如果没有会员扫该二维码的记录信息，创建记录并发奖，否则不进行操作
			if ChannelQrcodeToMemberLog.objects.filter(channel_qrcode=channel_qrcode, member=member).count() == 0:
				if member:
					prize_info = PrizeInfo.from_json(channel_qrcode.award_prize_info)
					award(prize_info, member, CHANNEL_QRCODE)
				try:
					ChannelQrcodeToMemberLog.objects.create(channel_qrcode=channel_qrcode, member=member)
				except:
					pass
			try:
				if channel_qrcode.grade_id > 0:
					# updated by zhu tianqi,修改为会员等级高于目标等级时不降级，member_id->member
					Member.update_member_grade(member, channel_qrcode.grade_id)
				if channel_qrcode.tag_id > 0:
					MemberHasTag.add_tag_member_relation(member, [channel_qrcode.tag_id])
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
		print '==========999999999999=========='
		new_channel_qrcodes = MemberChannelQrcode.objects.filter(ticket=ticket, owner_id=user_profile.user_id)
		if new_channel_qrcodes.count() > 0:
			new_channel_qrcode = new_channel_qrcodes[0]
			#用户自己扫自己的码直接返回
			if new_channel_qrcode.member_id == member.id:
				return
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
		if award_type == AWARD_COUPON:
			consume_coupon(user_profile.user.id, award_content, member.id)
		elif award_type == AWARD_INTEGRAL:
			try:
				increase_member_integral(member, award_content, integral_type)
			except:
				notify_msg = u"新推广扫码-微信会员二维码扫描增加积分失败1 cause:\n{}".format(unicode_full_stack())
				watchdog_fatal(notify_msg)



def create_channel_qrcode_has_memeber_restructure(channel_qrcode, user_profile, member, ticket, is_new_member):
	try:
		print '=====33333333333333====='
		if channel_qrcode.bing_member_id == member.id:
			return

		# qrcode_award = MemberChannelQrcodeAwardContent.objects.get(owner_id=user_profile.user_id)
		# award_type = qrcode_award.scanner_award_type
		# award_content = qrcode_award.scanner_award_content
		# if award_type == AWARD_COUPON:
		# 	coupon_id = award_content
		# else:
		# 	coupon_id = ''
		print channel_qrcode,'==============channel_qrcode========='
		print member.id,'==============member.id========='
		award_prize_info = json.loads(channel_qrcode.award_prize_info)
		award_type = award_prize_info['type']
		if award_type == u'优惠券':
			coupon_id = str(award_prize_info['id'])
		else:
			coupon_id = ''
		print coupon_id,'==========coupon_id============'
		print is_new_member,'==========is_new_member============'
		print channel_qrcode.re_old_member,'=========channel_qrcode.re_old_member========='
		log = ChannelQrcodeToMemberLog.objects.filter(channel_qrcode=channel_qrcode, member=member)
		if log.count() > 0:
			coupon_ids_list = log.first().coupon_ids.split(',')
			coupon_ids_list = [] if coupon_ids_list[0] == '' else coupon_ids_list
		else:
			coupon_ids_list = []
		print coupon_ids_list,'==========coupon_ids_list==========='
		if (is_new_member is False) and channel_qrcode.re_old_member == 0:
			print '=====444444444444====='
			if not coupon_id or (coupon_id in coupon_ids_list):
				print '=====5555555555555====='
				return

		if ChannelQrcodeHasMember.objects.filter(channel_qrcode=channel_qrcode, member=member).count() == 0:
			ChannelQrcodeHasMember.objects.filter(member=member).delete()
			ChannelQrcodeHasMember.objects.create(channel_qrcode=channel_qrcode, member=member, is_new=is_new_member)
		else:
			try:
				# if channel_qrcode.grade_id > 0:
				# 	# updated by zhu tianqi,修改为会员等级高于目标等级时不降级，member_id->member
				# 	Member.update_member_grade(member, channel_qrcode.grade_id)
				if channel_qrcode.tag_id > 0:
					MemberHasTag.add_tag_member_relation(member, [channel_qrcode.tag_id])
			except:
				notify_message = u"渠道扫描异常update_member_grade error, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)

			if coupon_id and (coupon_id in coupon_ids_list):
				print '=========0000000========'
				return

		if member:
			prize_info = PrizeInfo.from_json(channel_qrcode.award_prize_info)
			award(prize_info, member, CHANNEL_QRCODE)

		if log.count() == 0:
			try:
				print '=====6666666666666====='
				ChannelQrcodeToMemberLog.objects.create(channel_qrcode=channel_qrcode, member=member, coupon_ids=coupon_id)
			except Exception,e:
				print e,'======create log==========='
				pass
		else:
			print '==========777777777777=========='
			if coupon_id:
				member_log = log.first()
				cur_coupon_ids = member_log.coupon_ids.split(',')
				cur_coupon_ids.append(coupon_id)
				member_log.coupon_ids = ','.join(cur_coupon_ids)
				member_log.save()

		try:
			if channel_qrcode.grade_id > 0:
				# updated by zhu tianqi,修改为会员等级高于目标等级时不降级，member_id->member
				Member.update_member_grade(member, channel_qrcode.grade_id)
			if channel_qrcode.tag_id > 0:
				MemberHasTag.add_tag_member_relation(member, [channel_qrcode.tag_id])
				if MemberHasTag.objects.filter(member=member).count() > 1:
					MemberHasTag.objects.filter(member=member, member_tag__name="未分组").delete()
		except:
			notify_message = u"渠道扫描异常update_member_grade error, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(notify_message)
	except Exception,e:
		print e,'-------------------'
		notify_message = u"渠道扫描异常create_channel_qrcode_has_memeber error, cause:\n{}".format(unicode_full_stack())
		watchdog_warning(notify_message)

def get_response_msg_info_restructure(channel_qrcode_setting, user_profile):
	if channel_qrcode_setting.reply_type == 0:
		return None, None
	elif channel_qrcode_setting.reply_type == 1:
		return 'text', channel_qrcode_setting.reply_detail
	elif channel_qrcode_setting.reply_type == 2:
		return 'news', channel_qrcode_setting.reply_material_id
	else:
		return None, None