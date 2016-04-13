# -*- coding: utf-8 -*-
from weizoom_card import settings
#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	top_navs = [{
		'name': 'card',
		'displayName': '微众卡',
		'icon': 'credit-card',
		'href': '/card/ordinary_rules/'
	},
	{
		'name': 'rule_order',
		'displayName': '卡订单',
		'icon': 'credit-card',
		'href': '/order/rule_order/'
	}]
	return {'top_navs': top_navs}

def bundle_host(request):
	return {'bundle_host': settings.BUNDLE_HOST}