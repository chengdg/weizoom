# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response

from models import *
from settings import TOOL_NAME


########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	#workspace_template_info = 'workspace_id=market_tool:red_envelope&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id
	workspace_template_info = 'workspace_id=market_tool:red_envelope&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id
	#获得页面
	pages = []
	for red_envelope in RedEnvelope.objects.filter(owner_id=request.workspace.owner_id, is_deleted=False):
		pages.append({'text': red_envelope.name, 'value': './?module=market_tool:red_envelope&model=red_envelope&action=get&red_envelope_id=%d&%s' % (red_envelope.id, workspace_template_info)})

	response.data = [
		{
			'name': u'微信红包列表',
			'data': pages
		}
	]
	return response.get_response()

########################################################################
# get_webapp_usage_link: 获得webapp使用情况的链接
########################################################################
def get_webapp_usage_link(webapp_owner_id, member):
	workspace_template_info = 'workspace_id=market_tool:red_envelope&webapp_owner_id=%d&project_id=0' % webapp_owner_id
	info = '%d' % RedEnvelopeRecord.objects.filter(webapp_user_id__in=member.get_webapp_user_ids).count()

	return {
		'name': u'我的红包',
		'link': './?module=market_tool:red_envelope&model=usage&action=get&%s' % workspace_template_info,
		'info': info
	}
