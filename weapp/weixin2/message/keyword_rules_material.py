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


class KeywordRulesMaterial(resource.Resource):
    app = 'new_weixin'
    resource = 'keyword_rules_material'

    @login_required
    @mp_required
    def api_get(request):
        """
        获取群发消息的“已发送消息”
        """
        material_id = int(request.GET.get('materialId', '-1'))
        material = None

        if material_id > 0:
            news_list = News.get_news_by_material_id(material_id)
            material = {}
            newses = []
            for news in news_list:
                _news = {}
                _news['id'] = news.id
                _news['title'] = news.title
                newses.append(_news)

            material['id'] = material_id
            material['newses'] = newses

        if material:
            response = create_response(200)
            response.data = {
                'material': material,
            }
        else:
            response = create_response(400)
            response.errMsg = u'没有获取到图文数据'

        return response.get_response()