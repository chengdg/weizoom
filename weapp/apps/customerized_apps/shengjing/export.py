# -*- coding: utf-8 -*-

__author__ = 'chuter'


from core.jsonresponse import create_response

from apps.module_api import get_app_link_url,get_shengjing_app_link_url


def __get_usercenter_link_targets(request):
	pages = []

	pages.append(
		{
			'text': '个人中心',
			'value': get_app_link_url(request, 'shengjing', 'user_center', 'user_info', 'get')
		}
	)
	pages.append(
		{
			'text': '积分日志',
			'value': get_app_link_url(request, 'shengjing', 'user_center', 'integral_log', 'get')
		}
	)
	pages.append(
		{
			'text': '会员扫码',
			'value': get_app_link_url(request, 'shengjing', 'user_center', 'member_qrcode', 'get')
		}
	)

	return {
		'name': u'会员中心',
		'data': pages
	}


def __get_stydy_plan_link_targets(request):
	pages = []

	pages.append(
		{
			'text': '学习计划',
			'value': get_app_link_url(request, 'shengjing', 'study_plan', 'study_plans', 'get')
		}
	)
	pages.append(
		{
			'text': '课程列表',
			'value': get_app_link_url(request, 'shengjing', 'study_plan', 'mobile_courses_list', 'get')
		}
	)
	pages.append(
		{
			'text': '课程签到',
			'value': get_app_link_url(request, 'shengjing', 'study_plan', 'courses_qrcode_list', 'get')
		}
	)

	return {
		'name': u'学习计划',
		'data': pages
	}

def __get_order_link_targets(request):
	pages = []

	pages.append(
		{
			'text': '账单',
			'value': get_app_link_url(request, 'shengjing', 'order', 'bills', 'get')
		}
	)

	return {
		'name': u'订单',
		'data': pages
	}

########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	ret_link_targets = []
	
	#会员中心的链接
	ret_link_targets.append(__get_usercenter_link_targets(request))

	#学习计划的链接
	ret_link_targets.append(__get_stydy_plan_link_targets(request))	

	#订单的链接
	ret_link_targets.append(__get_order_link_targets(request))	

	response = create_response(200)
	response.data = ret_link_targets
	return response.get_response()


########################################################################
# get_link_targets: 定义盛景定制APP可链接的目标
########################################################################
def __shengjingapp_link_targets(request):
    objects = []

    objects.append(
        {
        	'id': 1,
            'text': '个人中心',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'user_center', 'user_info', 'get')
        }
    )
    objects.append(
        {
        	'id': 2,
            'text': '会员扫码',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'user_center', 'member_qrcode', 'get')
        }
    )
    objects.append(
        {
        	'id': 3,
            'text': '积分日志',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'user_center', 'integral_log', 'get')
        }
    )
    objects.append(
        {
        	'id': 4,
            'text': '学习计划',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'study_plan', 'study_plans', 'get')
        }
    )
    objects.append(
        {
        	'id': 5,
            'text': '课程列表',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'study_plan', 'mobile_courses_list', 'get')
        }
    )
    objects.append(
        {
        	'id': 6,
            'text': '课程签到',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'study_plan', 'courses_qrcode_list', 'get')
        }
    )
    objects.append(
        {
        	'id': 7,
            'text': '账单',
            'link': get_shengjing_app_link_url(request, 'shengjing', 'order', 'bills', 'get')
        }
    )
    return {
        'name': u'盛景定制APP',
        'data': objects
    }

########################################################################
# get_link_targets: 获取盛景定制APP可链接的目标
########################################################################
def get_shengjing_link_targets(request):
    ret_link_targets = []
    
    #盛景定制的链接
    ret_link_targets.append(__shengjingapp_link_targets(request))

    # response = create_response(200)
    # response.data = ret_link_targets
    return ret_link_targets