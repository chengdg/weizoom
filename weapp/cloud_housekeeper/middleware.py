# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from cloud_user_util import *
from models import *


#===============================================================================
# CloudSessionMiddleware : 获取当前请求的用户信息
# view中的代码可直接通过request.cloud_user获取当前请求的用户
#===============================================================================
class CloudSessionMiddleware(object):
	NEED_REMOVE_CLOUD_USER_SESSION_FLAG = 'need_remove_cloud_user_session'
	def process_request(self, request):
		request.cloud_user = get_request_cloud_user(request)
		if request.cloud_user is None:
			user_id = get_cloud_user_from_cookie(request)
			try:
				user = CloudUser.objects.get(id=user_id)
			except:
				request.META[self.NEED_REMOVE_CLOUD_USER_SESSION_FLAG] = True
				user = None
			request.cloud_user = user

		print request.cloud_user
		return None