# -*- coding: utf-8 -*-

#from modules.member.middleware import _is_need_process_for_shared_url_request
from modules.member.visit_session_util import record_shared_page_visit #, get_request_url_digest,get_request_url
from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack

#from services.service_manager import register
#from modules.member.util import get_social_account_token

#from webapp.models import WebApp
#from django.contrib.auth.models import User
from modules.member import integral

from celery import task

#@register('shared_url_page_visit')
def serve(request, args):
	#先进行分享链接的pv更新
	try:
		integral.update_shared_url_pv(request)
	except:
		notify_message = u"进行分享页pv更新失败，path={}, cause:\n{}".format(request.get_full_path(), unicode_full_stack())
		watchdog_error(notify_message)

	integral.process_shared_url_request(request)

	try:
		record_shared_page_visit(request)
	except:
		notify_message = u"进行页面访问记录失败，path={}, cause:\n{}".format(request.get_full_path(), unicode_full_stack())
		watchdog_error(notify_message)

@task
def shared_url_page_visit(request0, args):
	from services.service_manager import create_request
	request = create_request(args)
	serve(request, args)
