# -*- coding: utf-8 -*-

import json
import qrcode, os

from weixin2 import export
from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import termite2.models as termite_models
from termite import pagestore as pagestore_manager

from weixin.user.module_api import get_mp_qrcode_img
from django.conf import settings

class AppPreview(resource.Resource):
	"""
	预览
	"""
	app = 'termite2'
	resource = 'app_preview'

	@login_required
	def get(request):
		"""
		预览
		"""
		preview_url = request.GET.get('preview_url', '')
		preview_url += '&isPC=1'
		is_view_editing_data = request.GET.get('view_editing_data', False)
		if is_view_editing_data:
			preview_url += '&page_id=preview'
		print preview_url,"preview_url"

		c = RequestContext(request, {
			'preview_url': preview_url
		})
		return render_to_response('termite2/app_preview.html', c)

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
	file_name = '{}.png'.format(object_id)
	dir_path = os.path.join(settings.UPLOAD_DIR, '../termite_preview')
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	file_path = os.path.join(dir_path, file_name)
	img.save(file_path)

	return '/static/termite_preview/%s' % file_name
