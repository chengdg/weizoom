# -*- coding: utf-8 -*-

PRODUCT_FIRST_NAV = 'product'
PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV = 'selling'
PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV = 'toSell'
PRODUCT_ADD_PRODUCT_NAV = 'addnew'
PRODUCT_MANAGE_RECYCLED_PRODUCT_NAV = 'recycleBin'
PRODUCT_MANAGE_IMAGE_NAV = 'pictureManagement'
PRODUCT_MANAGE_CATEGORY_NAV = 'groupManagement'
PRODUCT_MANAGE_MODEL_NAV = 'attrModelManagement'
PRODUCT_REVIEW_NAV = 'reviewManagement'

FIRST_NAVS = [{
    'name': u'首页',
    'url': '/mall/outline/get/',
    'permission': 'manage_index'
}, {
    'name': u'商品管理',
    'url': '/mall/onshelf_products/get/',
    'permission': 'manage_product'
}, {
    'name': u'订单管理',
    'url': '/mall/orders/get/',
    'permission': 'manage_order'
}, {
    'name': u'促销管理',
    'url': '/mall_promotion/promotion_list/get/',
    'permission': 'manage_promotion'
}, {
    'name': u'会员管理',
    'url': '/member/members/get/',
    'permission': 'manage_member'
}, {
    'name': u'数据罗盘',
    #'url': 'http://tj.weizzz.com/',
    'url': '/stats/manage_summary/',
    'permission': 'static'
}, {
    'name': u'权限管理',
    'url': '/auth/account_help/get/',
    'permission': 'manage_auth'
}, {
    'name': u'配置管理',
    'url': '/mall/pay_interfaces/get/',
    'permission': 'manage_mall_config'
}]

def get_first_navs(user):
    from auth.export import NAV as AUTH_NAV
    from member.export import MEMBER_NAV
    manage_index=HOME_NAV
    manage_product=NAV
    manage_order=ORDER_NAV
    manage_promotion=PROMOTION_NAV
    manage_member=CONFIG_NAV
    static={'navs':[]}
    manage_auth=MEMBER_NAV
    manage_mall_config=CONFIG_NAV

    first_navs_result = []
    for nav in FIRST_NAVS:
        if user.has_perm(nav['permission']):
            for s_nav in eval(nav['permission'])['navs']:
                if user.has_perm(s_nav['need_permissions']):
                    if not nav.get('children', None):
                        nav['children'] = []
                        nav['url'] = s_nav['url']
                    nav['children'].append(s_nav)
            first_navs_result.append(nav)

    return first_navs_result

NAV = {
    'section': u'微信商城',
    'navs': [
        # 商品管理
        {
            'name': PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV,
            'title': u'在售商品管理',
            'url': '/mall/onshelf_products/get/',
            'need_permissions': ['manage_product_onshelf', ]
        },

        {
            'name': PRODUCT_ADD_PRODUCT_NAV,
            'title': u'添加新商品',
            'url': '/mall/product/create/',
            'need_permissions': ['manage_product_add', ]
        },
        {
            'name': PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV,
            'title': u'待售商品管理',
            'url': '/mall/offshelf_products/get/',
            'need_permissions': ['manage_product_offshelf', ]
        },
        {
            'name': PRODUCT_MANAGE_RECYCLED_PRODUCT_NAV,
            'title': u'商品回收站',
            'url': '/mall/recycled_products/get/',
            'need_permissions': ['manage_product_deleted', ]
        },
        {
            'name': PRODUCT_MANAGE_IMAGE_NAV,
            'title': u'图片管理',
            'url': '/mall/image_groups/get/',
            'need_permissions': ['manage_product_image', ]
        },
        {
            'name': PRODUCT_MANAGE_CATEGORY_NAV,
            'title': u'分组管理',
            'url': '/mall/product_categories/get/',
            'need_permissions': ['manage_product_category', ]
        },
        {
            'name': PRODUCT_MANAGE_MODEL_NAV,
            'title': u'属性规格管理',
            'url': '/mall/model_properties/get/',
            'need_permissions': ['manage_product_property_and_model_property', ]
        },
        {
            'name': PRODUCT_REVIEW_NAV,
            'title': u'评价管理',
            'url': '/mall/product_review/get/',
            'need_permissions': ['manage_product_review', ],
        },
    ]
}

