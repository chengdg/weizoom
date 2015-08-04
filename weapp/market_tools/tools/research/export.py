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

	workspace_template_info = 'workspace_id=market_tool:research&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id

	#获得页面
	pages = []
	for research in Research.objects.filter(owner_id=request.workspace.owner_id, is_deleted=False):
		pages.append({'text': research.name, 'value': './?module=market_tool:research&model=research&action=get&research_id=%d&%s' % (research.id, workspace_template_info)})

	response.data = [
		{
			'name': u'用户调研列表',
			'data': pages
		}
	]
	return response.get_response()

