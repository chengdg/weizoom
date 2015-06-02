# -*- coding: utf-8 -*-

__author__ = "chuter"

import re
import urllib2

from weixin.user.models import WeixinMpUserAccessToken, WeixinMpUser

from django.contrib.auth.decorators import login_required
from django.conf import settings

from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_fatal

from settings import *

NOTIFY_TYPE = 'WEB_ERROR'

def __should_change_to_delete_request(menu_json_str):
	if menu_json_str is None:
		return True

	try:
		menu_json_str = re.sub('\\s+', '', menu_json_str)
		return menu_json_str == '{}'
	except:
		return False

########################################################################
# delete_customerized_menu: 删除自定义菜单
########################################################################
@login_required
def delete_customerized_menu(request):
	try:
		#在微信平台中删除
		response_content = _delete_weixin_customerized_menu(request.user)

		if _is_wexin_request_successful(response_content):
			response = create_response(200)
		else:
			response = create_response(500)
			response.errMsg = response_content
	except:
		notify_msg = u"删除自定义菜单失败({})，cause:\n{}".format(request.user.username, unicode_full_stack())
		_notify_weixin_request_failure(notify_msg)

		response = create_response(500)
		response.innerErrMsg = notify_msg

	return response.get_response()

########################################################################
# create_customerized_menu: 创建自定义菜单
########################################################################
@login_required
def create_customerized_menu(request):
	menu_json = request.POST['menu_json']

	if __should_change_to_delete_request(menu_json):
		return delete_customerized_menu(request)

	try:
		#在微信平台中创建
		response_content = _create_weixin_customerized_menu(request.user, menu_json)

		if _is_wexin_request_successful(response_content):
			response = create_response(200)
		else:
			response = create_response(500)
			response.errMsg = response_content
	except:
		notify_msg = u"创建自定义菜单失败({})，cause:\n{}".format(request.user.username, unicode_full_stack())
		_notify_weixin_request_failure(notify_msg)

		response = create_response(500)
		response.innerErrMsg = notify_msg

	return response.get_response()

########################################################################
# update_customerized_menu: 更新自定义菜单
########################################################################
@login_required
def update_customerized_menu(request):
	if settings.MODE == 'develop':
		print request
		return create_response(200).get_response()
	else:
		menu_json = request.POST['menu_json']

		if __should_change_to_delete_request(menu_json):
			return delete_customerized_menu(request)

		try:
			#在微信平台中删除
			response_content = _delete_weixin_customerized_menu(request.user)
			if not _is_wexin_request_successful(response_content):
				response = create_response(500)
				response.errMsg = response_content
			else:
				#然后重新创建
				response_content = _create_weixin_customerized_menu(request.user, menu_json)

				if _is_wexin_request_successful(response_content):
					response = create_response(200)
				else:
					response = create_response(500)
					response.errMsg = response_content
		except:
			notify_msg = u"更新自定义菜单失败({})，cause:\n{}".format(request.user.username, unicode_full_stack())
			_notify_weixin_request_failure(notify_msg)

			response = create_response(500)
			response.innerErrMsg = notify_msg

		return response.get_response()

def _notify_weixin_request_failure(msg):
	watchdog_fatal(msg)

def _is_wexin_request_successful(response_content):
	response_json = decode_json_str(response_content)
	return response_json['errcode'] == 0

WEIXIN_MENU_OP_CREATE = 'create'
WEIXIN_MENU_OP_DELETE = 'delete'

class WeixinMenuRequest(object):
	def __init__(self):
		super(WeixinMenuRequest, self).__init__()

	def do_weixin_menu_create_request(self, request_url, menu_json):
		req = urllib2.Request(request_url)
		opener = urllib2.build_opener()
		response = opener.open(req, menu_json.encode('utf-8'))

		try:
			content = response.read()
		finally:
			if response:
				try:
					response.close()
				except:
					pass

		return content

	def do_weixin_menu_delete_request(self, request_url):
		conn = urllib2.urlopen(request_url)

		try:
			content = conn.read()
		finally:
			if conn:
				try:
					conn.close()
				except:
					pass

		return content

weixin_menu_request = WeixinMenuRequest()

def _create_weixin_customerized_menu(user, menu_json):
	mp_user_access_token = _get_mpuser_access_token(user)
	request_url = _complete_wexin_menu_request_url(mp_user_access_token.access_token, WEIXIN_MENU_OP_CREATE)
	return weixin_menu_request.do_weixin_menu_create_request(request_url, menu_json)

def _delete_weixin_customerized_menu(user):
	mp_user_access_token = _get_mpuser_access_token(user)
	request_url = _complete_wexin_menu_request_url(mp_user_access_token.access_token, WEIXIN_MENU_OP_DELETE)
	return weixin_menu_request.do_weixin_menu_delete_request(request_url)

def _get_mpuser_access_token(user):
	mp_user = WeixinMpUser.objects.get(owner=user)
	return WeixinMpUserAccessToken.objects.filter(mpuser=mp_user)[0]

def _complete_wexin_menu_request_url(access_token, op):
	return "{}/{}?access_token={}".format(WEIXIN_MP_CUSTOMERIZED_MENU_REQUEST_URL_PREFIX, op, access_token)

