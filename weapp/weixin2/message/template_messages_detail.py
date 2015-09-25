# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
import weixin2.models as weixin_models
from market_tools.tools.template_message.models import *
from core import resource
from core import paginator
from core.jsonresponse import create_response

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV




class TemplateMessagesDetail(resource.Resource):
    """
    模板式消息详情
    """
    app = 'new_weixin'
    resource = 'template_messages_detail'

    @login_required
    def get(request):
        """
            获取指定ID的模板消息详情的内容
        """
        template_detail_id = int(request.GET.get('template_detail_id'))
        message_detail = MarketToolsTemplateMessageDetail.objects.get(id=template_detail_id)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_MESSAGE_SECOND_NAV,
            'third_nav_name': export.MESSAGE_TEMPLATE_MESSAGE_NAV,
            'message_detail': message_detail
        })
        return render_to_response('weixin/message/template_messages_detail.html', c)

    @login_required
    def api_post(request):
        """
            修改指定ID的模板消息详情的内容
        """
        id = request.POST.get('id')
        template_id = request.POST.get('template_id', '')
        first_text = request.POST.get('first_text', '')
        remark_text = request.POST.get('remark_text', '')

        response = create_response(200)
        if len(first_text) == 0 or len(remark_text) == 0:
            return response.get_response()

        message_detail = MarketToolsTemplateMessageDetail.objects.get(id=id)
        message_detail.template_id = template_id
        message_detail.first_text = first_text
        message_detail.remark_text = remark_text
        message_detail.save()

        return response.get_response()