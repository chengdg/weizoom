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
from weixin.user import module_api as weixin_api


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

		# 二维码
		try:				
			webapp_owner_id = request.GET.get('webapp_owner_id',None)
			woid = request.GET.get('woid', None)
			user_id = woid if webapp_owner_id is None else webapp_owner_id
			current_auth_qrcode_img = weixin_api.get_mp_qrcode_img(user_id)
		except:
			current_auth_qrcode_img = ''

		c = RequestContext(request, {
			'page_title': page_title,
			'page_html_content': html,
			'share_page_desc': site_description,
			'current_page_name': current_page_name,
			'current_auth_qrcode_img': current_auth_qrcode_img,
			'hide_non_member_cover': True #非会员也可使用该页面
		})

		return render_to_response('workbench/wepage_webapp_page.html', c)
