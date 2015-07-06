#coding: utf8
"""@package core.termite_middleware
Termite相关的中间件

WebappPageCacheMiddleware: webapp page的缓存中间件
"""

from django.http import HttpResponse
from django.conf import settings

from utils import cache_util
from webapp import models as webapp_models

class WebappPageCacheMiddleware(object):
	def process_request(self, request):
		if not settings.ENABLE_WEPAGE_CACHE:
			pass
		else:
			if not '/termite2/webapp_page/' in request.path:
				return

			project_id = None
			if 'model' in request.GET:
				pass
			elif 'project_id' in request.path:
				project_id = int(request.GET.get('project_id', -1))
				if project_id == 0:
					if 'workspace_id' in request.GET:
						workspace = webapp_models.Workspace.objects.get(id=request.GET['workspace_id'])
						project = webapp_models.Project.objects.get(workspace=workspace, type='wepage', is_active=True)
						project_id = project.id
			elif 'workspace_id' in request.GET:
				workspace = webapp_models.Workspace.objects.get(id=request.GET['workspace_id'])
				project = webapp_models.Project.objects.get(workspace=workspace, type='wepage', is_active=True)
				project_id = project.id

			if project_id != None:
				request.project_id = project_id
				key = 'termite_webapp_page_%s' % project_id
				value = cache_util.get_cache(key)
				if value:
					return HttpResponse(value+'<div style="display:none;">from cache</div>')
				else:
					request.NEED_CACHE_WEBAPP_PAGE_IN_RESPONSE = True
			else:
				return None

	def process_response(self, request, response):
		if not settings.ENABLE_WEPAGE_CACHE:
			return response
		else:
			if hasattr(request, 'NEED_CACHE_WEBAPP_PAGE_IN_RESPONSE'):
				try:
					project_id = request.project_id
					key = 'termite_webapp_page_%s' % project_id
					value = response.content
					cache_util.set_cache(key, value)
				except:
					pass
			return response
