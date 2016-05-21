# -*- coding: utf-8 -*-
# __author__: zwidny 整理
import random
from datetime import datetime
from django.db.models import F, Q

from . import models as promotion_models
from mall import models
from core import search_util
from apps.customerized_apps.group import models as group_models

def get_coupon_rules(owner):
    """
    获取优惠券列表
    多个营销工具使用
    """
    rules = list(promotion_models.CouponRule.objects.filter(
                                    owner=owner,
                                    is_active=True,
                                    end_date__gt=datetime.now()
                                    ).order_by('-id'))
    return rules


def consume_coupon(owner_id, rule_id, member_id, coupon_record_id=0):
    """
    领用优惠券
    """
    rules = promotion_models.CouponRule.objects.filter(
                                                       id=rule_id,
                                                       owner_id=owner_id)
    if len(rules) != 1:
        return None, u'该优惠券使用期已过，不能领取！'
    coupon_count = promotion_models.Coupon.objects.filter(
                                            coupon_rule_id=rule_id,
                                            member_id=member_id).count()

    if coupon_count >= rules[0].limit_counts and rules[0].limit_counts > 0:
        return None, u'该优惠券每人限领%s张，你已经领取过了！' % rules[0].limit_counts

    coupons = promotion_models.Coupon.objects.filter(
                        coupon_rule_id=rule_id,
                        member_id=0,
                        status=promotion_models.COUPON_STATUS_UNGOT)[:1]

    if len(coupons) == 1:

        promotion_models.Coupon.objects.filter(id=coupons[0].id).update(
                status=promotion_models.COUPON_STATUS_UNUSED,
                member_id=member_id,
                provided_time=datetime.today(),
                coupon_record_id=coupon_record_id
            )
        if coupon_count:
            rules.update(remained_count=F('remained_count')-1,
                         get_count=F('get_count')+1)
        else:
            rules.update(remained_count=F('remained_count')-1,
                         get_person_count=F('get_person_count')+1,
                         get_count=F('get_count')+1)
        return coupons[0], ''
    else:
        return None, u'该优惠券使用期已过，不能领取！'


def award_coupon_for_member(coupon_rule_info, member):
    """
    给会员发奖
    """
    rule = promotion_models.CouponRule.objects.get(id=coupon_rule_info.id)
    consume_coupon(rule.owner, rule.id, member.id)


def coupon_id_maker(a, b):
    random_args_value = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return '%03d%04d%s' % (a, b, ''.join(random.sample(random_args_value, 6)))



def create_coupons(couponRule, count, promotion=None):
    """
    创建未使用的优惠券
    """
    i = 0
    if not promotion:
        promotion = promotion_models.Promotion.objects.filter(type=promotion_models.PROMOTION_TYPE_COUPON, detail_id=couponRule.id)[0]

    a = couponRule.owner.id
    b = couponRule.id

    # 创建未使用的优惠券
    current_coupon_ids = [coupon.coupon_id for coupon in promotion_models.Coupon.objects.filter(coupon_rule_id=b)]
    new_coupons = []
    while i < count:
        # 生成优惠券ID
        coupon_id = coupon_id_maker(a, b)
        while coupon_id in current_coupon_ids:
            coupon_id = coupon_id_maker(a, b)
        current_coupon_ids.append(coupon_id)
        new_coupons.append(promotion_models.Coupon(
                owner=couponRule.owner,
                coupon_id=coupon_id,
                #provided_time=promotion.start_date,
                start_time=promotion.start_date,
                expired_time=promotion.end_date,
                money=couponRule.money,
                coupon_rule_id=couponRule.id,
                is_manual_generated=False,
                status=promotion_models.COUPON_STATUS_UNGOT
        ))
        i += 1
    promotion_models.Coupon.objects.bulk_create(new_coupons)


PROMOTION_FILTERS = {
    'promotion': [
        {
            'comparator': lambda promotion, filter_value: (filter_value == 'all') or (promotion_models.PROMOTION2TYPE[promotion.type]['name'] == filter_value),
            'query_string_field': 'promotionType'
        }, {
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.status),
            'query_string_field': 'promotionStatus'
        }, {
            'comparator': lambda promotion, filter_value: filter_value <= promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda promotion, filter_value: filter_value >= promotion.end_date.strftime("%Y-%m-%d %H:%M") or filter_value == '',
            'query_string_field': 'endDate'
        }
    ],
    'coupon': [{
            'comparator': lambda promotion, filter_value: filter_value in promotion.name,
            'query_string_field': 'name'
        }, {
            'comparator': lambda promotion, filter_value: filter_value in promotion.name,
            'query_string_field': 'coupon_type'
        }, {
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.status),
            'query_string_field': 'promotionStatus'
        }, {
            'comparator': lambda promotion, filter_value: filter_value <= promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda promotion, filter_value: filter_value >= promotion.end_date.strftime("%Y-%m-%d %H:%M") or filter_value == '',
            'query_string_field': 'endDate'
        }
    ],
    'product': [{
            'comparator': lambda product, filter_value: filter_value in product.name,
            'query_string_field': 'name'
        }, {
            'comparator': lambda product, filter_value: filter_value == product.bar_code,
            'query_string_field': 'barCode',
        }
    ],
}


