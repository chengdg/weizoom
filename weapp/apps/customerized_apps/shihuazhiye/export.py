# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'


from core.jsonresponse import create_response

from apps.module_api import get_app_link_url


def __get_stydy_plan_link_targets(request):
	pages = []

	pages.append(
		{
			'text': '课程列表',
			'value': get_app_link_url(request, 'shihuazhiye', 'mall', 'products', 'list')
		}
	)
	

	return {
		'name': u'课程列表',
		'data': pages
	}


########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	ret_link_targets = []
	
	#学习计划的链接
	ret_link_targets.append(__get_stydy_plan_link_targets(request))	

	response = create_response(200)
	response.data = ret_link_targets
	return response.get_response()


########################################################################
# get_webapp_usage_link: 获得webapp使用情况的链接
########################################################################
def get_webapp_usage_link(webapp_owner_id, member):
	workspace_template_info = 'workspace_id=apps:shihuazhiye:mall&webapp_owner_id=%d&project_id=0' % webapp_owner_id

	return {
		'name': u'我的课程',
		'link': './?module=apps:shihuazhiye:mall&model=order_list&action=get&type=0&%s' % workspace_template_info
	}
