# -*- coding: utf-8 -*-

import json

from weixin2 import export
from core import resource
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import weixin2.models as weixin_models
import weixin2.module_api as weixin_module_api

from weixin.user.module_api import get_mp_qrcode_img


FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class NewsPreview(resource.Resource):
    """
    图文(news)预览
    """
    app = 'new_weixin'
    resource = 'news_preview'

    @login_required
    def get(request):
        """
        获取图文信息
        """
        material_id = request.GET.get('id', None)
        if material_id:
            material = weixin_models.Material.objects.get(id=material_id)
            newses = list(weixin_models.News.objects.filter(material_id=material_id))
            news_count, newses_object = weixin_module_api.get_newses_object(newses, True)
        else:
            material = None
            newses_object = []

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
            'third_nav_name': export.ADVANCE_MANAGE_MATERIAL_NAV,
            'material_id': material_id,
            'newses': json.dumps(newses_object),
            'material': material,
            'head_img': get_mp_qrcode_img(request.user.id)
        })
        return render_to_response('weixin/advance_manage/news_preview.html', c)
