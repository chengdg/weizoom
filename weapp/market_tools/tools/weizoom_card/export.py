# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response

from models import *
from settings import TOOL_NAME

########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=market_tool:weizoom_card&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id

	#获得页面
	pages = [{
		'text': u'微众卡余额查询',
		'value': './?module=market_tool:weizoom_card&model=weizoom_card_login&action=get&%s' % workspace_template_info
	}]
	response.data = [
		{
			'name': u'微众卡余额查询',
			'data': pages
		}
	]
	return response.get_response()

########################################################################
# get_webapp_usage_link: 获得webapp使用情况的链接
########################################################################
def get_webapp_usage_link(webapp_owner_id, member):
	workspace_template_info = 'workspace_id=market_tool:weizoom_card&webapp_owner_id=%d&project_id=0' % webapp_owner_id

	return {
		'name': u'微众卡余额查询',
		'link': './?module=market_tool:weizoom_card&model=weizoom_card_login&action=get&%s' % workspace_template_info
	}