########################################################################
# get_second_navs: 获得二级导航
########################################################################


def get_second_navs(request):
    if request.user.username == 'manager':
        second_navs = [NAV]
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [NAV]

    return second_navs
get_product_second_navs = get_second_navs


ORDER_FIRST_NAV = 'order'
ORDER_ALL = 'allOrder'
ORDER_REFUND = 'refundOrder'
ORDER_AUDIT = 'financialCheck'
ORDER_EXPIRED_TIME = 'orderExpiration'
ORDER_BATCH_DELIVERY = 'orderBatchDelivery'

ORDER_NAV = {
    'section': u'',
    'navs': [
        # 商品管理
        {
            'name': ORDER_ALL,
            'title': u'所有订单',
            'url': '/mall/orders/get/',
            'need_permissions': ['manage_order_all', ]
        },
        {
            'name': ORDER_REFUND,
            'title': u'退款订单',
            'url': '/mall/refund_orders/get/',
            'need_permissions': ['manage_order_refund', ]
        },
        {
            'name': ORDER_EXPIRED_TIME,
            'title': u'订单设置',
            'url': '/mall/expired_time/edit/',
            'need_permissions': ['manage_order_expired_time', ]
        },
        {
            'name': ORDER_AUDIT,
            'title': u'财务审核',
            'url': '/mall/audit_orders/get/',
            'need_permissions': ['manage_order_audit', ]
        },
        {
            'name': ORDER_BATCH_DELIVERY,
            'title': u'批量发货',
            'url': 'javascript:void(0);',
            'need_permissions': ['manage_order_batch_delivery', ]
        },
        {
            'name': ORDER_RED_ENVELOPE,
            'title': u'分享红包',
            'url': '/mall/red_envelope_rule/get/',
            'need_permissions': ['manage_order_red_envelope', ]
        }
    ]
}


def get_orders_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [ORDER_NAV]

    return second_navs


MALL_PROMOTION_FIRST_NAV = 'promotion'
MALL_PROMOTION_PROMOTIONS_NAV = 'promotionQuery'
MALL_PROMOTION_FLASH_SALE_NAV = 'flashSale'
MALL_PROMOTION_PREMIUM_SALE_NAV = 'buyGifts'
MALL_PROMOTION_PRICE_CUT_NAV = 'fullReduction'
MALL_PROMOTION_COUPON_NAV = 'Coupon'
MALL_PROMOTION_INTEGRAL_SALE_NAV = 'integralYingyon'
MALL_PROMOTION_ISSUING_COUPONS_NAV = 'issuingCoupon'
ORDER_RED_ENVELOPE = 'orderRedEnvelope'


PROMOTION_NAV = {
    'navs': [
        # 商品管理
        {
            'name': MALL_PROMOTION_PROMOTIONS_NAV,
            'title': u'促销查询',
            'url': '/mall_promotion/promotion_list/get/',
            'need_permissions': ['search_promotion', ]
        },
        {
            'name': MALL_PROMOTION_FLASH_SALE_NAV,
            'title': u'限时抢购',
            'url': '/mall_promotion/flash_sales/get/',
            'need_permissions': ['manage_flash_sale', ]
        },
        {
            'name': MALL_PROMOTION_PREMIUM_SALE_NAV,
            'title': u'买赠',
            'url': '/mall_promotion/premium_sales/get/',
            'need_permissions': ['manage_premium_sale', ]
        },
        # {
        #     'name': MALL_PROMOTION_PRICE_CUT_NAV,
        #     'title': u'满减',
        #     'url': '/mall_promotion/price_cuts/get/',
        #     'need_permissions': ['manage_price_cut', ]
        # },
        {
            'name': MALL_PROMOTION_INTEGRAL_SALE_NAV,
            'title': u'积分应用',
            'url': '/mall_promotion/integral_sales/get/',
            'need_permissions': ['manage_integral_sale', ]
        },
        {
            'name': MALL_PROMOTION_COUPON_NAV,
            'title': u'优惠券',
            'url': '/mall_promotion/coupon_rules/get/',
            'need_permissions': ['manage_coupon', ]
        },
        {
            'name': MALL_PROMOTION_ISSUING_COUPONS_NAV,
            'title': u'发优惠券',
            'url': '/mall_promotion/issuing_coupons_record/get/',
            'need_permissions': ['manage_send_coupon', ]
        },
        # {
        #     'name': ORDER_RED_ENVELOPE,
        #     'title': u'分享红包',
        #     'url': '/mall/red_envelope_rule/get/',
        #     'need_permissions': ['manage_red_envelope', ]
        # }
    ]
}

