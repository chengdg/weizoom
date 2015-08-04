# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

FIRST_NAV_NAME = 'apps'

INSTALLED_MODULES = [
	'mall'
]

INSTALLED_VIEWS = [
	'views',

	'mall.views',
	'mall.mobile_pay_views',
	'mall.mobile_views',
	'mall.mobile_api_views'
] 

LEFT_NAVS = [{
	'section': u'世华智业',
	'navs': [
		{
			'url': '/apps/shihuazhiye/?module=mall&resource=product_list&action=get',
			'title': u'课程列表',
			'name': u'product_list'
		},
	]
}]