# -*- coding: utf-8 -*-


import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from core import emotion
from core import resource
from core import paginator
from core.jsonresponse import create_response, JsonResponse
from core.stringutil import cut_string
from core.dateutil import get_datetime_before_by_hour

from weixin2 import export
from weixin2.models import get_system_user_binded_mpuser, WeixinUser, DEFAULT_ICON, Message, CollectMessage

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV
CUT_STRING_LEN = 20
DATETIME_BEFORE_HOURS = 48


class MessageCollect(resource.Resource):
    """
    表示消息加星标的状态
    """
    app = 'new_weixin'
    resource = 'message_collect'

    @login_required
    def api_post(request):
            """
            更新消息星标状态
            """
            #print("POST: {}".format(request.POST))
            assert 'message_id' in request.POST
            assert 'status' in request.POST
            response = create_response(201)
            if request.POST:
                message_id = request.POST.get('message_id', None)
                current_status = request.POST.get('status', None)
                status = '1' if current_status == '0' else '0'

                if message_id and status and int(message_id) != 0:
                    if CollectMessage.objects.filter(message_id=message_id).count() > 0:
                        CollectMessage.objects.filter(message_id=message_id).update(status=int(status))
                    else:
                        CollectMessage.objects.create(message_id=message_id, status=int(status), owner=request.user)
                    response = create_response(200)

            return response.get_response()