def filter_promotions(request, promotions):
    has_filter = search_util.init_filters(request, PROMOTION_FILTERS)
    if not has_filter:
        # 没有filter，直接返回
        return promotions

    filtered_promotions = []
    if request.GET.get('type', 'all') == 'coupon':
        promotions = search_util.filter_objects(
            promotions, PROMOTION_FILTERS['coupon']
        )
        coupon_type = request.GET.get('couponPromotionType', '-1')
        if coupon_type != '-1':
            coupon_type = coupon_type == '2'
            promotion_models.Promotion.fill_details(
                request.manager,
                promotions,
                {'with_concrete_promotion': True})
            promotions = [promotion for promotion in promotions if promotion.detail['limit_product'] == coupon_type]
        return promotions
        #过滤promotion集合
    promotions = search_util.filter_objects(
        promotions, PROMOTION_FILTERS['promotion']
    )
    promotion_models.Promotion.fill_details(
        request.manager,
        promotions,
        {'with_product': True})

    if not promotions:
        return filtered_promotions

    for promotion in promotions:
        products = search_util.filter_objects(
            promotion.products, PROMOTION_FILTERS['product']
        )
        if products:
            filtered_promotions.append(promotion)
    return filtered_promotions


# def stop_promotion(request, product_ids, shelve_type):
#     """
#     结束促销活动
#     """
#     promotionIds =[relation.promotion_id for relation in promotion_models.ProductHasPromotion.objects.filter(
#         product_id__in=product_ids)]
#     promotions = promotion_models.Promotion.objects.filter(id__in=promotionIds).filter(~Q(status = promotion_models.PROMOTION_STATUS_DELETED))
#     if not promotions.count():
#         return
#     # need_stop_coupon_rule = False
#     # for promotion in promotions:
#     #
#     #     coupon_rule = promotion_models.CouponRule.objects.get(id=promotion.detail_id)
#     #     coupon_rule_phps = promotion_models.ProductHasPromotion.objects.filter(promotion=promotion)
#     #     coupon_rule_product_ids = [php.product_id for php in coupon_rule_phps]
#     #
#     #     deleting_product_ids_in_coupon_rule = list(set(coupon_rule_product_ids) & set(product_ids))
#     #     del
#
#     for promotion in promotions:
#         if promotion.type == promotion_models.PROMOTION_TYPE_COUPON and shelve_type == 'delete':
#             # 处理优惠券相关状态
#
#             not_deleted_promotion_product_count = promotion_models.ProductHasPromotion.objects.filter(
#                 promotion=promotion,
#                 product__is_deleted=False).count()
#             if not_deleted_promotion_product_count == 0:
#                 ruleIds = [i.detail_id for i in promotion_models.Promotion.objects.filter(
#                     owner=request.manager,
#                     id=promotion.id)
#                 ]
#                 promotion_models.CouponRule.objects.filter(
#                     owner=request.manager,
#                     id__in=ruleIds
#                 ).update(is_active=False, remained_count=0)
#
#                 promotion_models.Coupon.objects.filter(
#                     owner=request.manager,
#                     coupon_rule_id__in=ruleIds,
#                     status=promotion_models.COUPON_STATUS_UNGOT
#                 ).update(status=promotion_models.COUPON_STATUS_Expired)
#                 promotion.status = promotion_models.PROMOTION_STATUS_FINISHED
#                 promotion.save()
#         elif promotion.type == promotion_models.PROMOTION_TYPE_COUPON:
#             pass
#         else:
#             promotion.status = promotion_models.PROMOTION_STATUS_FINISHED
#             promotion.save()
#
#     #发送finish_promotion event
#     from webapp.handlers import event_handler_util
#     event_data = {
#        "id": ','.join([str(promotion.id)]),
#        "type": promotion.type
#     }
#     event_handler_util.handle(event_data, 'finish_promotion')


