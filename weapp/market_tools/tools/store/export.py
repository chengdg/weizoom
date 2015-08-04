# -*- coding: utf-8 -*-

__author__ = 'robert'

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response

from models import *
from settings import TOOL_NAME

########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=market_tool:store&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id

	#获得页面
	pages = []
	pages.append({'text': u'全部门店列表', 'value': './?module=market_tool:store&model=store_citys&action=get&%s' % workspace_template_info})
	
	response.data = [
		{
			'name': u'页面',
			'data': pages
		}
	]
	return response.get_response()
