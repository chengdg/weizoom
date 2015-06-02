# -*- coding: utf-8 -*-

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
from .util import *
from weixin2.advance_manage.util import get_members
from modules.member.models import Member

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV

class MassSendingMessages(resource.Resource):
    """
    群发消息的资源
    """
    app = 'new_weixin'
    resource = 'mass_sending_messages'

    @login_required
    @mp_required
    def get(request):
        """
        群发消息
        """
        webapp_id = request.user_profile.webapp_id
        sent_count = UserSentMassMsgLog.success_count(webapp_id)
        groups = get_member_groups(webapp_id)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_message_second_navs(request),
            'second_nav_name': export.MESSAGE_MASS_SENDING_NAV,
            'sent_count': sent_count,
            'groups': groups,
            'mode': 'mass_sending'
        })
        return render_to_response('weixin/message/mass_sending_messages.html', c)

    @login_required
    @mp_required
    def post(request):
        """
        粉丝管理页面提交过来的群发请求
        """
        webapp_id = request.user_profile.webapp_id

        params = request.POST.get('params', None)
        
        category = None
        status = None
        sex = None
        filter_value = None
        member_list = []
        member_ids_str = ''
        mode = ''  #发送模式

        if params and len(params) > 0:
            if 'filter_value' in params:
                #params例子： category=全部&status=全部&sex=全部&filter_value=name:jobs
                mode = 'filter'  #向全部筛选出来的人群发
                param2value = {}
                fields = params.split('&')
                for field in fields:
                    _fields = field.split('=')
                    param2value[_fields[0]] = _fields[1]

                category = param2value['category'];
                status = param2value['status'];
                sex = param2value['sex'];
                filter_value = param2value['filter_value'];

                members = get_members(request, filter_value, '-id')
            else:
                #params例子： member_ids=1|2|3
                fields = params.split('=')
                ids = []
                for id in fields[1].split('|'):
                    if id != '':
                        ids.append(int(id))
                members = Member.objects.filter(webapp_id = request.user_profile.webapp_id, is_subscribed = True, is_for_test = False, id__in = ids).order_by('-id')

            for member in members:
                if member.is_subscribed:
                    id2name = {}
                    id2name['id'] = member.id
                    member_ids_str = member_ids_str + str(member.id) + '|'
                    if mode != 'filter':
                        nickname = member.username_for_html
                        if nickname == '':
                            nickname = '无昵称用户'
                        id2name['name'] = nickname
                    member_list.append(id2name)

        sent_count = UserSentMassMsgLog.success_count(webapp_id)

        c = RequestContext(request, {
            'first_nav_name': export.ADVANCE_MANAGE_FIRST_NAV,
            'second_navs': export.get_advance_manage_second_navs(request),
            'second_nav_name': export.ADVANCE_MANAGE_FANS_NAV,
            'sent_count': sent_count,
            'category': category,
            'status': status,
            'sex': sex,
            'mode': mode,
            'member_list': member_list,
            'member_ids_str': member_ids_str,
            'number': len(member_list),
        })

        return render_to_response('weixin/message/mass_sending_messages.html', c)


    @login_required
    @mp_required
    def api_get(request):
        """
        获取分组数据
        """
        user_profile = request.user_profile
        webapp_id = user_profile.webapp_id

        group_type = request.GET.get('group_type', 'member')
        groups = []
        if group_type == 'member':
            groups = get_member_groups(webapp_id)
        else:
            groups = get_fans_groups(webapp_id)

        response = create_response(200)
        response.data = {
            'groups': groups
        }
        return response.get_response()

    @login_required
    @mp_required
    def api_post(request):
        """
        发送群发消息
        """
        content = request.POST.get('content')
        if content is None or content == '':
            response = create_response(402)
            response.errMsg = u'群发内容不能为空'
            return response.get_response()

        send_type  = request.POST.get('send_type')
        if send_type is None or send_type == '':
            response = create_response(403)
            response.errMsg = u'发送类型不能为空'
            return response.get_response()

        is_from_fans_list = False
        id_array = []
        result = None

        member_ids = request.POST.get('member_ids', None)
        ids = request.POST.get('ids', None)
        response = create_response(200)
        webapp_id = request.user_profile.webapp_id
        openid_list = []

        #从粉丝管理页面过来的群发请求
        if member_ids and member_ids != '' and member_ids != 'undefined':
            is_from_fans_list = True
            for member_id in member_ids.split('|'):
                if len(member_id) > 0:
                    id_array.append(int(member_id))
        elif ids and ids != '' and ids != 'undefined' and ids != '[]':
            is_from_fans_list = True
            try:
                for member_id in json.loads(ids):
                    id_array.append(int(member_id))
            except Exception, e:
                print u'群发消息异常，mass_sending_messages:', e
        
        if is_from_fans_list:
            members = Member.objects.filter(webapp_id = webapp_id, is_subscribed = True, is_for_test = False, id__in = id_array)
            for member in members:
                openid_list.append(member.member_open_id)
        else:  #从群发消息页面过来的群发请求
            group_id = request.POST.get('group_id')
            group_type = request.POST.get('group_type')
            if group_id is None or group_id == '':
                response = create_response(401)
                return response.get_response()

            group_id = int(group_id)
            if group_type == 'member':
                #商城会员
                if group_id == -1:
                    #当group_id等于-1时发送给全部会员
                    openid_list = get_openid_list_by_webapp_id(webapp_id)
                else:
                    openid_list = get_openid_list(group_id)
            else:
                #微信粉丝
                members = None
                if group_id == -1:
                    members = Member.get_members(webapp_id)
                else:
                    id_array = FanHasCategory.get_fan_id_list_by_category_id(group_id)
                    members = Member.objects.filter(webapp_id = webapp_id, is_subscribed = True, is_for_test = False, id__in = id_array)
                
                for member in members:
                    openid_list.append(member.member_open_id)

        if len(openid_list) < 2:
            response = create_response(405)
            response.errMsg = u'群发目标用户数量不能少于2个'
            return response.get_response()

        if send_type != 'news':
            result = send_mass_text_message_with_openid_list(request.user_profile, openid_list, content)
        else:
            material_id = int(content)
            result = send_mass_news_message_with_openid_list(request.user_profile, openid_list, material_id)

        if result:
            response = create_response(200)
        else:
            response = create_response(404)
            response.errMsg = u'群发失败，请检查token'

        return response.get_response()
