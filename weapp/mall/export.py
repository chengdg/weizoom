# -*- coding: utf-8 -*-
from weapp.settings import MONEY_HOST

MALL_HOME_FIRST_NAV = 'mall_outline'
WEIXIN_HOME_FIRST_NAV = 'weixin_outline'
PRODUCT_FIRST_NAV = 'product'
ORDER_FIRST_NAV = 'order'
MALL_PROMOTION_AND_APPS_FIRST_NAV = 'promotion'
MEMBER_HOME_FIRST_NAV = 'member'
STATS_HOME_FIRST_NAV = 'manage_summary'
MALL_CONFIG_FIRST_NAV = 'config'
BIG_DATA_HOME_FIRST_NAV = 'big_data'


#############temp##########################
MALL_HOME_WEPAGE_NAV = 'wepage'
MALL_HOME_GLOBAL_NAVBAR_NAV = 'globalNavbar'
#############temp##########################

FIRST_NAVS = [{
    'name': u'首页',
    'url': '/mall2/outline/',
    'inner_name': MALL_HOME_FIRST_NAV,
    'permission': 'manage_index'
}, {
    'name': u'微信',
    'url': '/new_weixin/outline/',
    'inner_name': WEIXIN_HOME_FIRST_NAV,
    'permission': 'weixin',
    'class_name': 'xa-msgTip'
}, {
    'name': u'商品',
    'url': '/mall2/product_list/?shelve_type=1',
    'inner_name': PRODUCT_FIRST_NAV,
    'permission': 'manage_product'
}, {
    'name': u'订单',
    'url': '/mall2/order',
    'inner_name': ORDER_FIRST_NAV,
    'permission': 'manage_order',
    'class_name': 'xa-orderTip'
}, {
    'name': u'应用和营销',
    'url': '/mall2/flash_sale_list/',
    'inner_name': MALL_PROMOTION_AND_APPS_FIRST_NAV,
    'permission': 'manage_promotion_all'
}, {
    'name': u'会员',
    'url': '/member/member_list/',
    'inner_name': MEMBER_HOME_FIRST_NAV,
    'permission': 'manage_member'
}, {
    'name': u'数据罗盘',
    'url': '/stats/manage_summary/',
    'inner_name': STATS_HOME_FIRST_NAV,
    'permission': 'stats'
}, {
    'name': u'配置',
    'url': '/mall2/pay_interface_list/',
    'inner_name': MALL_CONFIG_FIRST_NAV,
    'permission': 'config'
}, {
    'name': u'粉丝招募平台',
    'url': 'http://data.weizoom.com/',
    'inner_name': BIG_DATA_HOME_FIRST_NAV,
    'permission': 'big_data',
    'need_token': True
}]

def get_first_navs(user):
    # from auth.export import NAV as AUTH_NAV
    from member.export import MEMBER_NAV
    manage_index=MALL_HOME_SECOND_NAV
    manage_product=MALL_PRODUCT_SECOND_NAV
    manage_order=MALL_ORDER_SECOND_NAV
    manage_promotion=MALL_PROMOTION_AND_APPS_SECOND_NAV
    manage_member=CONFIG_NAV
    static={'navs':[]}
    manage_auth=MEMBER_NAV
    manage_mall_config=CONFIG_NAV
    apps = MALL_PROMOTION_AND_APPS_SECOND_NAV

    first_navs_result = []
    for nav in FIRST_NAVS:
        if user.has_perm(nav['permission']):
            for s_nav in eval(nav['permission'])['navs']:
                if user.has_perm(s_nav['permission']):
                    if not nav.get('children', None):
                        nav['children'] = []
                        nav['url'] = s_nav['url']
                    nav['children'].append(s_nav)
            first_navs_result.append(nav)

    return first_navs_result


#首页左侧垂直方向二级导航
MALL_HOME_OUTLINE_NAV = 'census'
MALL_HOME_INTEGRAL_NAV = 'integralRule'
MALL_HOME_NOTICES_NAV = 'notices'
MALL_HOME_WEPAGE_NAV = 'wepage'
MALL_HOME_GLOBAL_NAVBAR_NAV = 'globalNavbar'

MALL_HOME_SECOND_NAV = {
    'section': u'商城首页',
    'navs': [  # 商品管理
        {
            'name': MALL_HOME_OUTLINE_NAV,
            'title': u'统计概况',
            'url': '/mall2/outline/',
            'permission': 'manage_index_outline'
        }, {
            'name': MALL_HOME_INTEGRAL_NAV,
            'title': u'积分规则',
            'url': '/mall2/integral_strategy/',
            'permission': 'manage_index_integral'
        }, {
            'name': MALL_HOME_WEPAGE_NAV,
            'title': u'店铺装修',
            'url': '/termite2/pages/',
            'permission': 'manage_wepage'
        }, {
            'name': MALL_HOME_GLOBAL_NAVBAR_NAV,
            'title': u'店铺导航',
            'url': '/termite2/global_navbar/',
            'permission': 'manage_wepage_navbar'
        }
    ]
}


