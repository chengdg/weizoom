# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import datetime

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from cloud_required import cloud_housekeeper_required
import models
from stats.manage import manage_summary as manage_util
import stats.util as stats_util
import pandas as pd
from core.charts_apis import create_line_chart_response

from stats.manage.brand_value_utils import get_brand_value


class CloudBrandValues(resource.Resource):
    """
    云管家登陆
    """
    app = 'cloud_housekeeper'
    resource = 'brand_values'

    @cloud_housekeeper_required
    def api_get(request):
        """
        返回微品牌价值的EChart数据
        """        
        webapp_id = request.cloud_user.get_webapp_id()
        periods = 20
        freq = 'W'
        end_date = datetime.datetime.now()
        date_range = pd.date_range(end=end_date, periods=periods, freq=freq)
        date_list = []
        values = []
        for date in date_range:
            date_time = date.to_datetime()
            date_str = date_time.strftime('%Y-%m-%d')  # 将pd.Timestamp转成datetime
            date_list.append(date_time.strftime('%m/%d'))
            values.append(get_brand_value(webapp_id, date_str))

        print("date_list: {}".format(date_list))

        response = create_line_chart_response(
            "",
            "",
            #['2010-10-10', '2010-10-11', '2010-10-12', '2010-10-13'],
            date_list,
            [{
                "name": "品牌价值",
                "values" : values
            }]
            )
        return response