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

class ActiveProject(resource.Resource):
	app = 'termite2'
	resource = 'active_project'

	@login_required
	def api_put(request):
		"""
		创建active project
		"""
		project_id = request.POST['id']
		webapp_models.Project.objects.filter(owner=request.user, is_active=True).update(is_active=False)
		webapp_models.Project.objects.filter(id=project_id).update(is_active=True)

		response = create_response(200)
		return response.get_response()
