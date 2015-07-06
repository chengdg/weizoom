# -*- coding: utf-8 -*-

import json
from datetime import datetime
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from termite2 import export
import termite2.models as termite_models
from core import resource
from core import paginator
from core.jsonresponse import create_response
from weixin.mp_decorators import mp_required

FIRST_NAV = export.WEPAGE_FIRST_NAV
COUNT_PER_PAGE = 20

class CustomModule(resource.Resource):
	"""
	自定义模块资源
	"""
	app = 'termite2'
	resource = 'custom_module'

	@login_required
	@mp_required
	def get(request):
		"""
		获取自定义模块
		"""
		module_id = request.GET.get('id', None)
		if module_id:
			custom_module = termite_models.TemplateCustomModule.objects.get(owner=request.manager, id=module_id)
		else:
			custom_module = None

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_wepage_second_navs(request),
			'second_nav_name': export.WEPAGE_MODULES_NAV,
			'custom_module': custom_module
		})

		return render_to_response('termite2/custom_module_editor.html', c)


	def api_delete(request):
		"""
		删除自定义模块
		"""
		termite_models.TemplateCustomModule.objects.filter(owner=request.user, id=request.POST['id']).update(is_deleted=True)
		return create_response(200).get_response()


class CustomModuleName(resource.Resource):
	"""
	自定义模块名称资源
	"""
	app = 'termite2'
	resource = 'custom_module_name'

	def api_post(request):
		"""
		修改自定义模块名称
		"""
		try:
			module_id = request.POST.get('id')
			name = request.POST.get('name')
			if CustomModuleName.is_check_name_repeat(request.user, module_id, name):
				response = create_response(501)
				response.data.msg = u'标题名已存在'
				return response.get_response()
			else:
				termite_models.TemplateCustomModule.objects.filter(owner=request.user, id=module_id).update(name=name, updated_at=datetime.now())
				return create_response(200).get_response()
		except:
			return create_response(500).get_response()


	def api_get(request):
		"""
		验证名字是否重复
		"""
		try:
			module_id = request.GET.get('id')
			name = request.GET.get('name')
			if CustomModuleName.is_check_name_repeat(request.user, module_id, name):
				response = create_response(501)
				response.data.msg = u'标题名已存在'
				return response.get_response()
			else:
				return create_response(200).get_response()
		except:
			return create_response(500).get_response()

	
	def is_check_name_repeat(user, id, name):
		count = termite_models.TemplateCustomModule.objects.filter(owner=user, name__contains=name).exclude(id=id).count()
		if count > 0:
			return True

		return False