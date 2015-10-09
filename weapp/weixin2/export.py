# -*- coding: utf-8 -*-
from mall import export as mall_export

FIRST_NAVS = mall_export.FIRST_NAVS
WEIXIN_HOME_FIRST_NAV = mall_export.WEIXIN_HOME_FIRST_NAV

UNBIND_ACCOUNT_FIRST_NAVS = [{
    'name': u'微信',
    'url': '/new_weixin/unbind_account/',
    'inner_name': 'unbind_account',
    'permission': ''
}]

UNBIND_ACCOUNT_FIRST_NAV = 'unbind_account'

UNBIND_ACCOUNT_NAV = {
    'section': u'微信',
    'navs': []
}

def get_unbind_account_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        second_navs = [UNBIND_ACCOUNT_NAV]

    return second_navs

#
# 微信左侧垂直方向二级导航信息
#
WEIXIN_HOME_OUTLINE_NAV = WEIXIN_HOME_FIRST_NAV
WEIXIN_MESSAGE_SECOND_NAV = 'realtime_messages'
WEIXIN_ADVANCE_SECOND_NAV = 'material'
WEIXIN_MPUSER_SECOND_NAV = 'menu'

#
# 微信左侧垂直方向三级导航信息
#
MESSAGE_REALTIME_MESSAGE_NAV = 'realtime_messages'
MESSAGE_MASS_SENDING_NAV = 'mass_sending'
MESSAGE_AUTO_REPLY_NAV = 'auto_reply'
MESSAGE_TEMPLATE_MESSAGE_NAV = 'template_message'

ADVANCE_MANAGE_MATERIAL_NAV = 'material'
ADVANCE_MANAGE_FANS_NAV = 'fans'
ADVANCE_MANAGE_QRCODE_NAV = 'qrcode'
ADVANCE_MANAGE_MEMBER_CHANNEL_QRCODE_NAV = 'member_channel_qrcode'

MPUSER_FIRST_NAV = 'mp_user'
MPUSER_BINDING_NAV = 'binding'
MPUSER_MENU_NAV = 'menu'
MPUSER_DIRECT_FOLLOW_NAV = 'direct_follow'

WEIXIN_SECOND_NAV = {
    'section': u'微信概况',
    'navs': [
        {
            'name': WEIXIN_HOME_OUTLINE_NAV,
            'title': u'微信概况',
            'url': '/new_weixin/outline/',
            'need_permissions': []
        }, {
            'name': WEIXIN_MESSAGE_SECOND_NAV,
            'title': u'消息互动',
            'url': '/new_weixin/realtime_messages/',
            'need_permissions': [], 
            'third_navs': [
                {
                    'name': MESSAGE_REALTIME_MESSAGE_NAV,
                    'title': u'实时消息',
                    'url': '/new_weixin/realtime_messages/',
                    'need_permissions': [],
                    'class_name': 'xa-msgTip'
                },
                {
                    'name': MESSAGE_MASS_SENDING_NAV,
                    'title': u'群发消息',
                    'url': '/new_weixin/mass_sending_messages/',
                    'need_permissions': []
                },
                {
                    'name': MESSAGE_AUTO_REPLY_NAV,
                    'title': u'自动回复',
                    'url': '/new_weixin/keyword_rules/',
                    'need_permissions': []
                },
                {
                    'name': MESSAGE_TEMPLATE_MESSAGE_NAV,
                    'title': u'模板消息',
                    'url': '/new_weixin/template_messages/',
                    'need_permissions': []
                }
            ]
        }, {
            'name': ADVANCE_MANAGE_MATERIAL_NAV,
            'title': u'高级管理',
            'url': '/new_weixin/materials/',
            'need_permissions': [], 
            'third_navs': [
                {
                    'name': ADVANCE_MANAGE_MATERIAL_NAV,
                    'title': u'图文管理',
                    'url': '/new_weixin/materials/',
                    'need_permissions': []
                },
                {
                    'name': ADVANCE_MANAGE_QRCODE_NAV,
                    'title': u'带参数二维码',
                    'url': '/new_weixin/qrcodes/',
                    'need_permissions': []
                }
            ]
        }, {
            'name': MPUSER_MENU_NAV,
            'title': u'公众号设置',
            'url': '/new_weixin/menu/',
            'need_permissions': [], 
            'third_navs': [
                {
                    'name': MPUSER_MENU_NAV,
                    'title': u'自定义菜单',
                    'url': '/new_weixin/menu/',
                    'need_permissions': []
                },
                {
                    'name': MPUSER_DIRECT_FOLLOW_NAV,
                    'title': u'快速关注',
                    'url': '/new_weixin/direct_follow/',
                    'need_permissions': []
                },
                 {
                    'name': MPUSER_BINDING_NAV,
                    'title': u'公众号绑定',
                    'url': '/new_weixin/mp_user/',
                    'need_permissions': []
                }
            ]
        }
    ]
}

def get_weixin_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        if request.manager.id in [467,154]:
            import copy
            SHOWCAO_WEIXIN_SECOND_NAV = copy.deepcopy(WEIXIN_SECOND_NAV)
            for navs in SHOWCAO_WEIXIN_SECOND_NAV['navs']:
                if navs['name'] == ADVANCE_MANAGE_MATERIAL_NAV:
                    for third_nav in navs['third_navs']:
                        if third_nav['name'] == ADVANCE_MANAGE_QRCODE_NAV:
                            third_nav['name'] = ADVANCE_MANAGE_MEMBER_CHANNEL_QRCODE_NAV
                            third_nav['title'] = u'首草渠道扫码'
                            third_nav['url'] = '/new_weixin/channel_qrcode/'

            second_navs = [SHOWCAO_WEIXIN_SECOND_NAV]
        else:
            second_navs = [WEIXIN_SECOND_NAV]

    return second_navs