# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
import weixin2.models as weixin_models
from core import resource
from core import paginator
from core import emotion
from core.jsonresponse import create_response
from util import *

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class KeywordRules(resource.Resource):
    app = 'new_weixin'
    resource = 'keyword_rules'

    @login_required
    @mp_required
    def get(request):
        """
        关键词自动回复的消息

        @param patterns 关键词列表
        @param answer 回复内容列表
        """
        FAKE_DATA=False
        if FAKE_DATA:
            items = [{
                "id": 1,
                "rule_name": "未命名规则1",
                "patterns": [{"keyword":"你好","type":1},{"keyword":"hi","type":0}],  # 1表示部分匹配，0表示精确匹配
                "answer": [{
                    "content":"欢迎光临","type":"text"
                }, {
                    "content":"1","type":"text"
                },{
                    "content":"2","type":"news","newses":[{"id":1, "title":"标题一"},{"id":2, "title":"标题二"}]
                }],
            }, {
                "id": 2,
                "rule_name": "未命名规则2",
                "patterns": [{"keyword":"你好","type":1},{"keyword":"hi","type":0}],  # 1表示部分匹配，0表示精确匹配
                "answer": [{
                    "type":"text", "content":"欢迎光临"
                }, {
                    "type":"text", "content":"1"
                },{
                    "type":"news", "content":"2","newses":[{"id":1, "title":"标题一"},{"id":2, "title":"标题二"}]
                }],
            }]


        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_MESSAGE_SECOND_NAV,
            'third_nav_name': export.MESSAGE_AUTO_REPLY_NAV,
            #'rules': items,
            #'jsons': jsons
        })
        return render_to_response('weixin/message/keyword_rules.html', c)

    @login_required
    @mp_required
    def api_get(request):
        keyword = request.GET.get('keyword', '')
        keywords = request.GET.get('keywords', '')
        if keyword != '':
            msg = None
            response = create_response(200)

            try:
                words = json.loads(keywords)
                if keyword in words:
                    msg = u'关键词“%s”已经存在' % keyword
                else:
                    has_duplicate, duplicate_patterns = has_duplicate_pattern(request.manager, keyword)
                    if has_duplicate:
                        msg = u'关键词“%s”已经存在' % keyword
            except:
                print 'invalid keywords:',keywords
                has_duplicate, duplicate_patterns = has_duplicate_pattern(request.manager, keyword)
                if has_duplicate:
                    msg = u'关键词“%s”已经存在' % keyword

            response.data = {
                'msg': msg
            }
            return response.get_response()
        else:
            #获取当前页数
            cur_page = int(request.GET.get('page', '1'))
            #获取每页个数
            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))

            raw_rules = Rule.get_keyword_reply_rule(request.manager)
            rules = []

            is_search =False
            #搜索只搜关键词
            query = request.GET.get('query', None)
            if query and len(query) > 0 and query != 'undefined':
                is_search = True
                for rule in raw_rules:
                    is_valid = False
                    rule = rule.format_to_dict()
                    for pattern in rule['patterns']:
                        if query in pattern['keyword']:
                            is_valid = True
                    if is_valid:
                        rules.append(rule)
            else:
                for rule in raw_rules:
                    rules.append(rule.format_to_dict())


            pageinfo, rules = paginator.paginate(rules, cur_page, count_per_page, None)

            jsons = [{
                "name": "rule", "content": rules
            }]
            response = create_response(200)
            response.data = {
                'items': rules,
                'is_search' : True,
                'jsons': jsons,
                'is_search': is_search,
                'pageinfo': paginator.to_dict(pageinfo),
                'sortAttr': ''
            }

        return response.get_response()

    @login_required
    @mp_required
    def api_put(request):
        """
        创建关键词自动回复消息
        """
        rule_name = request.POST.get('rule_name', '')
        patterns = request.POST.get('patterns', None)
        if not patterns:
            raise Http404('invalid keywords')

        answer = request.POST.get('answer', '')
        material_id = int(request.POST.get('material_id', 0))

        if material_id == 0:
            type = TEXT_TYPE
        else:
            type = NEWS_TYPE

        rule = Rule.objects.create(
            owner = request.manager,
            type = type,
            rule_name = rule_name,
            patterns = patterns,
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
        更新关键词自动回复消息的规则
        """
        id = int(request.POST.get('id', -1))
        if id == -1:
            response = create_response(400)
            response.errMsg = u'关键词自动回复消息id错误: %d，无法更新关键词自动回复消息' % id
        else:
            rule_name = request.POST.get('rule_name', '')
            patterns = request.POST.get('patterns', None)
            if not patterns:
                raise Http404('invalid keywords')

            has_duplicate, duplicate_patterns = has_duplicate_pattern(request.manager, patterns, id)

            if has_duplicate:
                response = create_response(601)
                response.errMsg = u'下列关键词已经存在: %s' % duplicate_patterns[0]
                return response.get_response()

            answer = request.POST.get('answer', '')
            #将answer中的表情img标签转化为文字符号 by Eugene
            answers = json.loads(answer)
            for data in answers:
                if data['type'] == "text":
                    data['content'] = emotion.change_img_to_emotion(data['content'])
            answer = json.dumps(answers)
            material_id = int(request.POST.get('material_id', 0))

            if material_id == 0:
                type = TEXT_TYPE
            else:
                type = NEWS_TYPE

            Rule.objects.filter(id=id).update(
                rule_name = rule_name,
                patterns = patterns,
                answer = answer,
                material_id = material_id,
                type = type
            )

            response = create_response(200)
        return response.get_response()


    @login_required
    @mp_required
    def api_delete(request):
        """
        删除关键词自动回复规则
        """
        id = int(request.POST.get('id', -1))
        Rule.objects.filter(owner=request.manager, id=id).delete()
        return create_response(200).get_response()
