# -*- coding: utf-8 -*-
__author__ = 'bert'

import time
import os
import qrcode
import random
import string

from django.conf import settings
from django.db.models import F

from core.exceptionutil import full_stack, unicode_full_stack
from core.wxapi import get_weixin_api

from datetime import datetime

from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from utils.uuid import uniqueid
from utils.string_util import byte_to_hex

from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN, SOCIAL_PLATFORM_QQ, SOCIAL_PLATFORM_SINAWEIBO
from account.social_account.account_info import get_social_account_info
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

import member_settings
from models import *

from modules.member import tasks

########################################################################
# get_member : 获取会员信息
# 如果cookie中携带会员token信息，直接根据会员token获取对应的会员信息返回
# 如果根据请求可获取当前请求的社交账户信息，则根据社交账户获取对应的会员
# 否则返回None
########################################################################
def get_member(request):
	if request.user_profile is None:
		#如果获取不到当前所请求的店铺信息则直接返回None
		return None

	member = get_request_member(request)
	if member:
		if member.webapp_id != request.user_profile.webapp_id:
			#如果获取到的当前请求的会员不是当前所请求的店铺中的则返回None
			return None
		else:
			return member

	request_social_account = get_social_account(request)
	if request_social_account is None:
		return None
	else:
		cur_request_social_account = request_social_account
		if MemberHasSocialAccount.objects.filter(account=cur_request_social_account).count() > 0:
			return MemberHasSocialAccount.objects.filter(account=cur_request_social_account)[0].member
		else:
			return None
				
def get_request_member(request):
	#假设经过了MemberSessionMiddleware中间件的处理
	return request.member if hasattr(request, 'member') else None

def get_request_social_account(request):
	#假设经过了RequestSocialAccountSessionMiddleware中间件的处理
	return request.social_account if hasattr(request, 'social_account') else None

def get_social_account_token_from_url(request):
	return request.GET.get(member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD, None)

def get_social_account_token_from_cookie(request):
	return request.COOKIES.get(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, None)

def get_social_account_token(request, default=None):
	social_account_token_in_url = get_social_account_token_from_url(request)
	if social_account_token_in_url is None:
		social_account_token_in_cookie = get_social_account_token_from_cookie(request)
		return social_account_token_in_cookie if social_account_token_in_cookie else default
	else:
		return social_account_token_in_url

def get_social_account(request):
	social_account = get_request_social_account(request)
	if social_account:
		return social_account

	social_account_session_key = request.COOKIES.get(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, None)
	if social_account_session_key:
		try:
			return SocialAccount.objects.get(token=social_account_session_key)	
		except:
			notify_message = u"从数据库读取社会化账号信息失败，社交账户信息:('token':{}), cause:\n{}".format(
				social_account_session_key, unicode_full_stack())
			watchdog_warning(notify_message)
			return None
	else:
		return None

#===============================================================================
# create_member : 创建会员
#
# 该方法假设已经经过RequestSocialAccountSessionMiddleware中间件的处理，
# 即可直接通过request.social_account获取当前请求的社交用户信息
#
# 1. 首先check当前请求的社交用户信息是否为空，如果是直接返回None;
# 2. 否则，根据当前请求的社交用户信息创建对应的会员信息并返回;
#===============================================================================
def create_member(request):
	if request.user_profile is None:
		#如果识别当前所请求的应用对应的用户配置信息，不进行任何处理
		return None

	if request.social_account is None:
		return None
	else:
		try:
			return create_member_by_social_account(request.user_profile, request.social_account)
		except:
			notify_message = u"创建会员信息失败，社交账户信息:('openid':{}), cause:\n{}".format(
				request.social_account.openid, unicode_full_stack())
			watchdog_error(notify_message)
			return None

def update_member_group(user_profile, member, social_account=None):
	if (member is None) or (social_account is None) or member.is_for_test or (member.is_subscribed is False):
		return

	if len(MemberHasTag.get_member_has_tags(member)) == 0:
		all_groups = get_all_group(user_profile)
		member_group_id =  get_member_group_id(user_profile, social_account.openid)
		create_relation_in_weapp(member, all_groups, member_group_id)

def get_member_by_binded_social_account(social_account):
	if social_account is None:
		return None

	try:
		return MemberHasSocialAccount.objects.filter(
			account = social_account,
			webapp_id = social_account.webapp_id
			)[0].member
	except:
		return None
	# member_has_social_accounts = MemberHasSocialAccount.objects.filter(
	# 	account = social_account,
	# 	webapp_id = social_account.webapp_id
	# 	)

	# if member_has_social_accounts.count() >= 1:
	# 	return member_has_social_accounts[0].member
	# else:
	# 	return None


