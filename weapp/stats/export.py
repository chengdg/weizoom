# -*- coding: utf-8 -*-

MARKETING_NAV = 'marketing'
MANAGEMENT_NAV = 'manage'
SALES_NAV = 'sales'
MEMBER_NAV = 'member'

FIRST_NAVS = [{
    'name': u'经营报告',
    'url': '/stats/manage_summary/',
    'inner_name': MANAGEMENT_NAV,
    'permission': ''
}, {
    'name': u'营销分析',
    'url': '/stats/activity_analysis/',
    'inner_name': MARKETING_NAV,
    'permission': ''
}, {
    'name': u'销售分析',
    'url': '/stats/order_summary/',
    'inner_name': SALES_NAV,
    'permission': ''
}, {
    'name': u'会员分析',
    'url': '/stats/member_summary/',
    'inner_name': MEMBER_NAV,
    'permission': ''
}]

#
# 营销分析
#
MARKETING_ACTIVITY_NAV = 'activity'

MARKETING_NAVS = {
    'section': u'营销分析',
    'navs': [
        {
            'name': MARKETING_ACTIVITY_NAV,
            'title': u'营销传播分析',
            'url': '/stats/activity_analysis/',
            'need_permissions': []
        },
    ]
}


def get_market_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [MARKETING_NAVS]
    return second_navs


#
# 销售概况
#
SALES_ORDER_SUMMARY_NAV = 'order_summary'
SALES_ORDER_LIST_NAV = 'order_list'
PRODUCT_SUMMARY_NAV = 'product_summary'

SALES_NAVS = {
    'section': u'销售分析',
    'navs': [
        {
            'name': SALES_ORDER_SUMMARY_NAV,
            'title': u'订单概况分析',
            'url': '/stats/order_summary/',
            'need_permissions': []
        },
        {
            'name': SALES_ORDER_LIST_NAV,
            'title': u'订单明细分析',
            'url': '/stats/order_list/',
            'need_permissions': []
        },
        {
            'name': PRODUCT_SUMMARY_NAV,
            'title': u'商品概况分析',
            'url': '/stats/product_summary/',
            'need_permissions': []
        }
    ]
}



def get_sales_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [SALES_NAVS]
    return second_navs


#
# 会员分析
#
MEMBER_SUMMARY_NAV = 'member_summary'

MEMBERS_NAVS = {
    'section': u'会员分析',
    'navs': [
        {
            'name': MEMBER_SUMMARY_NAV,
            'title': u'会员概况',
            'url': '/stats/member_summary/',
            'need_permissions': []
        },
    ]
}



def get_member_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [MEMBERS_NAVS]
    return second_navs


#
# 经营概况
#
MANAGEMENT_SUMMARY_NAV = 'management_summary'

MANAGEMENT_NAVS = {
    'section': u'经营报告',
    'navs': [
        {
            'name': MANAGEMENT_SUMMARY_NAV,
            'title': u'经营概况',
            'url': '/stats/manage_summary/',
            'need_permissions': []
        },
    ]
}



def get_management_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [MANAGEMENT_NAVS]
    return second_navs
