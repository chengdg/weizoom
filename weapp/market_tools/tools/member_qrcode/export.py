# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response

from models import *
from settings import TOOL_NAME


########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'webapp_owner_id=%d&project_id=0&workspace_id=market_tool:member_qrcode' % request.workspace.owner_id

	#获得页面
	pages = []
	member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner_id=request.workspace.owner_id)
	if member_qrcode_settings.count() > 0:
		pages.append({'text': TOOL_NAME, 'value': './?module=market_tool:member_qrcode&model=settings&action=get&settings_id=%d&%s' % (member_qrcode_settings[0].id, workspace_template_info)})

	response.data = [
		{
			'name': u'会员扫码列表',
			'data': pages
		}
	]
	return response.get_response()


def get_member_qrcode_webapp_link(request):
	workspace_template_info = 'webapp_owner_id=%d&project_id=0&workspace_id=market_tool:member_qrcode' % request.user.id
	member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner_id=request.user.id)
	if member_qrcode_settings.count() > 0:
		return './?module=market_tool:member_qrcode&model=settings&action=get&settings_id=%d&%s' % (member_qrcode_settings[0].id, workspace_template_info)

	return None
