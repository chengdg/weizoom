# -*- coding: utf-8 -*-
import evaluates

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "evaluates",
			'title': "商品评价",
			'url': '/apps/evaluate/evaluates/',
			'need_permissions': []
		},
	]
}


########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.manager.username == 'manager':
		second_navs = [NAV]
	else:
		# webapp_module_views.get_modules_page_second_navs(request)
		second_navs = [NAV]
	
	return second_navs
