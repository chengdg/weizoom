# -*- coding: utf-8 -*-

__author__ = 'bert'

from account.social_account.models import SocialAccount 
from core.exceptionutil import full_stack, unicode_full_stack
from watchdog.utils import watchdog_info, watchdog_error

from models import *

def get_member_by_id(member_id):
	if member_id is None:
		return None

	if not isinstance(member_id, int):
		return None

	members = Member.objects.filter(id=member_id)
	if members.count() > 0:
		return members[0]
	else:
		return None

def get_member_by_id_list(member_id_list):
	if member_id_list is None or len(member_id_list) == 0:
		return []

	if not isinstance(member_id_list, list):
		return []

	return list(Member.objects.filter(id__in=member_id_list))

def get_integral_detail(webapp_id):
	if IntegralStrategySttingsDetail.objects.filter(webapp_id=webapp_id).count() > 0:
		return IntegralStrategySttingsDetail.objects.filter(webapp_id=webapp_id)[0]
		

def get_integral_strategy_setting(webapp_id):
	if IntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() > 0:
		return IntegralStrategySttings.objects.filter(webapp_id=webapp_id)[0]
		
	return None
		
def get_scoial_account_by_webapp_user_id(webapp_user_id):
	try:
		webapp_user = WebAppUser.objects.get(id=webapp_user_id)
		if webapp_user.member_id != 0 and MemberHasSocialAccount.objects.filter(member_id=webapp_user.member_id).count() > 0:
			return MemberHasSocialAccount.objects.filter(member_id=webapp_user.member_id)[0].account
		elif webapp_user.father_id != 0:
			father_webapp_user = WebAppUser.objects.get(id=webapp_user.father_id)
			if father_webapp_user.member_id != 0 and MemberHasSocialAccount.objects.filter(member_id=father_webapp_user.member_id).count() > 0:
				return MemberHasSocialAccount.objects.filter(member_id=webapp_user.member_id)[0].account
		return None
	except:
		return None	

def is_member_for_buy_test(member_id):
	try:
		member = Member.objects.get(id=member_id)
		return member.is_for_buy_test
	except:
		return False

def get_social_account(webapp_user_id):
		try:
			webapp_user = WebAppUser.objects.get(id=webapp_user_id)
			if webapp_user.member_id == 0 and webapp_user.father_id != 0:
				webapp_user_father = WebAppUser.objects.get(id=webapp_user.father_id)
				if webapp_user_father.member_id and MemberHasSocialAccount.objects.filter(member_id=webapp_user_father.member_id).count() >0:
					return MemberHasSocialAccount.objects.filter(member_id=webapp_user_father.member_id)[0].account
			else:
				if webapp_user.member_id != 0:
					return MemberHasSocialAccount.objects.filter(member_id=webapp_user.member_id)[0].account
			return None
		except:
			error_msg = u"get_social_account:\n{}, {}".format(webapp_user_id, unicode_full_stack())
			watchdog_error(error_msg)
			return None

def get_openid_by(webapp_user_id):
	try:
		webapp_user = WebAppUser.objects.get(id=webapp_user_id)
		if webapp_user.member_id == 0 and webapp_user.father_id != 0:
			webapp_user_father = WebAppUser.objects.get(id=webapp_user.father_id)
			if webapp_user_father.member_id and MemberHasSocialAccount.objects.filter(member_id=webapp_user_father.member_id).count() >0:
				return MemberHasSocialAccount.objects.filter(member_id=webapp_user_father.member_id)[0].account.openid
		else:
			if webapp_user.member_id != 0:
				return MemberHasSocialAccount.objects.filter(member_id=webapp_user.member_id)[0].account.openid
		return None
	except:
		error_msg = u"get_openid_by，cause:\n{},{}".format(webapp_user_id, unicode_full_stack())
		watchdog_error(error_msg)
		return None
	
def get_member_by(webapp_user_id):
	try:
		webapp_user = WebAppUser.objects.get(id=webapp_user_id)
		if webapp_user.member_id == 0 and webapp_user.father_id != 0:
			webapp_user_father = WebAppUser.objects.get(id=webapp_user.father_id)
			if webapp_user_father.member_id and MemberHasSocialAccount.objects.filter(member_id=webapp_user_father.member_id).count() >0:
				return MemberHasSocialAccount.objects.filter(member_id=webapp_user_father.member_id)[0].member
		else:
			if webapp_user.member_id != 0:
				return MemberHasSocialAccount.objects.filter(member_id=webapp_user.member_id)[0].member
		return None
	except:
		error_msg = u"get_member_by:\n{},{}".format(webapp_user_id, unicode_full_stack())
		watchdog_error(error_msg)
		return None


def get_member_info_by(member_id):
	try:
		member = Member.objects.get(id=member_id)
	 	if MemberInfo.objects.filter(member=member).count() > 0:
	 		member_info = MemberInfo.objects.filter(member=member)[0]
	 	else:
	 		member_info = MemberInfo.objects.create(member=member, name = '')
	except:
		return None

def get_member_by_openid(openid, webapp_id):
	try:
		social_account = SocialAccount.objects.get(webapp_id=webapp_id, openid=openid)
		return MemberHasSocialAccount.objects.filter(account=social_account)[0].member
	except:
		return None
	