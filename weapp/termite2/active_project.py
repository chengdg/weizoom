# -*- coding: utf-8 -*-

import json
import os
import sys
import zipfile
import shutil

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models
from termite import pagestore as pagestore_manager

from utils import cache_util

from termite2.tasks import purge_webapp_page_from_varnish_cache

class ActiveProject(resource.Resource):
	app = 'termite2'
	resource = 'active_project'

	@staticmethod
	def delete_webapp_page_cache(webapp_owner_id, project_id):
		key = 'termite_webapp_page_%s_%s' % (webapp_owner_id, project_id)
		cache_util.delete_cache(key)

		purge_webapp_page_from_varnish_cache.delay(webapp_owner_id, project_id)

	@login_required
	def api_put(request):
		"""
		创建active project
		"""
		project_id = request.POST['id']
		webapp_models.Project.objects.filter(owner=request.user, is_active=True).update(is_active=False)
		webapp_models.Project.objects.filter(id=project_id).update(is_active=True)

		ActiveProject.delete_webapp_page_cache(request.manager.id, project_id)

		response = create_response(200)
		return response.get_response()
