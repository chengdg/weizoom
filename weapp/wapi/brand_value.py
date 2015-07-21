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

from wapi.decorators import wapi_access_required

from stats.manage.brand_value_utils import get_brand_value

from utils import dateutil as utils_dateutil

class BrandValue(resource.Resource):
	"""
	获取微品牌价值的接口
	"""
	app = 'wapi'
	resource = 'brand_value'

	@wapi_access_required
	def api_get(request):
		"""
		获取微品牌价值

		@param wid webapp_id
		@param dates 日期列表，多日期用逗号(,)分隔。默认是当天。
		"""
		webapp_id = request.REQUEST.get('wid')
		print("webapp_id: {}".format(webapp_id))
		dates = request.REQUEST.get('dates')
		if dates is None or len(dates)<1:
			dates = [ utils_dateutil.date2string(utils_dateutil.now()) ]
		else:
			dates = dates.split(',')

		values = [ {"date":date_str, "bv":get_brand_value(webapp_id, date_str)} for date_str in dates ]

		response = create_response(200)
		response.data = {
			"values": values
		}
		return response.get_response()
