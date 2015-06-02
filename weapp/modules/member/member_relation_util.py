# -*- coding: utf-8 -*-
"""@package modules.member.member_relation_util
member_relation_util

"""
__author__ = 'bert'

from utils.uuid import uniqueid
from utils.string_util import byte_to_hex

import member_settings

from member_info_util import *
from models import *

from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info
from core.exceptionutil import full_stack, unicode_full_stack


def build_member_follow_relation(request):
	"""
	build_member_follow_relation : 建立会员之间的关系

	@retval 成功创建返回True，否则返回False

	说明：

	1. 如果request的cookie信息中包含了当前会员信息那么进行2中的操作，否则返回结束。

	2. 如果从request的cookie中可以获取到当前会员所关注的会员信息则进行3中的操作，否则结束。

	3. 创建对应会员的双向关系, 如果当前会员信息和所关注的会员信息相同不进行任何操作，否则创建关系

	@note 该方法中假设已经经过中间件MemberSessionMiddleware的处理。

	"""
	member = get_request_member(request)
	if member is None:
		return False
	followed_member_token = get_followed_member_token(request)

	followed_member = get_member_by_member_token(followed_member_token)
	if followed_member is None:
		if followed_member_token is not None:
			#如果cookie中携带的所关注的会员信息在库中不存在则删除
			#cookie中的携带的所关注的会员的token信息
			from middleware import MemberRelationMiddleware
			request.META[MemberRelationMiddleware.SHOULD_REMOVE_FOLLOWED_MEMBER_SESSION_FLAG] = True
		return False
	if followed_member.id == member.id:
		return False
	if followed_member.webapp_id != member.webapp_id:
		#如果不是同一个webapp的不建立关系
		return False
	if MemberFollowRelation.objects.filter(member_id=followed_member.id, follower_member_id=member.id).count() == 0:
		is_fans = False if MemberFollowRelation.objects.filter(follower_member_id=member.id,is_fans=True).count() > 0 else True
		if member.source == -1 and is_fans:
			is_fans = True
		else:
			is_fans = False
		MemberFollowRelation.objects.create(
			member_id = followed_member.id,
			follower_member_id = member.id,
			is_fans = is_fans,
		)

		MemberFollowRelation.objects.create(
			member_id = member.id,
			follower_member_id = followed_member.id
		)
		try:
			Member.update_factor(member)
			Member.update_factor(followed_member)
			Member.increase_friend_count(('%d, %d') % (member.id, followed_member.id))
		except:
			notify_message = u"点击分享链接更新好友数量异常 cause:\n{}".format(unicode_full_stack()
			)
			watchdog_warning(notify_message)
		return True
	else:
		return False

def get_followed_member_shared_url_info(request):
	followed_member_token = get_followed_member_token(request)
	followed_member = get_member_by_member_token(followed_member_token)
	member = get_request_member(request)
	if member is None:
		return None
	if followed_member is None:
		return None
	if member.id == followed_member.id:
		return None

	shared_url_digest = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, None)
	if shared_url_digest is None:
		return None

	try:
		return MemberSharedUrlInfo.objects.get(member=followed_member, shared_url_digest=shared_url_digest)
	except:
		notify_message = u"从数据库获取会员分享链接信息失败，会员id:{}, shared_url_digest:{}}, cause:\n{}".format(
			followed_member.id, followed_member.shared_url_digest, unicode_full_stack()
		)
		watchdog_warning(notify_message)
		return None


def process_payment_with_shared_info(request):
	"""
	购买完成后进行分享链接的相关处理
	
	如果请求信息中没有相应的分享链接信息，那么不进行任何处理,。
	否则该分享链接带来的购买量+1

	"""
	member_shared_url_info = get_followed_member_shared_url_info(request)

	if not member_shared_url_info:
		return

	try:
		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update member_shared_url_info set leadto_buy_count=leadto_buy_count+1 where id = %d' % member_shared_url_info.id)
		transaction.commit_unless_managed()

		#计算成功后清除请求中携带的分享链接信息
		remove_shared_info(request)
	except:
		notify_message = u"更新分享链接带来的购买量失败，分享链接id:{}, cause:\n{}".format(
			member_shared_url_info.id, unicode_full_stack()
		)
		watchdog_warning(notify_message)


def remove_shared_info(request):
	from middleware import RemoveSharedInfoMiddleware
	request.META[RemoveSharedInfoMiddleware.SHOULD_REMOVE_SHARED_URL_SESSION_FLAG] = True
	





