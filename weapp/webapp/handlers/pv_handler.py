# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import base64
import random

from modules.member.visit_session_util import get_request_url

# def handle(request):
# 	request_url = get_request_url(request)
# 	get = {}
# 	get.update(request.GET)
# 	cookies = {}
# 	cookies.update(request.COOKIES)
# 	data = {
# 		'full_path': request.get_full_path(),
# 		'url': request_url,
# 		'GET': get,
# 		'COOKIES': cookies,
# 		'data': {
# 			'app_id': request.app.id if request.app else -1,
# 			'user_id': request.user.id if request.user.is_authenticated() else -1,
# 			'is_user_from_mobile_phone': request.user.is_from_mobile
# 			'is_user_from_weixin': request.user.is_from_weixin
# 		}
# 	}
# 	#print json.dumps(data, indent=4)
# 	from services import service_manager
# 	service_manager.call_service('page_visit', data)


# 		# token = get_social_account_token(request, '')
# 		# #add by bert 当token为null的时候是否统计?
# 		# try:
# 		# 	PageVisitLog.objects.create(
# 		# 		webapp_id = request.app.appid,
# 		# 		token = token,
# 		# 		is_from_mobile_phone = request.user.is_from_mobile,
# 		# 		url = request_url
# 		# 	)
# 		# except:
# 		# 	pass


