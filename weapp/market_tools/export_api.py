# -*- coding: utf-8 -*-

__author__ = 'chuter'

from market_tools import ToolModule
from product.module_api import get_market_tool_modules_for_user_id
from market_tools.tools.weizoom_card import module_api as weizoom_card_module_api

###################################################################
# get_market_tool_webapp_usage_links: 获取webapp的用户中心中显示的营销工具使用情况链接
###################################################################
def get_market_tool_webapp_usage_links(webapp_owner_id, member=None):
	if webapp_owner_id <= 0:
		return []

	#使用每个营销工具中的export.get_webapp_usage_link获得信息
	all_market_tool_webapp_usage_links = []
	
	user_market_tool_modules = get_market_tool_modules_for_user_id(webapp_owner_id)

	# by liupeiyu
	# 是否有微众卡权限，如果有，在个人中心中添加“微众卡余额查询”
	if weizoom_card_module_api.is_weizoom_card_use_permission_by_owner_id(webapp_owner_id):
		user_market_tool_modules.update([u'weizoom_card'])

	for tool_module in ToolModule.all_tool_modules():
		try:
			tool_module_export = tool_module.export
		except:
			continue
		
		if not tool_module.module_name in user_market_tool_modules:
			#无权限，跳过
			continue

		if tool_module.module_name in  ['lottery', 'activity', 'vote', 'point_card']:
			continue

		if tool_module_export and hasattr(tool_module_export, 'get_webapp_usage_link'):
			link_info = tool_module_export.get_webapp_usage_link(webapp_owner_id, member)
			link_info['en_name'] = tool_module.module_name
			all_market_tool_webapp_usage_links.append(
				link_info
				)

	all_market_tool_webapp_usage_links.sort(key=lambda obj:len(obj.get('name')), reverse=False)

	return all_market_tool_webapp_usage_links