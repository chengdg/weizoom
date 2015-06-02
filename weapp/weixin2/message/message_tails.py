# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
from weixin2.models import *
from core import resource
from core import paginator
from core.jsonresponse import create_response

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV

class MessageTails(resource.Resource):
    app = 'new_weixin'
    resource = 'message_tails'

    @login_required
    @mp_required
    def get(request):
        """
        获取消息小尾巴

        POST例子：
        ~~~~~~~~~~~~~~~~~~~~~~~{.c}
        "tail":"这是一个小尾巴~~~~~"
        "is_active" = 1
        ~~~~~~~~~~~~~~~~~~~~~~~
        """
        FAKE_DATA=False
        if FAKE_DATA:
            tail = {
                        "tail": u'这是一个小尾巴~~~~~',
                        "is_active": 1
                    }
        else:
            tail = None
            try:
                tail = Tail.objects.get(owner=request.user)
            except:
                pass

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_message_second_navs(request),
            'second_nav_name': export.MESSAGE_AUTO_REPLY_NAV,
            'tail': tail,
        })
        return render_to_response('weixin/message/message_tails.html', c)

    @login_required
    @mp_required
    def api_put(request):
        """
        创建消息小尾巴
        """

        tail = request.POST.get('tail', '')
        is_active = int(request.POST.get('is_active', 1))

        if Tail.objects.filter(owner=request.user).count() < 1:
            Tail.objects.create(
                owner = request.user,
                tail = tail,
                is_active = is_active,
            )

        response = create_response(200)
        response.data = {
            'redirect_url': '/new_weixin/message_tails/'
        }
        return response.get_response()

    @login_required
    @mp_required
    def api_post(request):
        """
        更新消息小尾巴
        """

        tail_id = int(request.POST.get('id', -1))
        if tail_id == -1:
            response = create_response(400)
            response.errMsg = u'关注自动回复消息id错误: %d，无法更新关注自动回复消息' % tail_id
        else:
            tail = request.POST.get('tail', '')
            is_active = int(request.POST.get('is_active', 1))

            Tail.objects.filter(id=tail_id).update(
                owner = request.user,
                tail = tail,
                is_active = is_active,
            )

            response = create_response(200)
            response.data = {
                'redirect_url': '/new_weixin/message_tails/'
            }
        return response.get_response()
