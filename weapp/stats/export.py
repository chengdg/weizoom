# -*- coding: utf-8 -*-
from mall import export as mall_export

FIRST_NAVS = mall_export.FIRST_NAVS
STATS_HOME_FIRST_NAV = mall_export.STATS_HOME_FIRST_NAV


#
# 数据罗盘左侧垂直方向二级导航信息
#
STATS_MANAGEMENT_SECOND_NAV = 'manage_summary'
STATS_SALES_SECOND_NAV = 'sales'
STATS_MEMBER_SECOND_NAV = 'member'

#
# 数据罗盘左侧垂直方向三级导航信息
#
SALES_ORDER_SUMMARY_NAV = 'order_summary'
# SALES_ORDER_LIST_NAV = 'order_list'
PRODUCT_SUMMARY_NAV = 'product_summary'
MARKETING_ACTIVITY_NAV = 'activity_analysis'

STATS_SECOND_NAV = {
    'navs': [
        {
            'name': STATS_MANAGEMENT_SECOND_NAV,
            'title': u'经营报告',
            'url': '/stats/manage_summary/',
            'permission': 'manage_summary'
        }, {
            'name': STATS_SALES_SECOND_NAV,
            'title': u'销售分析',
            'url': '/stats/order_summary/',
            'need_permissions': [], 
            'third_navs': [
                {
                    'name': SALES_ORDER_SUMMARY_NAV,
                    'title': u'订单概况分析',
                    'url': '/stats/order_summary/',
                    'need_permissions': []
                }, {
                    'name': PRODUCT_SUMMARY_NAV,
                    'title': u'商品概况分析',
                    'url': '/stats/product_summary/',
                    'need_permissions': []
                }, {
                    'name': MARKETING_ACTIVITY_NAV,
                    'title': u'营销传播分析',
                    'url': '/stats/activity_analysis/',
                    'need_permissions': []
                }#, {
                #     'name': SALES_ORDER_LIST_NAV,
                #     'title': u'订单明细分析',
                #     'url': '/stats/order_list/',
                #     'need_permissions': []
                # },
            ]
        }, {
            'name': STATS_MEMBER_SECOND_NAV,
            'title': u'会员分析',
            'url': '/stats/member_summary/',
            'need_permissions': []
        }
    ]
}


def get_stats_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        second_navs = [STATS_SECOND_NAV]
    return second_navs