def get_followed_member_token_from_url_querystr(request):
	return request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)

def get_followed_member_token_from_cookie(request):
	return request.COOKIES.get(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, None)

def get_followed_member_token(request):
	followed_member_token = get_followed_member_token_from_cookie(request)
	if followed_member_token is None:
		return get_followed_member_token_from_url_querystr(request)
	else:
		return followed_member_token

def get_followed_member(request):
	member_token = get_followed_member_token(request)
	if member_token is None:
		return None
	else:
		return get_member_by_member_token(member_token)

def get_member_by_member_token(member_token):
	if member_token is None or len(member_token) == 0:
		return None
	try:
		return Member.objects.get(token=member_token)
	except:
		notify_message = u"根据token获取会员信息失败,可能会员已被删除，会员token={}, cause:\n{}".format(member_token, unicode_full_stack())
		watchdog_warning(notify_message)
		return None

def get_all_group(user_profile):
	mpuser_access_token = _check_access_token(user_profile)

	if mpuser_access_token:
		weixin_api = get_weixin_api(mpuser_access_token)
		groups = weixin_api.get_groups()
		return groups
	else:
		return None

def get_member_group_id(user_profile, openid):
	mpuser_access_token = _check_access_token(user_profile)

	if mpuser_access_token:
		weixin_api = get_weixin_api(mpuser_access_token)
		groups = weixin_api.get_member_group_id(openid)
		return groups
	else:
		return None

def _check_access_token(user_profile):
	mp_user = get_binding_weixin_mpuser(user_profile.user)
	if mp_user is None:
		return None

	if not mp_user.is_service or not mp_user.is_certified:
		return None
		
	mpuser_access_token = get_mpuser_accesstoken(mp_user)

	if mpuser_access_token is None:
		return None

	if mpuser_access_token.is_active:
		return mpuser_access_token
	else:
		return None

def create_relation_in_weapp(member, all_groups, member_group_id):
	if member and all_groups and member_group_id:
		if 'groups' in all_groups.keys() and  'groupid' in member_group_id.keys():
			name = ''
			for group in all_groups['groups']:
				if 'id' in group.keys() and int(group['id']) == int(member_group_id['groupid']):
					name = group['name']
					break
			if name != '':
				member_tag = MemberTag.get_member_tag(member.webapp_id, name)
				if member_tag is None:
					member_tag = MemberTag.create(member.webapp_id, name)
				
				MemberHasTag.add_tag_member_relation(member, [member_tag.id])	

def create_member_group(all_groups, webapp_id):
	if all_groups and 'groups' in all_groups.keys():
		for groups in all_groups['groups']:
			name = ''
			if 'name' in groups.keys():
				name = groups['name']
			if name != '':
				member_tag = MemberTag.get_member_tag(webapp_id, name)
				if member_tag is None:
					member_tag = MemberTag.create(webapp_id, name)
		
def get_member_binded_social_account(member):
	if member is None:
		return None

	try:
		member_social_account_relation = MemberHasSocialAccount.objects.get(member=member)
		return member_social_account_relation.account	
	except:
		notify_message = u"根据会员信息从数据库获取绑定的社会化账号信息失败，会员id:{}, cause:\n{}".format(
				member.id, unicode_full_stack())
		watchdog_warning(notify_message)

		return None		

def update_member_basic_info(user_profile, member):
	if member.is_for_test:
		return
	#系统网络问题会员信息更新不下了 改正
	today = datetime.now()
	today_str = datetime.today().strftime('%Y-%m-%d')
	if member.update_time.strftime("%Y-%m-%d") == today_str:
		return None

	if user_profile is None:
		return None

	social_account = get_member_binded_social_account(member)
	social_account_info = get_social_account_info(social_account, user_profile, False)
	if social_account_info:
		member.user_icon = social_account_info.head_img

		if settings.MODE == 'develop' and social_account_info.nickname == u'预览':
			pass
		else:
			member.username = social_account_info.nickname

		member_nickname = social_account_info.nickname if social_account_info else ''
		if member_nickname:
			if isinstance(member_nickname, unicode):
				member_nickname_str = member_nickname.encode('utf-8')
			else:
				member_nickname_str = member_nickname
			username_hexstr = byte_to_hex(member_nickname_str)
		else:
			username_hexstr = member.username_hexstr
		if social_account_info.is_subscribed:
			Member.objects.filter(id=member.id).update(user_icon=member.user_icon, 
					update_time = today, 
					username_hexstr=username_hexstr,
					is_subscribed=social_account_info.is_subscribed,
					city=social_account_info.city,
					province=social_account_info.province,
					country=social_account_info.country,
					sex=social_account_info.sex,
					)
		else:
			Member.objects.filter(id=member.id).update( 
					update_time = today, 
					is_subscribed=social_account_info.is_subscribed,
					)
		# member.update_time = today
		# member.save()
		

