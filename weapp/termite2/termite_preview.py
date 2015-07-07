# -*- coding: utf-8 -*-

import json
import qrcode, os

from weixin2 import export
from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import termite2.mode
cd weixinls as termite_models
from termite import pagestore as pagestore_manager

from weixin.user.module_api import get_mp_qrcode_img
from django.conf import settings

class TermitePreview(resource.Resource):
    """
    预览
    """
    app = 'termite2'
    resource = 'termite_preview'

    @login_required
    def get(request):
        """
        预览
        """
        object_id = request.GET.get('id', None)
        is_view_editing_data = request.GET.get('view_editing_data', False)
        preview_url = u'/termite2/webapp_page/?project_id={}&woid={}'.format(object_id, request.user.id)
        if is_view_editing_data:
            preview_url += '&page_id=preview'

        c = RequestContext(request, {
            'object_id': object_id,
            # 'head_img': get_mp_qrcode_img(request.user.id),
            'qrcode_url': get_preview_url(request.get_host(), preview_url, object_id),
            'head_img': get_preview_url_qrcode(request.get_host(), preview_url, object_id),                        
            'preview_url': preview_url
        })
        return render_to_response('termite2/termite_preview.html', c)

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


def get_preview_url(host, url, object_id):
    return u'http://{}{}'.format(host, url)

def get_preview_url_qrcode(host, url, object_id):
    url = u'http://{}{}'.format(host, url)
    return _create_qrcode(url, object_id)


def _create_qrcode(url, object_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    img = qr.make_image()
cd we
    file_name = '{}.png'.format(object_id)
    dir_path = os.path.join(settings.UPLOAD_DIR, '../termite_preview')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path, file_name)
    img.save(file_path)

    return '/static/termite_preview/%s' % file_name
