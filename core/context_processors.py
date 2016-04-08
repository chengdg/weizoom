# -*- coding: utf-8 -*-

#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	top_navs = [{
		'name': 'card',
		'displayName': '微众卡',
		'icon': 'credit-card',
		'href': '/card/ordinary_rules/'
	}]
	return {'top_navs': top_navs}