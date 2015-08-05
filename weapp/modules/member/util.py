# -*- coding: utf-8 -*-

__author__ = 'bert'

import time
import os
import qrcode

from django.conf import settings
from django.db.models import F

from core.exceptionutil import full_stack, unicode_full_stack
from core.wxapi import get_weixin_api

from utils.uuid import uniqueid
from utils.string_util import byte_to_hex

from models import *
from weixin.user.models import WeixinUser
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN, SOCIAL_PLATFORM_QQ, SOCIAL_PLATFORM_SINAWEIBO
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from mall.models import Order

import member_settings

import member_info_util
import member_identity_util
import member_relation_util

def get_request_member(request):
	#假设经过了MemberSessionMiddleware中间件的处理
	return member_info_util.get_request_member(request)

def get_request_social_account(request):
	#假设经过了RequestSocialAccountSessionMiddleware中间件的处理
	return member_info_util.get_request_social_account(request)

def get_followed_member_token_from_url_querystr(request):
	return member_info_util.get_followed_member_token_from_url_querystr(request)

def get_followed_member_token_from_cookie(request):
	return member_info_util.get_followed_member_token_from_cookie(request)

def get_followed_member_token(request):
	return member_info_util.get_followed_member_token(request)

def get_member_by_member_token(member_token):
	return member_info_util.get_member_by_member_token(member_token)

def get_member_by_binded_social_account(social_account):
	return member_info_util.get_member_by_binded_social_account(social_account)

def get_followed_member(request):
	return member_info_util.get_followed_member(request)

########################################################################
# get_uuid : 获取请求信息中包含的uuid信息
# 对于还没有与微站进行过绑定的用户，cookie中都会有uuid信息，用于记录
# 在绑定前在微站中进行的操作行为
########################################################################
def get_uuid(request):
	return member_identity_util.get_uuid(request)

def generate_uuid(request):
	return member_identity_util.generate_uuid(request)

def get_social_account_token_from_url(request):
	return member_info_util.get_social_account_token_from_url(request)

def get_social_account_token_from_cookie(request):
	return member_info_util.get_social_account_token_from_cookie(request)

def get_social_account_token(request, default=None):
	return member_info_util.get_social_account_token(request, default=None)

def get_social_account(request):
	return member_info_util.get_social_account(request)

########################################################################
# get_member : 获取会员信息
# 如果cookie中携带会员token信息，直接根据会员token获取对应的会员信息返回
# 如果根据请求可获取当前请求的社交账户信息，则根据社交账户获取对应的会员
# 否则返回None
########################################################################
def get_member(request):
	return member_info_util.get_member(request)

def get_request_member(request):
	return member_info_util.get_request_member(request)	

def get_member_binded_social_account(member):
	return member_info_util.get_member_binded_social_account(member)

def update_member_basic_info(user_profile, member, oauth_create=False):
	member_info_util.update_member_basic_info(user_profile, member, oauth_create)

member_basic_info_updater = update_member_basic_info

#TODO 考虑数据库操作事务？
def create_member_by_social_account(user_profile, social_account, is_checked=True):
	return member_info_util.create_member_by_social_account(user_profile, social_account, is_checked)

def get_all_group(user_profile):
	return member_info_util.get_all_group(user_profile)

def get_member_group_id(user_profile, openid):
	return member_info_util.get_member_group_id(user_profile, openid)

def create_relation_in_weapp(member, all_groups, member_group_id):
	return member_info_util.create_relation_in_weapp(member, all_groups, member_group_id)

def create_member_group(all_groups, webapp_id):
	return member_info_util.create_member_group(all_groups, webapp_id)
		
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
	return member_info_util.create_member(request)

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
	return member_info_util.create_social_account(webapp_id,
						  openid,
						  token,
						  platform,
						  is_for_test=is_for_test)

#===============================================================================
# build_member_follow_relation : 建立会员之间的关系, 
# 成功创建返回True，否则返回False
#
# 1. 如果request的cookie信息中包含了当前会员信息那么进行2中的操作，否则返回结束
# 2. 如果从request的cookie中可以获取到当前会员所关注的会员信息则进行3中的操作，
#    否则结束
# 3. 创建对应会员的双向关系, 如果当前会员信息和所关注的会员信息相同不进行任何操
#    作，否则创建关系
#
# 该方法中假设已经经过中间件MemberSessionMiddleware的处理
#===============================================================================
def build_member_follow_relation(request):
	return member_relation_util.build_member_follow_relation(request)

def get_followed_member_shared_url_info(request):
	return member_relation_util.get_followed_member_shared_url_info(request)

def remove_shared_info(request):
	member_relation_util.remove_shared_info(request)

########################################################################
# create_qrcode : 创建二维码
########################################################################
def create_qrcode(member_id):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4
	)
	qr.add_data('member=%d' % member_id)
	img = qr.make_image()

	file_name = '%d.png' % member_id
	dir_path = os.path.join(settings.UPLOAD_DIR, '../member_qrcode')
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	file_path = os.path.join(dir_path, file_name)
	img.save(file_path)

	return '/static/member_qrcode/%s' % file_name

########################################################################
# process_payment_with_shared_info : 购买完成后进行分享链接的相关处理
#
# 如果请求信息中没有相应的分享链接信息，那么不进行任何处理
# 否则该分享链接带来的购买量+1
########################################################################
def process_payment_with_shared_info(request):
	member_relation_util.process_payment_with_shared_info(request)

def get_request_webapp_user_by_uuid(uuid, webapp_id):
	return member_identity_util.get_request_webapp_user_by_uuid(uuid, webapp_id)

from core.alipay.alipay_notify import AlipayNotify
def get_request_webapp_user_by_member(request, is_create_when_not_exist=True):
	return member_identity_util.get_request_webapp_user_by_member(request, is_create_when_not_exist)

def update_member_group(user_profile, member, social_account=None):
	return member_info_util.update_member_group(user_profile, member, social_account)

def update_send_mass_msg_log(user_profile, msg_id, sent_count, total_count, filter_count, error_count, status):
	if user_profile and msg_id:
		UserSentMassMsgLog.update_log(user_profile.webapp_id, msg_id, sent_count, total_count, filter_count, error_count, status)	

def update_models_use_webapp_user(current_webapp_user, expired_webapp_user):
	if current_webapp_user is None and expired_webapp_user is None:
		return None
	
	if current_webapp_user.webapp_id == expired_webapp_user.webapp_id:
		Order.objects.filter(webapp_user_id=expired_webapp_user.id, webapp_id=current_webapp_user.webapp_id).update(webapp_user_id=current_webapp_user.id)