def get_mall_home_second_navs(request):
    """
    获取"商铺首页"部分的二级导航
    """
    if request.user.username == 'manager':
        second_navs = [MALL_HOME_SECOND_NAV]
    else:
        second_navs = [MALL_HOME_SECOND_NAV]

    return second_navs



PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV = 'selling'
PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV = 'toSell'
PRODUCT_ADD_PRODUCT_NAV = 'addnew'
PRODUCT_MANAGE_RECYCLED_PRODUCT_NAV = 'recycleBin'
PRODUCT_MANAGE_IMAGE_NAV = 'pictureManagement'
PRODUCT_MANAGE_CATEGORY_NAV = 'groupManagement'
PRODUCT_MANAGE_MODEL_NAV = 'attrModelManagement'
PRODUCT_REVIEW_NAV = 'reviewManagement'

MALL_PRODUCT_SECOND_NAV = {
    'section': u'商品',
    'navs': [
        # 商品管理
        {
            'name': PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV,
            'title': u'在售商品管理',
            'url': '/mall2/product_list/?shelve_type=1',
            'permission': 'manage_product_onshelf'
        },

        {
            'name': PRODUCT_ADD_PRODUCT_NAV,
            'title': u'添加新商品',
            'url': '/mall2/product/',
            'permission': 'manage_product_add'
        },
        {
            'name': PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV,
            'title': u'待售商品管理',
            'url': '/mall2/product_list/?shelve_type=0',
            'permission': 'manage_product_offshelf'
        },
        # {
        #     'name': PRODUCT_MANAGE_RECYCLED_PRODUCT_NAV,
        #     'title': u'商品回收站',
        #     'url': '/mall2/product_list/?shelve_type=2',
        #     'permission': 'manage_product_deleted'
        # },
        {
            'name': PRODUCT_MANAGE_IMAGE_NAV,
            'title': u'图片管理',
            'url': '/mall2/image_group_list/',
            'permission': 'manage_product_image'
        },
        {
            'name': PRODUCT_MANAGE_CATEGORY_NAV,
            'title': u'分组管理',
            'url': '/mall2/category_list/',
            'permission': 'manage_product_category'
        },
        {
            'name': PRODUCT_MANAGE_MODEL_NAV,
            'title': u'属性规格管理',
            'url': '/mall2/model_property_list/',
            'permission': 'manage_product_property_and_model_property'
        },
        {
            'name': PRODUCT_REVIEW_NAV,
            'title': u'评价管理',
            'url': '/mall2/product_review_list/',
            'permission': 'manage_product_review'
        },
    ]
}

########################################################################
# get_mall_product_second_navs: 获得商品二级导航
########################################################################
def get_mall_product_second_navs(request):
    if request.user.username == 'manager':
        # second_navs = [MALL_PRODUCT_SECOND_NAV]
        pass
    else:
        second_navs = [MALL_PRODUCT_SECOND_NAV]

    return second_navs


ORDER_ALL = 'allOrder'
ORDER_REFUND = 'refundOrder'
ORDER_AUDIT = 'financialCheck'
ORDER_EXPIRED_TIME = 'orderExpiration'
ORDER_BATCH_DELIVERY = 'orderBatchDelivery'
ORDER_MONEY = 'orderMoney'

MALL_ORDER_SECOND_NAV = {
    'section': u'',
    'navs': [
        # 商品管理
        {
            'name': ORDER_ALL,
            'title': u'所有订单',
            'url': '/mall2/order_list/',
            'permission': 'manage_order_all'
        },
        {
            'name': ORDER_EXPIRED_TIME,
            'title': u'订单设置',
            'url': '/mall2/order_config/',
            'permission': 'manage_order_expired_time'
        },
        {
            'name': ORDER_AUDIT,
            'title': u'财务审核',
            'url': '/mall2/order_list/?belong=audit',
            'permission': 'manage_order_audit'
        },
        {
            'name': ORDER_BATCH_DELIVERY,
            'title': u'批量发货',
            'url': 'javascript:void(0);',
            'permission': 'manage_order_batch_delirvery'
        },{
            'name': ORDER_MONEY,
            'title': u'结算管理',
            'url': '/mall2/orders_to_money/',
            'permission': 'manage_order_batch_delivery',
        }
    ]
}


def get_mall_order_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        second_navs = [MALL_ORDER_SECOND_NAV]

    return second_navs




