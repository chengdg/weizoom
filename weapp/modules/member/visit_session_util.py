# -*- coding: utf-8 -*-

__author__ = 'chuter'

import hashlib
from datetime import datetime

from django.conf import settings

from modules.member import member_settings
from modules.member.member_identity_util import *
from modules.member.member_info_util import *
from modules.member.models import AnonymousClickedUrl, MemberClickedUrl

from core.dateutil import is_timespan_beyond_the_interval_util
from utils.url_helper import remove_querystr_filed_from_request_url

def get_request_url(request):
	shared_url = remove_querystr_filed_from_request_url(request, 'from')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'isappinstalled')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'from')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'isappinstalled')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'code')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'state')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'appid')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'workspace_id')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'workspace_id')
	return shared_url

def get_request_url_digest(request, request_url=None):
	if request_url is None:
		request_url = get_request_url(request)
	return hashlib.md5(request_url).hexdigest()

#===============================================================================
# record_shared_page_visit : 记录分享页面的访问记录
#
# 分享出去的url地址都会在url中携带分享会员的token信息
# 
# 1. 如果请求中携带了会员的session信息，那么记录到MemberClickedUrl中
# 2. 否则请求中肯定会携带uuid信息，那么记录到AnonymousClickedUrl中
#===============================================================================
def record_shared_page_visit(request):
	followed_member_token = get_followed_member_token_from_url_querystr(request)
	if followed_member_token is None or len(followed_member_token) == 0:
		#对于url中没有分享者信息的不进行任何处理
		return

	followed_member = get_member_by_member_token(followed_member_token)
	if followed_member is None:
		#如果获取不到分享者信息不进行任何处理
		return

	url = get_request_url(request)
	#request_path_digest = get_request_url_digest(request, request_url)

	#url_digest = hashlib.md5(url).hexdigest()
	request_path_digest = hashlib.md5(url).hexdigest()
	member = get_request_member(request)
	if member:
		if followed_member_token == member.token:
			#如果当前访问者即分享者那么不进行任何操作
			return

		records = MemberClickedUrl.objects.filter(mid=member.id, followed_mid=followed_member.id)
		if records.count() > 0:
			records.update(
				url_digest = request_path_digest,
				created_at = datetime.now()
				)
		else:
			MemberClickedUrl.objects.create(
				url = url,
				url_digest = request_path_digest,
				mid = member.id,
				followed_mid = followed_member.id
				)
	else:
		uuid = get_uuid(request)
		if uuid:
			records = AnonymousClickedUrl.objects.filter(uuid=uuid, followed_mid=followed_member.id)
			if records.count() > 0:
				records.update(
					url_digest = request_path_digest,
					created_at = datetime.now()
					)
			else:
				AnonymousClickedUrl.objects.create(
					url = url,
					url_digest = request_path_digest,
					uuid = uuid,
					followed_mid = followed_member.id,
					webapp_user_id = request.webapp_user.id
					)

def __has_last_visit_beyond_the_interval(member_id, uuid, followed_member, interval_seconds, request=None):
	# request_path_digest = get_request_url_digest(request)
	# if member_id and member_id > 0:
	# 	# visit_records = MemberClickedUrl.objects.filter(followed_mid=followed_member.id, mid=member_id, url_digest=request_path_digest)
	# 	visit_records = MemberClickedUrl.objects.filter(followed_mid=followed_member.id, mid=member_id).order_by('-created_at')
	# elif uuid:
	# 	# visit_records = AnonymousClickedUrl.objects.filter(followed_mid=followed_member.id, uuid=uuid, url_digest=request_path_digest)
	# 	visit_records = AnonymousClickedUrl.objects.filter(followed_mid=followed_member.id, uuid=uuid).order_by('-created_at')
	# else:
	# 	return True

	# if visit_records.count() == 0:
	# 	return True
	# request_path_digest = get_request_url_digest(request)
	if member_id and member_id > 0:
		# visit_records = MemberClickedUrl.objects.filter(followed_mid=followed_member.id, mid=member_id, url_digest=request_path_digest)
		member_visit_records = MemberClickedUrl.objects.filter(followed_mid=followed_member.id, mid=member_id).order_by('-created_at')
	else:
		member_visit_records = None

	if request.webapp_user:
		# visit_records = AnonymousClickedUrl.objects.filter(followed_mid=followed_member.id, uuid=uuid, url_digest=request_path_digest)
		uuid_visit_records = AnonymousClickedUrl.objects.filter(followed_mid=followed_member.id, webapp_user_id=request.webapp_user.id).order_by('-created_at')
	else:
		uuid_visit_records = None
	if (member_visit_records is None) and (uuid_visit_records is None):
		return True

	if uuid_visit_records and uuid_visit_records.count() == 0:
		return True

	if member_visit_records and member_visit_records.count() == 0:
		return True
	if member_visit_records and member_visit_records.count() > 0:
		visit_records = member_visit_records
		return False
	elif uuid_visit_records and uuid_visit_records.count() > 0:
		visit_records = uuid_visit_records
		return False
	else:
		return True

	last_vist_datetime = visit_records[0].created_at
	return is_timespan_beyond_the_interval_util(last_vist_datetime, interval_seconds)

def has_visit(request, member_id, uuid):
	if (member_id is None or member_id <= 0) and uuid is None:
		return False

	followed_member_token = get_followed_member_token_from_url_querystr(request)
	if followed_member_token is None or len(followed_member_token) == 0:
		#对于url中没有分享者信息的不进行任何处理
		return

	followed_member = get_member_by_member_token(followed_member_token)
	if followed_member is None:
		#如果获取不到分享者信息不进行任何处理
		return

	return not __has_last_visit_beyond_the_interval(member_id, uuid, followed_member, settings.VISIT_RECORD_MIN_TIME_SPAN_SECONDS, request)