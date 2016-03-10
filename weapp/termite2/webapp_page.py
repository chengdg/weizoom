# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models

from termite2 import pagecreater
from termite.workbench import jqm_views


class WebappPage(resource.Resource):
	app = 'termite2'
	resource = 'webapp_page'

	def get(request):
		"""
		webapp页面（目前是首页）
		"""
		if 'model' in request.GET:
			return jqm_views.show_preview_page(request)

		project_id = request.REQUEST.get('project_id', 0)
		if project_id == 0:
			response = create_response(500)
			response.errMsg = u'没有project_id参数'
			return response.get_response()


		# 如果是空页面，跳转到404页面
		if pagecreater.is_home_page(request):
			pass
		else:
			projects = webapp_models.Project.objects.filter(id=project_id)
			if projects.count() == 0:
				c = RequestContext(request, {
					# "is_deleted_data": True
				})
				return render_to_response('mobile_error_info.html', c);

				# from account.views import show_error_page
				# return show_error_page(request)


		#获取project
		# project = None
		# #project_id = request.REQUEST.get('project_id')
		# is_app_project = False
		# app_name = ''
		# if project_id.startswith('new_app:'):
		# 	_, app_name, project_id = project_id.split(':')
		# 	is_app_project = True
		# else:
		# 	project_id = int(request.REQUEST.get('project_id', 0))

		# if is_app_project:
		# 	project = webapp_models.Project()
		# 	project.id = project_id
		# 	project.type = 'appkit'
		# else:
		# 	if project_id != 0:
		# 		project = webapp_models.Project.objects.get(id=project_id)
		# 	else:
		# 		workspace = webapp_models.Workspace.objects.get(owner=request.webapp_owner_id, inner_name='home_page')
		# 		project = webapp_models.Project.objects.get(workspace_id=workspace.id, type='wepage', is_active=True)
		# 		project_id = project.id

		# project.app_name = ''
		# project.is_app_project = is_app_project
		# request.project = project

		html = pagecreater.create_page(request, return_html_snippet=True)

		#获取page title
		page_title = u'店铺首页'
		beg_tag = 'data-page-title="'
		end_tag = '"'
		beg = html.find(beg_tag)+len(beg_tag)
		if beg != -1:
			end = html.find(end_tag, beg)
			page_title = html[beg:end]

		# 获取页面描述
		site_description = pagecreater.get_site_description(request)

		# 是否是首页
		if pagecreater.is_home_page(request):
			# 首页
			current_page_name = 'home'
		else:
			# 微页面
			current_page_name = 'page'
		# 是否是预览状态
		is_preview = True if request.GET.get('page_id', '') == 'preview' else False

		c = RequestContext(request, {
			'page_title': page_title,
			'page_html_content': html,
			'share_page_desc': site_description,
			'share_to_timeline_use_desc': True,  #分享到朋友圈的时候信息变成分享给朋友的描述
			'current_page_name': current_page_name,
			'is_preview': is_preview,
			'hide_non_member_cover': True #非会员也可使用该页面
		})

		return render_to_response('workbench/wepage_webapp_page.html', c)