#
# 应用和营销左侧垂直方向三级导航信息
#
MALL_PROMOTION_PROMOTIONS_NAV = 'promotionQuery'
MALL_PROMOTION_FLASH_SALE_NAV = 'flashSale'
MALL_PROMOTION_PREMIUM_SALE_NAV = 'buyGifts'
MALL_PROMOTION_PRICE_CUT_NAV = 'fullReduction'
MALL_PROMOTION_COUPON_NAV = 'Coupon'
MALL_PROMOTION_INTEGRAL_SALE_NAV = 'integralYingyon'
MALL_PROMOTION_ISSUING_COUPONS_NAV = 'issuingCoupon'
MALL_PROMOTION_FORBIDDEN_COUPON_PRODUCT_NAV = 'forbiddenCouponProduct'
MALL_PROMOTION_CARD_EXCHANGE_NAV = 'cardExchange'

MALL_APPS_LOTTERY_NAV = 'lotteries'
MALL_APPS_FEEDBACK_NAV = 'exsurveies'
MALL_APPS_SURVEY_NAV = 'surveies'
MALL_APPS_EVENT_NAV = 'events'
MALL_APPS_VOTE_NAV = 'votes'
MALL_APPS_SIGN_NAV = 'sign'
MALL_APPS_RED_ENVELOPE_NAV = 'red_envelopes'
MALL_APPS_POWERME_NAV = 'powerme'
MALL_APPS_REDPACKET_NAV = 'red_packet'
MALL_APPS_GROUP_NAV = 'groups'
MALL_APPS_SHVOTE_NAV = 'shvotes'
MALL_APPS_REBATE_NAV = 'rebate'

#
# 应用和营销左侧垂直方向二级导航信息
#
MALL_PROMOTION_SECOND_NAV = MALL_PROMOTION_FLASH_SALE_NAV
MALL_APPS_SECOND_NAV = MALL_APPS_LOTTERY_NAV


MALL_PROMOTION_AND_APPS_SECOND_NAV = {
    'section': u'',
    'navs': [
        # 商品管理
        {
            'name': MALL_PROMOTION_SECOND_NAV,
            'title': u'促销管理',
            'url': '/mall2/flash_sale_list/',
            'permission': 'manage_promotion',
            'third_navs': [
                # 商品管理
                # {
                #     'name': MALL_PROMOTION_PROMOTIONS_NAV,
                #     'title': u'促销查询',
                #     'url': '/mall2/promotion_list/',
                #     'permission': ['search_promotion', ]
                # },
                {
                    'name': MALL_PROMOTION_FLASH_SALE_NAV,
                    'title': u'限时抢购',
                    'url': '/mall2/flash_sale_list/',
                    'permission': 'manage_flash_sale'
                },
                {
                    'name': MALL_PROMOTION_PREMIUM_SALE_NAV,
                    'title': u'买赠',
                    'url': '/mall2/premium_sale_list/',
                    'permission': 'manage_premium_sale'
                },
                # {
                #     'name': MALL_PROMOTION_PRICE_CUT_NAV,
                #     'title': u'满减',
                #     'url': '/mall2/price_cut_list/',
                #     'permission': ['manage_price_cut', ]
                # },
                {
                    'name': MALL_PROMOTION_INTEGRAL_SALE_NAV,
                    'title': u'积分应用',
                    'url': '/mall2/integral_sales_list/',
                    'permission': 'manage_integral_sale'
                },
                {
                    'name': MALL_PROMOTION_COUPON_NAV,
                    'title': u'优惠券',
                    'url': '/mall2/coupon_rule_list/',
                    'permission': 'manage_coupon'
                },
                {
                    'name': MALL_PROMOTION_ISSUING_COUPONS_NAV,
                    'title': u'发优惠券',
                    'url': '/mall2/issuing_coupons_record_list/',
                    'permission': 'manage_send_coupon'
                },
                # {
                #     'name': MALL_PROMOTION_ORDER_RED_ENVELOPE,
                #     'title': u'分享红包',
                #     'url': '/mall2/red_envelope_rule_list/',
                #     'permission': ['manage_order_red_envelope', ]
                # }
                {
                    'name': MALL_PROMOTION_FORBIDDEN_COUPON_PRODUCT_NAV,
                    'title': u'禁用优惠券商品',
                    'url': '/mall2/forbidden_coupon_product/',
                    'permission': 'forbidden_coupon_product'
                },
                {
                    'name': MALL_PROMOTION_CARD_EXCHANGE_NAV,
                    'title': u'微众卡兑换平台',
                    'url': '/mall2/card_exchange/',
                    'users': ['jobs', 'njtest', 'ceshi01', 'fulilaile'],
                    'permission': ''
                }
            ]
        },
        {
            'name': MALL_APPS_SECOND_NAV,
            'title': u'百宝箱',
            'url': '/apps/lottery/lotteries/',
            'permission': 'manage_apps',
            'third_navs': [
                {
                    'name': MALL_APPS_LOTTERY_NAV,
                    'title': "微信抽奖",
                    'url': '/apps/lottery/lotteries/',
                    'permission': ''
                },
                # {
                    # 'name': MALL_APPS_FEEDBACK_NAV,
                    # 'title': "用户反馈",
                    # 'url': '/apps/feedback/feedbacks/',
                    # 'permission': []
                # },
                 {
                    'name': MALL_APPS_SURVEY_NAV,
                    'title': "用户调研",
                    'url': '/apps/survey/surveies/',
                    'permission': ''
                },
                {
                    'name': MALL_APPS_EVENT_NAV,
                    'title': "活动报名",
                    'url': '/apps/event/events/',
                    'permission': []
                },
                {
                    'name': MALL_APPS_VOTE_NAV,
                    'title': "微信投票",
                    'url': '/apps/vote/votes/',
                    'permission': ''
                },
                {
                    'name': MALL_APPS_RED_ENVELOPE_NAV,
                    'title': u'分享红包',
                    'url': '/apps/red_envelope/red_envelope_rule_list/',
                    'permission': ''
                },
                {
                    'name': MALL_APPS_SIGN_NAV,
                    'title': u'签到',
                    'url': '/apps/sign/sign/',
                    'permission': ''
                },
                {
                    'name': MALL_APPS_POWERME_NAV,
                    'title': u'微助力',
                    'url': '/apps/powerme/powermes/',
                    'permission': ''
                },
                {
                    'name': MALL_APPS_FEEDBACK_NAV,
                    'title': u'用户反馈',
                    'url': '/apps/exsurvey/exsurveies/',
                    'permission': '',
                    'users': ['jobs','njtest','ceshi01', 'wzjx001', 'weizoomxs', 'weizoommm', 'weshop', 'weizoomclub', 'weizoomshop'] #这些帐号可以显示用户反馈
                },{
                    'name': MALL_APPS_GROUP_NAV,
                    'title': u'团购',
                    'url': '/apps/group/groups/',
                    'permission': '',
                },{
                    'name': MALL_APPS_SHVOTE_NAV,
                    'title': u'高级投票',
                    'url': '/apps/shvote/shvotes/',
                    'permission': '',
                    'users': ['jobs','jierunda', 'ceshi01']
                },{
                    'name': MALL_APPS_REBATE_NAV,
                    'title': u'返利活动',
                    'url': '/apps/rebate/rebates/',
                    'permission': '',
                },
                # {
                #     'name': MALL_APPS_REDPACKET_NAV,
                #     'title': u'拼红包',
                #     'url': '/apps/red_packet/red_packets/',
                #     'permission': ''
                # }
            ]
        }
    ]

}

