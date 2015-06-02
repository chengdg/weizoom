# -*- coding: utf-8 -*-

__author__ = 'chuter'

from market_tools import ToolModule
from settings import TOOLS_ORDERING

NAV = {
	'section': u'营销工具'
}

#TODO 增加营销工具首页

########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs_bak(request):
	#add by robert: 禁用缓存
	#if NAV.has_key('navs'):
	#	return [NAV]

	user_market_tool_modules = request.user.market_tool_modules
	NAV['navs'] = []
	for tool_module in ToolModule.all_tool_modules():
		if not tool_module.module_name in user_market_tool_modules:
			#无权限，跳过
			continue

		if tool_module.module_name in TOOLS_ORDERING:
			order_index = TOOLS_ORDERING[tool_module.module_name]
		else:
			order_index = 100
		
		NAV['navs'].append({
			'name': tool_module.module_name,
			'url': '/market_tools/%s/' % tool_module.module_name,
			'title': tool_module.settings.TOOL_NAME,
			'order_index': order_index
		})
	
	NAV['navs'] = sorted(NAV['navs'], reverse=False, key=lambda n : n['order_index']) #排序

	return [NAV]


########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	#add by robert: 禁用缓存
	#if NAV.has_key('navs'):
	#	return [NAV]

	user_market_tool_modules = request.user.market_tool_modules
	NAV['navs'] = []

	path = request.META['PATH_INFO']
	module_name = path.split('/')[-2]
	for tool_module in ToolModule.all_tool_modules():
		if module_name == tool_module.module_name:	
			NAV['navs'].append({
				'name': tool_module.module_name,
				'url': '/market_tools/%s/' % tool_module.module_name,
				'title': tool_module.settings.TOOL_NAME
			})
	
	NAV['navs'].append({
		'name': 'apps',
		'url': '/apps/',
		'title': u'<i class="icon icon-arrow-left"></i>返回百宝箱'
	})
	
	return [NAV]