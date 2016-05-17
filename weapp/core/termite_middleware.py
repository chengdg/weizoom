#coding: utf8
"""@package core.termite_middleware
Termite相关的中间件

WebappPageCacheMiddleware: webapp page的缓存中间件
"""

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings

from utils import cache_util
from webapp import models as webapp_models
from account import models as account_models

class WebappPageCacheMiddleware(object):
	def process_request(self, request):
		if not settings.ENABLE_WEPAGE_CACHE:
			pass
		else:
			if not '/termite2/webapp_page/' in request.path:
				return

			if request.GET.get('page_id', '') == 'preview':
				#预览不使用缓存
				return
				
			#如果当前cookie中没有会员信息，则不进行缓存
			cookie_openid_webapp_id = request.COOKIES.get(member_settings.OPENID_WEBAPP_ID_KEY, None)
			#print ">>>>>DF>>>DF>D>>>>>>&&&&&&&*88888",cookie_openid_webapp_id
			if (cookie_openid_webapp_id is None):
				return None
			else:
				split_list = cookie_openid_webapp_id.split('____')
				if len(split_list) != 2:
					return None
				else:
					webapp_id = split_list[1]
					openid = split_list[0]
					if webapp_id != request.user_profile.webapp_id or (not openid):
						return None

			project_id = None
			if 'model' in request.GET:
				pass
			elif 'project_id' in request.GET:
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
		#TODO:暂时只针对店铺首页进行缓存优化
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



class WebappPageHomePageMiddleware(object):
	"""
	重定向 HomePage 链接地址

	author = 'liupeiyu'
	"""
	def process_request(self, request):
		if not 'home_page' in request.get_full_path():
			return None

		webapp_owner_id = request.GET.get('webapp_owner_id', 0)
		if webapp_owner_id == 0:
			return None

		if hasattr(request, 'user_profile') and hasattr(request.user_profile, 'is_use_wepage'):
			if not request.user_profile.is_use_wepage:
				return None
		else:
			user_profiles = account_models.UserProfile.objects.filter(user_id=webapp_owner_id)
			if user_profiles.count() == 0:
				return None

			user_profile = user_profiles[0]
			if not user_profile.is_use_wepage:
				return None

		orig_path = request.path
		if orig_path != '/termite/workbench/jqm/preview/':
			return None

		new_path = '/termite2/webapp_page/'
		new_url = request.get_full_path().replace(orig_path, new_path)
		response = HttpResponseRedirect(new_url)
		return response