########################################################################
# get_promotion_and_apps_second_navs: 获得应用和营销的二级导航
########################################################################
def get_promotion_and_apps_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        second_navs = [MALL_PROMOTION_AND_APPS_SECOND_NAV]

    return second_navs


# MALL_CONFIG_FIRST_NAV = 'config'
MALL_CONFIG_PAYINTERFACE_NAV = 'payInterfaces'
MALL_CONFIG_POSTAGE_NAV = 'postageManagement'
MALL_CONFIG_EXPRESS_COMOANY_NAV = 'expressManagement'
MALL_CONFIG_MAIL_NOTIFY_NAV = 'emailNotify'
MAIL_CONFIG_SUPPLIER_NAV = 'supplier'
MAIL_CONFIG_WEIXIN_NAV = 'wxCertificate'



CONFIG_NAV = {
    'navs': [
        # 商品管理
        {
            'name': MALL_CONFIG_POSTAGE_NAV,
            'title': u'运费模板',
            'url': '/mall2/postage_list/',
            'permission': 'manage_postage_template'
        },
        {
            'name': MALL_CONFIG_EXPRESS_COMOANY_NAV,
            'title': u'物流名称管理',
            'url': '/mall2/express_delivery_list/',
            'permission': 'manage_express'
        },
        {
            'name': MALL_CONFIG_PAYINTERFACE_NAV,
            'title': u'支付方式',
            'url': '/mall2/pay_interface_list/',
            'permission': 'manage_pay_interface'
        },
        {
            'name': MALL_CONFIG_MAIL_NOTIFY_NAV,
            'title': u'运营邮件通知',
            'url': '/mall2/email_notify_list/',
            'permission': 'manage_config_mail'
        },
        {
            'name': MAIL_CONFIG_SUPPLIER_NAV,
            'title': u'供货商',
            'url': '/mall2/supplier_list/',
            'permission': 'manage_supplier'
        },
    ]
}

########################################################################
# get_config_second_navs: 获得配置管理的二级导航
########################################################################
def get_config_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        if request.user_profile.webapp_type:
            second_navs = [CONFIG_NAV]
        else:
            nav = {"navs":CONFIG_NAV['navs'][:-1]}
            second_navs = [nav]

    return second_navs
