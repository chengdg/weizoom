# -*- coding: utf-8 -*-
"""
有关账号的API
"""

#import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
#from django.db.models import F

from core import resource
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

from wapi.decorators import wapi_access_required

#from stats.manage.brand_value_utils import get_brand_value

#from utils import dateutil as utils_dateutil

from mall import models as mall_models

from django.contrib.auth.models import User


class WebappID(resource.Resource):
	"""
	获取WebAPP ID
	"""
	app = 'wapi'
	resource = 'webapp_id'

	@wapi_access_required
	def api_get(request):
		"""
		获取WebAPP ID

		@param username 用户名
		"""
		username = request.GET.get('username')
		user = User.objects.get(username=username)
		user.profile = UserProfile.objects.get(user=client.user)
		webapp_id = user.profile.webapp_id

		response = create_response(200)
		response.data = {
			"webapp_id": webapp_id,
			"username": user.username
		}
		return response.get_response()
