# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from cloud_user_util import *
from models import *
from account.url_util import get_webappid_from_request, is_request_for_api, is_request_for_webapp, is_request_for_webapp_api, is_request_for_editor, is_pay_request, is_request_for_weixin, is_paynotify_request, is_request_for_pcmall, is_js_config

#===============================================================================
# CloudSessionMiddleware : 获取当前请求的用户信息
# view中的代码可直接通过request.cloud_user获取当前请求的用户
#===============================================================================
class CloudSessionMiddleware(object):
	NEED_REMOVE_CLOUD_USER_SESSION_FLAG = 'need_remove_cloud_user_session'
	def process_request(self, request):
		if is_pay_request(request):
			return None

		#对于支付请求，不处理
		if request.is_access_pay or request.is_access_paynotify_callback:
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#webapp 请求不处理 add by bert 
		if request.is_access_webapp or request.is_access_pcmall or request.is_access_webapp_api:
			return None

		if '/weixin/js/config' in request.get_full_path():
			return None

		request.cloud_user = get_request_cloud_user(request)
		if request.cloud_user is None:
			user_id = get_cloud_user_from_cookie(request)
			user = None
			
			if user_id:
				try:
					user = CloudUser.objects.get(id=user_id)
				except:
					request.META[self.NEED_REMOVE_CLOUD_USER_SESSION_FLAG] = True

			request.cloud_user = user

		return None