# -*- coding: utf-8 -*-

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


class AccessGrant(resource.Resource):
	"""
	授权token(类似OAuth授权)
	"""
	app = 'wapi'
	resource = 'access_grant'

	@login_required
	def api_get(request):
		"""
		输入用户名、授权密码授权
		"""
		response = create_response(200)
		return response.get_response()
