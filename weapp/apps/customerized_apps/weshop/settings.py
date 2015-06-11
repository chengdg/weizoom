# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

FIRST_NAV_NAME = 'apps'

INSTALLED_MODULES = [
	'mall2'
]

INSTALLED_VIEWS = [
	'mall2.mobile_views',
	'mall2.mobile_api_views'
] 

LEFT_NAVS = [{
	'section': u'微众商城',
	'navs': []
}]

WEIZOOM_PRICE = 1