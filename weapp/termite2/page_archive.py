# -*- coding: utf-8 -*-

import json
import zipfile
import os
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models
from termite import pagestore as pagestore_manager

class PageArchive(resource.Resource):
	app = 'termite2'
	resource = 'page_archive'

	@login_required
	def get(request):
		"""
		页面的打包（zip）结果
		"""
		pagestore = pagestore_manager.get_pagestore('mongo')
		project_id = request.GET['project_id']

		#清空下载目录
		download_dir = os.path.join(settings.DOWNLOAD_HOME, 'download', project_id)
		if os.path.exists(download_dir):
			shutil.rmtree(download_dir)
		os.makedirs(download_dir)

		#export page
		for page in pagestore.get_pages(project_id):
			del page['_id']
			f = open(os.path.join(download_dir, 'page_%s.json' % page['page_id']), 'wb')
			print >> f, json.dumps(page, indent=4)
			f.close()

		#打包
		files = os.listdir(download_dir)
		zip_path = os.path.join(download_dir, 'project_%s.zip' % project_id)
		zip = zipfile.ZipFile(zip_path, 'w')
		for file in files:
			zip.write(os.path.join(download_dir, file), file)
		zip.close()

		path = '/termite_static/%s' % zip_path.replace('\\', '/').split('/static/')[-1]
		return HttpResponseRedirect(path)