# def get_usable_promotion_product_ids(webapp_owner, filter_type='coupon'):
#     products = models.Product.objects.filter(
#         owner=webapp_owner,
#         shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
#         is_deleted=False)
#
#     id2product = {}
#     from cache import webapp_cache
#
#     forbidden_coupon_product_ids = webapp_cache.get_forbidden_coupon_product_ids(webapp_owner.id)
#     for product in products:
#         has_forbidden_coupon = False
#         if product.id in forbidden_coupon_product_ids:
#             has_forbidden_coupon = True
#         data = product.format_to_dict()
#         data['can_select'] = True
#         # add by duhao 20150908
#         data['has_forbidden_coupon'] = has_forbidden_coupon
#         id2product[product.id] = data
#
#     # 获得已经与promotion关联的product
#     status_set = [
#         promotion_models.PROMOTION_STATUS_NOT_START,
#         promotion_models.PROMOTION_STATUS_STARTED,
#         promotion_models.PROMOTION_STATUS_DISABLE,  # 手动失效的单品优惠券要等到过期后才能创建买赠或限时抢购 duhao 2015-08-18
#     ]
#
#     if filter_type == 'integral_sale':
#         promotions = promotion_models.Promotion.objects.filter(
#             owner=webapp_owner,
#             type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE,
#             status__in=status_set)
#     else:
#         promotions = promotion_models.Promotion.objects.filter(
#             Q(owner=webapp_owner) &
#             ~Q(type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE) &
#             Q(status__in=status_set))
#
#     id2promotion = {}
#     promotion_ids = []
#     for promotion in promotions:
#         # 手动失效的单品优惠券要等到过期后才能创建买赠或限时抢购
#         if promotion.status == promotion_models.PROMOTION_STATUS_DISABLE:
#             now = datetime.now()
#             if now > promotion.end_date:
#                 continue
#
#         id2promotion[promotion.id] = promotion
#         promotion_ids.append(promotion.id)
#
#         php = promotion_models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)
#         for relation in php:
#             product_id = relation.product_id
#             product_data = id2product.get(product_id, None)
#             if not product_data:
#                 continue
#             promotion = id2promotion.get(relation.promotion_id, None)
#             if promotion:
#                 # 单品券是否可选更具促销名，弹窗模板使用mall_select_coupon_product_dialog
#                 if promotion.type == promotion_models.PROMOTION_TYPE_COUPON:
#                     product_data['promotion_name'] = u'多商品券'
#                 else:
#                     product_data['promotion_name'] = promotion.name
#
#             # 避免禁用优惠券商品列表里面收到促销活动的影响 duhao 20150908
#             if not filter_type == 'forbidden_coupon':
#                 product_data['can_select'] = False
#         # 过滤参团的商品
#         group_records = group_models.Group.objects(owner_id=webapp_owner.id, status__lte=1)
#         product_id2record = dict([(record.product_id, record) for record in group_records])
#         group_product_ids = [record.product_id for record in group_records]
#         for product_id in group_product_ids:
#             product_data = id2product.get(product_id, None)
#             if not product_data:
#                 continue
#             record = product_id2record.get(product_id, None)
#             if record:
#                 product_data['promotion_name'] = record.name
#
#         # 过滤下单位置为供货商的商品
#         buy_in_supplier_products = models.Product.objects.filter(owner=webapp_owner, buy_in_supplier=True)
#         buy_in_supplier_product_ids = [product.id for product in buy_in_supplier_products]
#         for product_id in buy_in_supplier_product_ids:
#             if id2product.has_key(product_id):
#                 id2product.pop(product_id)
#
#         if filter_type == 'coupon':
#             promotion_product_ids = filter(lambda k,v:)


def verification_multi_product_promotion(webapp_owner, product_ids, promotion_type):
    """
    创建多商品活动时的检测
    @param webapp_owner:
    @param product_ids: 要检测的商品id列表
    @param promotion_type:接受'integral_sale','coupon'
    @return:BOOL, error_product_ids错误商品id列表
    """
    all_error_product_ids = []
    # 检测商品拥有者、删除、下架、
    products = models.Product.objects.filter(
            owner=webapp_owner,
            shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
            is_deleted=False,
            buy_in_supplier=False,
            id__in=product_ids
    )

    usable_product_ids = [p.id for p in products]

    not_on_shelve_error_product_ids = list(set(product_ids).difference(set(usable_product_ids)))  # b中有而a中没有的

    all_error_product_ids.extend(not_on_shelve_error_product_ids)

    # 检测活动互斥,状态为“未开始”和“进行中”的活动属于检测互斥范围
    error_products = promotion_models.ProductHasPromotion.objects.filter(product_id__in=usable_product_ids,
                                                                         promotion__status__in=[
                                                                             promotion_models.PROMOTION_STATUS_NOT_START,
                                                                             promotion_models.PROMOTION_STATUS_STARTED])

    if promotion_type == 'coupon':
        # 多品券不和多品券、积分应用互斥
        error_products = error_products.exclude(promotion__type=promotion_models.PROMOTION_TYPE_COUPON).exclude(promotion__type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE)
    elif promotion_type == 'integral_sale':
        # 创建积分应用只和积分应用本身互斥
        error_products = error_products.filter(promotion__type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE)
    else:
        error_products = []

    all_error_product_ids.extend([p.product_id for p in error_products])

    # 检测团购
    group_records = group_models.Group.objects(owner_id=webapp_owner.id, status__lte=1)
    group_product_ids = [record.product_id for record in group_records]

    group_error_product_ids = list(set(product_ids).intersection(set(group_product_ids)))

    all_error_product_ids.extend(group_error_product_ids)

    return len(all_error_product_ids) == 0, all_error_product_ids


def string_ids2int_ids(string_ids, need_sorted=True):
    """
    @param string_ids:
    @param need_sorted:
    @return:
    """
    int_ids = list(set(map(lambda x: int(x), string_ids.split(','))))
    if need_sorted:
        int_ids = sorted(int_ids)

    return int_ids

