# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, Permission
from django.db.models import F
from django.contrib.auth.models import User

import time

from market_tools.prize.models import Prize
from market_tools.tools.coupon import util as coupon_util

from watchdog.utils import watchdog_fatal, watchdog_error

from modules.member.models import Member, MemberGrade, BRING_NEW_CUSTOMER_VIA_QRCODE, SOURCE_MEMBER_QRCODE, MemberFollowRelation, NOT_SUBSCRIBED
from models import *
from modules.member.integral import increase_member_integral
from market_tools.tools.coupon.util import consume_coupon

from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi.weixin_api import *
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApi
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket
from datetime import datetime, timedelta

#############################################################################
#get_coupon_rules: 获取优惠券rule
#############################################################################
def get_coupon_rules(owner):
	return coupon_util.get_coupon_rules(owner)


#############################################################################
#get_all_grades_list: 获取会员等级
#############################################################################
def get_all_grades_list(request):
	webapp_id = request.user_profile.webapp_id
	return MemberGrade.get_all_grades_list(webapp_id)


def __get_qrcode(user_id):
	try:
		user = User.objects.get(id=user_id)
	except:
		notify_msg = u"微信会员二维码__get_qrcode errror :id={}cause:\n{}".format(user_id, unicode_full_stack())
		watchdog_error(notify_msg)
		return None, None

	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return None, None

	if mpuser_access_token is None:
		return None, None

	if mpuser_access_token.is_active:
		weixin_api = get_weixin_api(mpuser_access_token)
		try:
			ticket = None
			qrcode_ticket = weixin_api.create_qrcode_ticket(int(user.id))
			try:
				ticket = qrcode_ticket.ticket
			except:
				ticket = None

			#qcrod_info = weixin_api.get_qrcode(ticket)
			if ticket:
				return ticket, 2592000
			else:
				return None, None
		except:
			notify_msg = u"微信会员二维码__get_qrcode errror :id={}cause:\n{}".format(user_id, unicode_full_stack())
			watchdog_error(notify_msg, 'WEB', user_id)
			return None, None

	else:
		return None, None


###########################################################
#get_member_qrcode : 获取微站下的会员二维码
###########################################################
def get_member_qrcode(user_id, member_id):
	try:
		now_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
		viper_spreads = MemberQrcode.objects.filter(member_id=member_id, created_at__gte=now_date, is_active=1)
		if viper_spreads.count() > 0:
	 		return viper_spreads[0].ticket, viper_spreads[0].expired_second
		ticket, expired_second = __get_qrcode(user_id)
		if ticket:
			MemberQrcode.objects.create(owner_id=user_id, member_id=member_id, ticket=ticket, created_time=int(time.time()), expired_second=expired_second)
			return ticket, expired_second
		else:
			ticket, expired_second = __get_qrcode(user_id)
			MemberQrcode.objects.create(owner_id=user_id, member_id=member_id, ticket=ticket, created_time=int(time.time()), expired_second=expired_second)
			return ticket, expired_second
	except:
		return None, None
	# try:
	# 	from django.db import connection, transaction
	# 	cursor = connection.cursor()
	# 	cursor.execute('update market_tool_member_qrcode set expired_second = expired_second - (%d - created_time) where is_active = 1;' % (int(time.time())))
	# 	cursor.execute('update market_tool_member_qrcode set is_active = 0 where expired_second <= 0;')
	# 	transaction.commit_unless_managed()
	# except:
	# 	notify_msg = u"微信会员二维码get_member_qrcode execute sql errror cause:\n{}".format(unicode_full_stack())
	# 	watchdog_fatal(notify_msg)

	# try:
	# 	viper_spreads = MemberQrcode.objects.filter(member_id=member_id, expired_second__gt=850, is_active=1)
	# 	if viper_spreads.count() > 0:
	# 		return viper_spreads[0].ticket, viper_spreads[0].expired_second
	# 	else:
	# 		ticket, expired_second = __get_qrcode(user_id)
	# 		if ticket:
	# 			MemberQrcode.objects.create(owner_id=user_id, member_id=member_id, ticket=ticket, created_time=int(time.time()), expired_second=expired_second)
	# 			return ticket, expired_second
	# 		else:
	# 			return None, None
	# except:
	# 	notify_msg = u"微信会员二维码get_member_qrcode execute sql errror cause:\n{}".format(unicode_full_stack())
	# 	watchdog_fatal(notify_msg)
	# 	return None, None


###########################################################
#get_qcrod_url : 二维码url路径
###########################################################
weixin_qcrod_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s'
def get_qcrod_url(ticket):
	return 	weixin_qcrod_url % ticket


###########################################################
#check_member_qrcode_ticket : 检查是否是 会员二维码
###########################################################
# def check_member_qrcode_ticket(ticket):
# 	return


###########################################################
#update_member_qrcode_log : 二维码推广日志
###########################################################
def update_member_qrcode_log(user_profile, member, ticket):
	try:
		if MemberQrcode.objects.filter(ticket=ticket).count() > 0:
			member_qrcode =  MemberQrcode.objects.filter(ticket=ticket)[0]
			only_create_friend = False
			if hasattr(member, 'old_status') and member.old_status == NOT_SUBSCRIBED:
				only_create_friend = True
			if member and  member.is_new:
				if MemberQrcodeLog.objects.filter(member_id=member.id).count() == 0:

					if member_qrcode and MemberQrcodeLog.objects.filter(member_id=member.id).count() == 0:
						MemberQrcodeLog.objects.create(member_qrcode=member_qrcode,member_id=member.id)
						_add_award_to_member(user_profile, member, member_qrcode)
						#修改来源
						if not only_create_friend:
							_update_member_source(member)
						#建立关系
						_add_member_relation(member, member_qrcode.member, only_create_friend)
			return True
		else:
			return False
	except:
		notify_msg = u"微信会员二维码扫描增加积分失败1 cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_msg)
		return True


