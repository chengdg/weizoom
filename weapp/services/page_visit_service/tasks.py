#coding:utf8
"""@package services.page_visit_service.tasks
page_visit 的Celery task实现

"""
from django.conf import settings
from modules.member.util import get_social_account_token
from webapp.models import PageVisitLog
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error

from modules.member import member_info_util, member_relation_util
from modules.member import models as member_models
from modules.member import integral
from modules.member import member_settings

from celery import task

def record_pv(request, args):
	"""
	记录Page Visit(PV)
	"""
	member = member_info_util.get_request_member(request)
	try:
		"""
		记录会员访问轨迹
		"""
		if member and request.get_full_path().find('api') == -1:
			member_models.MemberBrowseRecord.objects.create(
				title = '', 
				url = request.get_full_path(), 
				member=member
			)
	except:
		notify_message = u"record_pv, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_message)

	token = get_social_account_token(request, '')
	#add by bert 当token为null的时候是否统计?
	if token == None:
		if settings.MODE == 'develop':
			token = 'user'
		else:
			return
	try:
		PageVisitLog.objects.create(
			webapp_id = request.app.appid,
			token = token,
			is_from_mobile_phone = request.is_from_mobile_phone if hasattr(request, 'is_from_mobile_phone') else False,
			url = request.get_full_path()
		)
	except:
		notify_message = u"record_pv, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_message)


def update_member_source(request, args):
	"""
	更新用户来源(?)
	"""
	member = member_info_util.get_request_member(request)
	if member is None:
		return None

	if member.source == -1:
		followed_member_token = member_info_util.get_followed_member_token(request)
		if followed_member_token:
			followed_member = member_info_util.get_member_by_member_token(followed_member_token)
			if followed_member and member and member.id != followed_member.id and followed_member.webapp_id == request.app.appid:
				member_models.Member.objects.filter(id=member.id).update(source=member_models.SOURCE_BY_URL)
				try:
					shared_url_digest = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, None)
					if shared_url_digest:
						integral.increase_shared_url_followers(followed_member,shared_url_digest)
				except :
					notify_message = u"MemberSouceMiddleware error, cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)
			else:
				member_models.Member.objects.filter(id=member.id).update(source=member_models.SOURCE_SELF_SUB)
		else:
			member_models.Member.objects.filter(id=member.id).update(source=member_models.SOURCE_SELF_SUB)


def build_member_relation(request, args):
	"""
	构建member关系(?)
	"""
	member_relation_util.build_member_follow_relation(request)

@task
def record_page_visit(request0, args):
	"""
	记录page visit的服务

	@param request 无用，为了兼容
	@param args dict类型

	调用方式：

	 * 方式一：通过 `webapp.handlers.event_handler_util` 调用

	 	# 参考 `core/middleware.py` 
	 	from webapp.handlers import event_handler_util
	 	request.event_data = ...
	 	event_handler_util.handle(request, 'page_visit')

	 * 方式二：直接调用

	 	# 参考 `event_handler_util.py`
		from services.page_visit_service.tasks import record_page_visit
		result = record_page_visit.delay(None, request.event_data)
	"""
	# 构造request对象
	from services.service_manager import create_request
	request = create_request(args)

	record_pv(request, args)
	update_member_source(request, args)
	build_member_relation(request, args)
	return "OK"
