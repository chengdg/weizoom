# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json, time, datetime
import random, string

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from cloud_required import cloud_housekeeper_required
from core import dateutil
from models import CloudReport

class CloudReports(resource.Resource):
    """
    云管家登陆
    """
    app = 'cloud_housekeeper'
    resource = 'reports'

    @cloud_housekeeper_required
    def get(request):
        """
        记录
        """

        webapp_id = request.cloud_user.get_webapp_id()
        # print '+++++++++++++++++++++++++1'

        weeks = list(CloudReport.get_weeklys_by_webapp_id(webapp_id))
        months = list(CloudReport.get_monthlys_by_webapp_id(webapp_id))
        c = RequestContext(request, {
            'page_title': '云管家',
            'weeks': weeks,
            'months': months
        })
        return render_to_response('cloud_housekeeper/reports.html', c)



# def get_months(start_str, end_date=time.time()):
#     start_date = time.strftime('%Y-%m-%d', start_str)
    # print start_date

    # datetime.
    # datetime.timedelta(months=3) 
    # datetime.date(datetime.date.today().year,datetime.date.today().month,1) 
    # datetime.date.().month -1




# def get_weeds(start_str, end_date=time.time()):
#     start_date = time.strftime('%Y-%m-%d', start_str)



# if __name__ == '__main__':
#     print 'aaaaa'
#     get_months(start_str="2015-1-1")