def _add_award_to_member(user_profile, member, member_qrcode):
	member_qrcode_setting = MemberQrcodeSettings.objects.filter(owner=user_profile.user)[0] if MemberQrcodeSettings.objects.filter(owner=user_profile.user).count() > 0 else None

	try:
		if member_qrcode_setting:
			#如果扫码用户数量超过限制的奖励次数，则不再奖励
			if member_qrcode_setting.is_limited:
				limit_log = MemberQrcodeLimitLog.objects.filter(belong_settings_id=member_qrcode_setting.id, owner_member_id=member_qrcode.member.id, created_at=datetime.now().date())
				if limit_log.count() > 0:
					limit_log = limit_log.first()
					if limit_log.count >= member_qrcode_setting.limit_chance:
						return
				else:
					limit_log = MemberQrcodeLimitLog.objects.create(
						belong_settings_id=member_qrcode_setting.id,
						owner_member_id=member_qrcode.member.id,
						created_at=datetime.now().date(),
						count = 0
					)
				#确认本次奖励，更新次数(本次优惠券或积分奖励失败也会扣掉次数)
				tmp_count = limit_log.count + 1
				limit_log.count=tmp_count
				limit_log.save()

			if member_qrcode_setting.award_member_type == AWARD_MEMBER_TYPE_ALL:
				award_contents = MemberQrcodeAwardContent.objects.filter(member_qrcode_settings=member_qrcode_setting)
				award_content = award_contents[0] if member_qrcode_setting.award_member_type == 1 and award_contents.count() > 0 else None
				if award_content:
					if award_content.award_type == AWARD_COUPON:
						# create_coupons(user_profile.user, award_content.award_content, 1, member_qrcode.member.id)
						consume_coupon(user_profile.user.id, award_content.award_content, member_qrcode.member.id)
					elif award_content.award_type == AWARD_INTEGRAL:
						try:
							increase_member_integral(member_qrcode.member,award_content.award_content, BRING_NEW_CUSTOMER_VIA_QRCODE, member)
						except:
							notify_msg = u"微信会员二维码扫描增加积分失败1 cause:\n{}".format(unicode_full_stack())
							watchdog_fatal(notify_msg)

			elif member_qrcode_setting.award_member_type == AWARD_MEMBER_TYPE_LEVEL:
				award_contents = MemberQrcodeAwardContent.objects.filter(member_qrcode_settings=member_qrcode_setting, member_level=member_qrcode.member.grade.id)
				if award_contents.count() > 0:
					award_content = award_contents[0]
					if award_content.award_type == AWARD_COUPON:
						# create_coupons(user_profile.user, award_content.award_content, 1, member_qrcode.member.id)
						consume_coupon(user_profile.user.id, award_content.award_content, member_qrcode.member.id)
					elif award_content.award_type == AWARD_INTEGRAL:
						try:
							increase_member_integral(member_qrcode.member,award_content.award_content, BRING_NEW_CUSTOMER_VIA_QRCODE, member)
						except:
							notify_msg = u"微信会员二维码扫描增加积分失败2 cause:\n{}".format(unicode_full_stack())
							watchdog_fatal(notify_msg)
	except:
		notify_msg = u"微信会员二维_add_award_to_member cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_msg)

def _update_member_source(member):
	try:
		if member.source == -1:
			Member.objects.filter(id=member.id).update(source=SOURCE_MEMBER_QRCODE)
	except:
		notify_msg = u"微信会员二维码扫描修改会员来源member_id :{} cause:\n{}".format(member.id, unicode_full_stack())
		watchdog_fatal(notify_msg)


def _add_member_relation(new_member, old_member, only_create_friend=False):
	if only_create_friend and MemberFollowRelation.objects.filter(member_id=new_member.id, follower_member_id=old_member.id).count() == 0:
		MemberFollowRelation.objects.create(member_id=new_member.id, follower_member_id=old_member.id)
		MemberFollowRelation.objects.create(member_id=old_member.id, follower_member_id=new_member.id)
		Member.objects.filter(id=new_member.id).update(friend_count = F('friend_count') + 1)
		Member.objects.filter(id=old_member.id).update(friend_count = F('friend_count') + 1)
	else:
		try:
			if MemberFollowRelation.objects.filter(member_id=new_member.id, follower_member_id=old_member.id).count() == 0:
				is_fans = False if MemberFollowRelation.objects.filter(follower_member_id=new_member.id,is_fans=True).count() > 0 else True
				MemberFollowRelation.objects.create(member_id=new_member.id, follower_member_id=old_member.id)
				MemberFollowRelation.objects.create(member_id=old_member.id, follower_member_id=new_member.id, is_fans=is_fans)
				Member.objects.filter(id=new_member.id).update(friend_count = F('friend_count') + 1)
				Member.objects.filter(id=old_member.id).update(friend_count = F('friend_count') + 1)
			# from django.db import connection, transaction
			# cursor = connection.cursor()
			# cursor.execute('update member_member set friend_count=friend_count+1 where id in (%d,%d)' % (new_member.id, old_member.id))
			# watchdog_error('update member_member set friend_count=friend_count+1 where id in (%d,%d)' % (new_member.id, old_member.id))
			# transaction.commit_unless_managed()
			# Member.update_factor(old_member)
			# Member.update_factor(new_member)
		except:
			notify_msg = u"微信会员二维码扫描建立粉丝关系new_member_id :{}, follower_member_id:{} cause:\n{}".format(new_member.id, old_member.id, unicode_full_stack())
			watchdog_fatal(notify_msg)
