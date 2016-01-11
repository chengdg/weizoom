# -*- coding: utf-8 -*-

import json
import os
import sys
import zipfile
import shutil
import qrcode
import StringIO

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models
from termite import pagestore as pagestore_manager

class QRCode(resource.Resource):
	app = 'termite2'
	resource = 'qrcode_image'

	@login_required
	def get(request):
		"""
		创建二维码
		"""
		data = request.GET['data']
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4
		)
		qr.add_data(data)
		img = qr.make_image()

		output = StringIO.StringIO()
		img.save(output)
		print output.getvalue()

		response = HttpResponse(output.getvalue(), 'image/png')
		if 'download' in request.GET:
			response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
		return response