# -*- coding: utf-8 -*-

from core import apiview_util
from core.jsonresponse import JsonResponse, create_response
from core import paginator
from models import *

from django.contrib.auth.decorators import login_required

from modules.member.module_api import get_member_by_id_list


def call_api(request):
    api_function = apiview_util.get_api_function(request, globals())
    return api_function(request)