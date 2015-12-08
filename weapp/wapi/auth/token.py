# -*- coding: utf-8 -*-

#import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
from wapi.decorators import param_required
#from django.shortcuts import render_to_response
#from django.db.models import F

from django.contrib import auth

from core import api_resource
#from core import paginator
from core.jsonresponse import create_response
#from core.charts_apis import create_line_chart_response

from mall.models import *
#from utils import dateutil as util_dateutil
#import pandas as pd
#from core import dateutil
#from webapp import models as webapp_models
#from webapp import statistics_util as webapp_statistics_util
from core.charts_apis import *
#from django.conf import settings
#import stats.util as stats_util
#from stats.models import BrandValueHistory

#from core.exceptionutil import unicode_full_stack
#from watchdog.utils import watchdog_error, watchdog_warning
from wapi.models import OAuthToken
import datetime as dt
import hashlib
import logging

TOKEN_EXPIRE_AFTER_DAYS = 90

class AuthToken(api_resource.ApiResource):
	"""
	授权token(类似OAuth授权)
	"""
	app = 'open'
	resource = 'auth_token'

	@staticmethod
	def _get_token_string(user_id):
		md5 = hashlib.md5(dt.datetime.now().strftime("%Y-%m-%d %H:%H:%S")+str(user_id)).hexdigest()
		return "WZT10_"+md5

	@param_required(['username', 'password'])
	def post(args):
		"""
		输入用户名、授权密码获取授权token
		"""
		username = args['username']
		password = args['password']

		user = auth.authenticate(username=username, password=password)
		token = None
		now = dt.datetime.now()
		errMsg = "Unknown error"
		if user:
			if user.is_active:
				# 如果存在token，则返回token；否则创建token
				tokens = OAuthToken.objects.filter(user=user, expire_time__gt=now)
				if tokens.count()>0:
					token = tokens[0]
				else:
					try:
						token_str = AuthToken._get_token_string(user.id)
						token = OAuthToken.objects.create(
							user=user,
							token=token_str,
							expire_time=now + dt.timedelta(days=TOKEN_EXPIRE_AFTER_DAYS)
						)
					except Exception as e:
						logging.error(str(e))
						token = None
		else:
			errMsg = "Incorrect username or password."
		if token:
			data = {
				'access_token': token.token,
			}
		else:
			data = {
				'message': errMsg
			}
		return data
