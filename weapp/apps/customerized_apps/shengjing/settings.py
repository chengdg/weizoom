# -*- coding: utf-8 -*-

__author__ = 'chuter'

FIRST_NAV_NAME = 'apps'

INSTALLED_MODULES = [
	'order',
	'study_plan',
	'user_center'
]

INSTALLED_VIEWS = [
	'views',

	'order.mobile_views',
	'order.mobile_api_views',

	'study_plan.api_views',
	'study_plan.mobile_views',
	'study_plan.views',
	'study_plan.mobile_api_views',

	'user_center.views',
	'user_center.mobile_views',
	'user_center.api_views',
	'user_center.mobile_api_views'
] 

LEFT_NAVS = [{
	'section': u'盛景学院',
	'navs': [
		{	
			'url' : '/apps/shengjing/?module=user_center&resource=score&action=get',
			'title': u'积分配置',
			'name': u'integral_settings'
		},
		{
			'url': '/apps/shengjing/?module=study_plan&resource=course_list&action=get',
			'title': u'课程列表',
			'name': u'course_settings'
		},
	]
}]