# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response
from django.db.models import F
from watchdog.utils import watchdog_warning, watchdog_error

from weixin2 import export
from weixin2.models import Rule, UNMATCH_TYPE
from core import resource
from core import paginator
from core.jsonresponse import create_response
from .util import is_valid_time

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV

class UnmatchRules(resource.Resource):
    app = 'new_weixin'
    resource = 'unmatch_rules'

    @login_required
    @mp_required
    def get(request):
        """
        未匹配自动回复的消息
        active_type等于2表示分时段开启，等于1表示始终开启，等于0表示禁用
        """
        FAKE_DATA=False
        rule = None
        if FAKE_DATA:
            rule = {
                "answer": [{"content":"欢迎光临","type":"text"},
                    {"content":"1","type":"text"},
                    {"content":"2","type":"news","newses":[{"id":1,"title":"标题一"},{"id":2,"title":"标题二"}]}], 
                "active_type": 2,
                "active_days":{'Mon':True,'Tue':False,'Wed':True,'Thu':True,'Fri':True,'Sat':False,'Sun':False},
                "start_hour": '00:00',
                "end_hour": '24:00',
                "material_id": 0
            }
            jsons = [{
                "name": "rule", "content": rule
            }]
        else:
            try:
                raw_rule = Rule.objects.get(owner=request.user, type=UNMATCH_TYPE)
                if not raw_rule.answer or raw_rule.answer == '':
                    #当内容为空时删除该条记录
                    Rule.objects.filter(owner=request.user, type=UNMATCH_TYPE).delete()
                else:
                    rule = raw_rule.format_to_dict()
            except:
                rule = None
        
        jsons = [{
            "name": "rule", "content": rule
        }]

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_message_second_navs(request),
            'second_nav_name': export.MESSAGE_AUTO_REPLY_NAV,
            'rule': rule,
            'jsons': jsons
        })
        return render_to_response('weixin/message/unmatch_rules.html', c)

    @login_required
    @mp_required
    def api_put(request):
        """
        创建未匹配自动回复消息
        """
        answer = request.POST.get('answer', '')
        material_id = request.POST.get('material_id', 0)

        active_type = int(request.POST.get('active_type', 2))
        active_days = request.POST.get('active_days', '')
        start_hour = request.POST.get('start_hour', '')
        end_hour = request.POST.get('end_hour', '')

        rule = None

        if is_valid_time(start_hour) and is_valid_time(end_hour):
            if Rule.objects.filter(owner=request.user, type=UNMATCH_TYPE).count() < 1:
                rule = Rule.objects.create(
                    owner = request.user,
                    active_type = active_type,
                    active_days = active_days,
                    start_hour = start_hour,
                    end_hour = end_hour,
                    type = UNMATCH_TYPE,
                    patterns = '',
                    answer = answer,
                    material_id = material_id
                )
            if rule:
                response = create_response(200)
            else:
                response = create_response(400)
                response.errMsg = u'保存规则失败'
        else:
            response = create_response(401)
            response.errMsg = u"非法起止时间：start_hour:%s,end_hour:%s" % (start_hour, end_hour)

        

        return response.get_response()

    @login_required
    @mp_required
    def api_post(request):
        """
        更新关键词自动回复消息
        """
        id = int(request.POST.get('id', -1))
        if id == -1:
            response = create_response(400)
            response.errMsg = u'托管消息id错误: %d，无法更新托管消息' % id
        else:
            answer = request.POST.get('answer', '')
            material_id = request.POST.get('material_id', 0)
            active_type = int(request.POST.get('active_type', 2))
            active_days = request.POST.get('active_days', '')
            start_hour = request.POST.get('start_hour', '')
            end_hour = request.POST.get('end_hour', '')

            if is_valid_time(start_hour) and is_valid_time(end_hour):
                Rule.objects.filter(id=id).update(
                    answer = answer, 
                    active_type = active_type,
                    active_days = active_days,
                    start_hour = start_hour,
                    end_hour = end_hour,
                    material_id = material_id
                )
                response = create_response(200)
            else:
                response = create_response(401)
                response.errMsg = u"非法起止时间：start_hour:%s,end_hour:%s" % (start_hour, end_hour)

        return response.get_response()