member_basic_info_updater = update_member_basic_info

def _generate_member_token(member, social_account):
	return "{}{}{}{}".format(
		member.webapp_id, 
		social_account.platform,
		time.strftime("%Y%m%d"),
		(''.join(random.sample(string.ascii_letters + string.digits, 6))) + str(member.id))

#TODO 考虑数据库操作事务？
def create_member_by_social_account(user_profile, social_account, is_checked=True):
	#print '==========================1'
	#if is_checked:
	if MemberHasSocialAccount.objects.filter(webapp_id=user_profile.webapp_id, account=social_account).count() >  0:
		return MemberHasSocialAccount.objects.filter(webapp_id=user_profile.webapp_id, account=social_account)[0].member

	member_grade = MemberGrade.get_default_grade(social_account.webapp_id)
	temporary_token = _create_random()
	is_new = False
	try:
		member = Member.objects.create(
			webapp_id = social_account.webapp_id,
			user_icon = '',#social_account_info.head_img if social_account_info else '',
			username_hexstr = '',
			grade = member_grade,
			remarks_name = '',
			token = temporary_token,
			is_for_test = social_account.is_for_test
		)
		is_new = True
	except:
		notify_message = u"create_member_by_social_account1: cause:\n{}".format(unicode_full_stack())
		watchdog_warning(notify_message)
		try:
			temporary_token = _create_random()
			member = Member.objects.create(
				webapp_id = social_account.webapp_id,
				user_icon = '',#social_account_info.head_img if social_account_info else '',
				username_hexstr = '',#username_hexstr,
				grade = member_grade,
				remarks_name = '',
				token = temporary_token,
				is_for_test = social_account.is_for_test,
			)
			is_new = True
		except:
			notify_message = u"create_member_by_social_account2: cause:\n{}".format(unicode_full_stack())
			watchdog_warning(notify_message)
			member = None
	
	if member is None:
		return None
	

	if MemberHasSocialAccount.objects.filter(webapp_id=user_profile.webapp_id, account=social_account).count() >  0:
		member.delete()
		member = MemberHasSocialAccount.objects.filter(webapp_id=user_profile.webapp_id, account=social_account)[0].member
	else:	
		try:
			if MemberHasSocialAccount.objects.filter(webapp_id=social_account.webapp_id, member=member, account=social_account).count() == 0:
				MemberHasSocialAccount.objects.create(
					member = member,
					account = social_account,
					webapp_id = member.webapp_id
					)
			else:
				try:
					member.delete()
				except:
					pass
				member = MemberHasSocialAccount.objects.filter(webapp_id=member.webapp_id, account=social_account)[0].member

		except:
			#如果会员及对应的社交账号关系创建失败，则删除刚创建的会员信息
			#避免重复创建会员
			#TODO 进行预警操作
			if member is not None:
				try:
					member.delete()
				except:
					pass
				return None
	
	try:
		token = _generate_member_token(member, social_account)
		member.token = token
		member.save()
	except:
		token = _generate_member_token(member, social_account)
		member.token = token
		member.save()
		
	member.is_new = is_new
	# try:
	# 	if member:
	# 		tasks.create_member_info.delay(member.id, '', social_account_info.sex if social_account_info and social_account_info.sex else SEX_TYPE_UNKOWN)
	# 	# MemberInfo.objects.create(
	# 	# 	member = member,
	# 	# 	name = '',
	# 	# 	sex = social_account_info.sex if social_account_info and social_account_info.sex else SEX_TYPE_UNKOWN
	# 	# 	)
	# except:
	# 	#如果会员信息创建失败，则删除刚创建的会员信息
	# 	#避免查看会员详情时出现问题
	# 	if member:
	# 		tasks.create_member_info.delay(member.id, '', SEX_TYPE_UNKOWN)
	return member




	# print '------------------------------'
	# if is_checked:
	# 	if MemberHasSocialAccount.objects.filter(webapp_id=user_profile.webapp_id, account=social_account).count() >  0:
	# 		return MemberHasSocialAccount.objects.filter(webapp_id=user_profile.webapp_id, account=social_account)[0].member
	# social_account_info = get_social_account_info(social_account, user_profile)
	# member_grade = MemberGrade.get_default_grade(social_account.webapp_id)
	# member_nickname = social_account_info.nickname if social_account_info else ''
	# if isinstance(member_nickname, unicode):
	# 	member_nickname_str = member_nickname.encode('utf-8')
	# else:
	# 	member_nickname_str = member_nickname
	# username_hexstr = byte_to_hex(member_nickname_str)
	
	# if not username_hexstr:
	# 	username_hexstr = ''
	# temporary_token = _create_random()
	# try:
	# 	member = Member.objects.create(
	# 		webapp_id = social_account.webapp_id,
	# 		user_icon = social_account_info.head_img if social_account_info else '',
	# 		username_hexstr = username_hexstr,
	# 		grade = member_grade,
	# 		remarks_name = '',
	# 		token = temporary_token,
	# 		is_for_test = social_account.is_for_test
	# 	)
	# 	member.is_new = True
	# except:
	# 	try:
	# 		temporary_token = _create_random()
	# 		member = Member.objects.create(
	# 			webapp_id = social_account.webapp_id,
	# 			user_icon = social_account_info.head_img if social_account_info else '',
	# 			username_hexstr = username_hexstr,
	# 			grade = member_grade,
	# 			remarks_name = '',
	# 			token = temporary_token,
	# 			is_for_test = social_account.is_for_test
	# 		)
	# 		member.is_new = True
	# 	except:
	# 		notify_message = u"create_member_by_social_account: cause:\n{}".format(unicode_full_stack())
	# 		watchdog_warning(notify_message)
	# 		member = None
	# if member is None:
	# 	return None
	# token = _generate_member_token(member, social_account)
	# if Member.objects.filter(webapp_id=social_account.webapp_id,token=token).count() > 0:
	# 	return Member.objects.filter(webapp_id=social_account.webapp_id,token=token)[0]
	# else:
	# 	try:
	# 		member.token = token
	# 		member.save()
	# 	except:
	# 		notify_message = u"保存会员token失败，请查询该token是否存在，token:{}, cause:\n{}".format(token, unicode_full_stack())
	# 		watchdog_error(notify_message)
	# 		if member is not None:
	# 			try:
	# 				member.delete()
	# 			except:
	# 				pass
	# 		if Member.objects.filter(webapp_id=social_account.webapp_id,token=token).count() > 0:
	# 			return Member.objects.filter(webapp_id=social_account.webapp_id,token=token)[0]
	# 		else:
	# 			return None
	# try:
	# 	if MemberHasSocialAccount.objects.filter(webapp_id=social_account.webapp_id, member=member, account=social_account).count() == 0:
	# 		MemberHasSocialAccount.objects.create(
	# 			member = member,
	# 			account = social_account,
	# 			webapp_id = member.webapp_id
	# 			)
	# 	else:
	# 		try:
	# 			member.delete()
	# 		except:
	# 			pass
	# 		return MemberHasSocialAccount.objects.filter(webapp_id=member.webapp_id, account=social_account)[0].member

	# except:
	# 	#如果会员及对应的社交账号关系创建失败，则删除刚创建的会员信息
	# 	#避免重复创建会员
	# 	#TODO 进行预警操作
	# 	if member is not None:
	# 		try:
	# 			member.delete()
	# 		except:
	# 			pass
	# 		return None
	# try:
	# 	if member:
	# 		tasks.create_member_info.delay(member.id, '', social_account_info.sex if social_account_info and social_account_info.sex else SEX_TYPE_UNKOWN)
	# 	# MemberInfo.objects.create(
	# 	# 	member = member,
	# 	# 	name = '',
	# 	# 	sex = social_account_info.sex if social_account_info and social_account_info.sex else SEX_TYPE_UNKOWN
	# 	# 	)
	# except:
	# 	#如果会员信息创建失败，则删除刚创建的会员信息
	# 	#避免查看会员详情时出现问题
	# 	if member:
	# 		tasks.create_member_info.delay(member.id, '', SEX_TYPE_UNKOWN)
	# return member

import random
def _create_random():
	date = str(time.time()*1000)
	sample_list = ['0','1','2','3','4','5','6','7','8','9','a', 'b', 'c', 'd', 'e'] 
		
	random_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
	random_str = date + random_str
	return random_str
#===============================================================================
# create_social_account : 创建社会化账号
# platform 指定社会化平台，支持：
# SOCIAL_PLATFORM_WEIXIN : 微信
# SOCIAL_PLATFORM_QQ : QQ
# SOCIAL_PLATFORM_SINAWEIBO : 新浪微博
#
# platform默认为SOCIAL_PLATFORM_WEIXIN，即微信平台
#===============================================================================
def create_social_account(webapp_id,
						  openid,
						  token,
						  platform,
						  is_for_test=False):
	social_account, _ = SocialAccount.objects.get_or_create(
			platform = platform, 
			webapp_id = webapp_id,
			openid = openid,
			token = token,
			is_for_test = is_for_test
		)	
	return social_account