########################################################################
# get_promotion_second_navs: 获得促销管理的二级导航
########################################################################


def get_promotion_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [PROMOTION_NAV]

    return second_navs


MALL_CONFIG_FIRST_NAV = 'config'
MALL_CONFIG_PAYINTERFACE_NAV = 'payInterfaces'
MALL_CONFIG_POSTAGE_NAV = 'postageManagement'
MALL_CONFIG_EXPRESS_COMOANY_NAV = 'expressManagement'
MALL_CONFIG_MAIL_NOTIFY_NAV = 'emailNotify'


CONFIG_NAV = {
    'navs': [
        # 商品管理
        {
            'name': MALL_CONFIG_POSTAGE_NAV,
            'title': u'运费模板',
            'url': '/mall/postage_templates/get/',
            'need_permissions': ['manage_postage_template', ]
        },
        {
            'name': MALL_CONFIG_EXPRESS_COMOANY_NAV,
            'title': u'物流名称管理',
            'url': '/mall/express_delivery/get/',
            'need_permissions': ['manage_express', ]
        },
        {
            'name': MALL_CONFIG_PAYINTERFACE_NAV,
            'title': u'支付方式',
            'url': '/mall/pay_interfaces/get/',
            'need_permissions': ['manage_pay_interface', ]
        },
        {
            'name': MALL_CONFIG_MAIL_NOTIFY_NAV,
            'title': u'运营邮件通知',
            'url': '/mall/email_notify/get/',
            'need_permissions': ['manage_config_mail', ]
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
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [CONFIG_NAV]

    return second_navs


MALL_HOME_FIRST_NAV = 'home'
MALL_HOME_OUTLINE_NAV = 'census'
MALL_HOME_INTEGRAL_NAV = 'integralRule'
MALL_HOME_NOTICES_NAV = 'notices'
MALL_HOME_WEPAGE_NAV = 'wepage'

HOME_NAV = {
    'section': u'商城首页',
    'navs': [  # 商品管理
        {
            'name': MALL_HOME_OUTLINE_NAV,
            'title': u'统计概况',
            'url': '/mall/outline/get/',
            'need_permissions': ['manage_index_outline', ]
        },
        {
            'name': MALL_HOME_INTEGRAL_NAV,
            'title': u'积分规则',
            'url': '/mall/integral_strategy/get/',
            'need_permissions': ['manage_index_integral', ]
        },
        {
            'name': MALL_HOME_NOTICES_NAV,
            'title': u'消息中心',
            'url': '/mall/notice_list/get',
            'need_permissions': ['manage_index_notice'],
        },
        {
            'name': MALL_HOME_WEPAGE_NAV,
            'title': u'店铺装修',
            'url': '/termite2/pages/',
            'need_permissions': ['manage_wepage'],
        }
    ]
}


def get_home_second_navs(request):
    """
    获取"商铺首页"部分的二级导航
    """
    if request.user.username == 'manager':
        second_navs = [HOME_NAV]
    else:
        second_navs = [HOME_NAV]

    return second_navs
