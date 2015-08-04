# -*- coding: utf-8 -*-

__author__ = 'chuter'


from django.contrib.auth.decorators import login_required
from django.conf import settings

from core.jsonresponse import create_response
from core import apiview_util


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)
