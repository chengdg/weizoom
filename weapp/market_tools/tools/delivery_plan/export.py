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

	workspace_template_info = 'workspace_id=market_tool:delivery_plan&webapp_owner_id=%d&project_id=0' % request.workspace.owner_id

	#获得页面
	pages = []
	for delivery_plan in DeliveryPlan.objects.filter(owner_id=request.workspace.owner_id, is_deleted=False):
		pages.append({'text': delivery_plan.name, 'value': './?module=market_tool:delivery_plan&model=delivery_plan&action=get&delivery_plan_id=%d&%s' % (delivery_plan.id, workspace_template_info)})

	response.data = [
		{
			'name': u'配送套餐列表',
			'data': pages
		}
	]
	return response.get_response()
