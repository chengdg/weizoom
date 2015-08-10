# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response

from models import *
from settings import TOOL_NAME


########################################################################
# get_link_targets: 获取可链接的目标
########################################################################


def get_channel_qrcode_webapp_link(request):
    if request.user_profile.user_id in [467,155]:
       workspace_template_info = 'webapp_owner_id=%d&project_id=0&workspace_id=market_tool:channel_qrcode' % request.user.id
       return './?module=market_tool:channel_qrcode&model=new_settings&action=get&%s' % workspace_template_info
    else:
	   workspace_template_info = 'webapp_owner_id=%d&project_id=0&workspace_id=market_tool:channel_qrcode' % request.user.id
	   return './?module=market_tool:channel_qrcode&model=settings&action=get&%s' % workspace_template_info

