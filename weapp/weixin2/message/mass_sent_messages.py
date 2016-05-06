#coding: utf8

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
import weixin2.models as weixin_models
from core import resource
from core import paginator
from core.jsonresponse import create_response
from modules.member.models import *
from datetime import timedelta, datetime, date
from member.util import *

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class MassSentMessages(resource.Resource):
    """
    表示群发消息中的“已发送消息”
    """
    app = 'new_weixin'
    resource = 'mass_sent_messages'

    @login_required
    @mp_required
    def get(request):
        """
        获取群发消息的“已发送消息”
        """

        """
        sent_messages = [{
            "id": 1,
            "message_type": 1, # 文本、图文、语音?
            "message_content": "已发送文本已发送文本已发送文本已发送文本已发送文本已发送文本已发送文本已发送文本",
            "status": 1, # 发送中、已发送、失败、已删除
            "created_at": "3月26日",
        }, {
            "id": 2,
            "message_type": 2, # 文本、图文、语音?
            "message_content": "已发送文本已发送文本已发送文本已发送文本已发送文本已发送文本已发送文本已发送文本",
            "status": 4, # 发送中、已发送、失败、已删除
            "created_at": "3月26日",
        }]
        """

        user_profile = request.user_profile
        webapp_id = user_profile.webapp_id
        sent_messages = UserSentMassMsgLog.objects.filter(webapp_id=webapp_id)

        for message in sent_messages:
            message.created_at = message.created_at.strftime('%m月%d日')
            message.message_content = emotion.change_emotion_to_img(message.message_content)

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_MESSAGE_SECOND_NAV,
            'third_nav_name': export.MESSAGE_MASS_SENDING_NAV,
            'sent_messages': sent_messages
        })
        return render_to_response('weixin/message/mass_sent_messages.html', c)

    @login_required
    @mp_required
    def api_get(request):
        """
        获取群发消息的“已发送消息”
        """
        #获取当前页数
        cur_page = int(request.GET.get('page', '1'))
        #获取每页个数
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))

        user_profile = request.user_profile
        webapp_id = user_profile.webapp_id
        sent_messages = UserSentMassMsgLog.objects.filter(webapp_id=webapp_id).order_by("-id")
        pageinfo, messages = paginator.paginate(sent_messages, cur_page, count_per_page, None)

        items = []

        member_group_id2name = {g.id: g.name for g in MemberTag.objects.filter(webapp_id=webapp_id)}
        
        for message in messages:
            # message.created_at = message.created_at.strftime('%m月%d日')
            # message.message_content = emotion.change_emotion_to_img(message.message_content)
            message_item = {}
            message_item['id'] = message.id
            message_item['webapp_id'] = message.webapp_id
            message_item['msg_id'] = message.msg_id
            message_item['sent_count'] = message.sent_count
            message_item['total_count'] = message.total_count
            message_item['filter_count'] = message.filter_count
            message_item['error_count'] = message.error_count
            message_item['status'] = message.status if (datetime.now() - message.created_at).days < 1 else 'send failed'
            message_item['message_type'] = message.message_type
            message_item['message_content'] = emotion.change_emotion_to_img(message.message_content)
            message_item['created_at'] = message.created_at.strftime('%m月%d日')
            message_item['group_id'] = message.group_id
            message_item['group_name'] = u"全部" if message.group_id == -1 else member_group_id2name[message.group_id]

            if message.message_type == 1:
                newses = News.get_news_by_material_id(int(message.message_content))
                news_array = []
                if len(newses) == 0:
                    news_array.append({"title": '图文已删除'})
                    message_item['message_content'] = -1
                else:
                    for news in newses:
                        news_array.append({"title": news.title})
                message_item['newses'] = news_array
            items.append(message_item)

        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': ''
        }

        return response.get_response()

    @login_required
    @mp_required
    def api_post(request):
        """
        删除已发送消息日志
        """
        #只能删除图文消息
        message_type = request.POST.get('message_type')
        
        if message_type is None or message_type != '1':
            response = create_response(400)
            return response.get_response()

        msg_id = request.POST.get('msg_id')
        if msg_id is None or msg_id == '':
            response = create_response(401)
            return response.get_response()

        result = delete_mass_message(request.user_profile, msg_id)

        if result:
            response = create_response(200)
        else:
            response = create_response(402)

        return response.get_response()
