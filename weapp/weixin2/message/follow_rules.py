# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from weixin2 import export
from weixin2.models import *
from core import resource
from util import *
import json

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class FollowRules(resource.Resource):
    app = 'new_weixin'
    resource = 'follow_rules'

    @login_required
    @mp_required
    def get(request):
        """
        关注后自动回复消息的规则资源

        @param answer 文本回复内容
        @param material_id 图文回复内容的id
        
        ```说明```：
         * 当回复类型为文本消息时，answer的值一定不为空，material_id一定等于0
         * 当回复类型为图文消息时，material_id一定大于0，answer的值一定为空

        如果answer值为空且material_id等于0，说明关注时没有自动回复
        """
        FAKE_DATA=False
        if FAKE_DATA:
            rule = [{
                "id": 1,
                "answer": {"content":"1","type":"news","newses":[{
                    "id": 1,
                    "title": "title1"
                }, {
                    "id": 2,
                    "title": "title2"
                }]}, 
                "material_id": 1
            }]
        else:
            rule =None
            try:
                raw_rule = Rule.objects.get(owner=request.manager, type=FOLLOW_TYPE)
                if not raw_rule.answer or raw_rule.answer == '':
                    #当内容为空时删除该条记录
                    Rule.objects.filter(owner=request.manager, type=FOLLOW_TYPE).delete()
                else:
                    rule = raw_rule.format_to_dict()
            except Exception, e:
                print e

        jsons = [{
            "name": "rule", "content": rule
        }]

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_MESSAGE_SECOND_NAV,
            'third_nav_name': export.MESSAGE_AUTO_REPLY_NAV,
            'rule': rule,
            'jsons': jsons
        })
        return render_to_response('weixin/message/follow_rules.html', c)

    @login_required
    @mp_required
    def api_put(request):
        """
        创建关注自动回复消息
        """
        answer = request.POST.get('answer', '')
        material_id = request.POST.get('material_id', 0)

        rule = None
        if Rule.objects.filter(owner=request.manager, type=FOLLOW_TYPE).count() < 1:
            rule = Rule.objects.create(
                owner = request.manager,
                type = FOLLOW_TYPE,
                answer = answer,
                material_id = material_id
            )

        if rule:
            response = create_response(200)
        else:
            response = create_response(400)

        return response.get_response()

    @login_required
    @mp_required
    def api_post(request):
        """
        更新关注自动回复消息
        """
        id = int(request.POST.get('id', -1))
        if id == -1:
            response = create_response(400)
            response.errMsg = u'关注自动回复消息id错误: %d，无法更新关注自动回复消息' % id
        else:
            answer = request.POST.get('answer', '')
            material_id = request.POST.get('material_id', 0)

            # 更新规则
            Rule.objects.filter(id=id).update(
                answer = answer,
                material_id = material_id
            )
            response = create_response(200)

        return response.get_response()

    @login_required
    @mp_required
    def api_delete(request):
        """
        删除关注自动回复规则
        """
        id = int(request.POST.get('id', -1))
        Rule.objects.filter(owner=request.manager, id=id, type=FOLLOW_TYPE).delete()
        return create_response(200).get_response()
