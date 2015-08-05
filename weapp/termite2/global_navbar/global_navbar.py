# -*- coding: utf-8 -*-

import json
import qrcode, os

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import termite2.models as termite_models
from django.conf import settings
from termite2 import export


FIRST_NAV = export.WEPAGE_FIRST_NAV
class GlobalNavbar(resource.Resource):
    """
    导航
    """
    app = 'termite2'
    resource = 'global_navbar'

    @login_required
    def get(request):
        """
        导航
        """
        # object_id = request.GET.get('id', None)
        # is_view_editing_data = request.GET.get('view_editing_data', False)
        # preview_url = u'/termite2/webapp_page/?project_id={}&woid={}'.format(object_id, request.user.id)
        # if is_view_editing_data:
        #     preview_url += '&page_id=preview'

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_wepage_second_navs(request),
            'second_nav_name': export.WEPAGE_GLOBAL_NAVBAR_NAV,
        })
        # return render_to_response('termite2/pages.html', c)
        return render_to_response('termite2/global_navbar_editor.html', c)

    @login_required
    def api_put(request):
        """
        预览
        """
        pagestore = pagestore_manager.get_pagestore('mongo')
        project_id = request.POST['project_id']
        page = json.loads(request.POST['page_json'])
        pagestore.save_page(project_id, "preview", page)

        response = create_response(200)
        return response.get_response()        

