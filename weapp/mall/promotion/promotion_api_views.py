# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.decorators import login_required

from core import paginator
from models import *
from mall import models as mall_models
from core.restful_url_route import *
from core.jsonresponse import create_response
from core import search_util


COUNT_PER_PAGE = 10


PROMOTION_FILTERS = {
    'promotion': [{
            'comparator': lambda promotion, filter_value: (filter_value == 'all') or (PROMOTION2TYPE[promotion.type]['name'] == filter_value),
            'query_string_field': 'promotionType'
        }, {
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.status),
            'query_string_field': 'promotionStatus'
        }, {
            'comparator': lambda promotion, filter_value: filter_value <= promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda promotion, filter_value: filter_value >= promotion.end_date.strftime("%Y-%m-%d %H:%M"),
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
            'comparator': lambda promotion, filter_value: filter_value <= promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda promotion, filter_value: filter_value >= promotion.end_date.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'endDate'
        }
    ],
    'product': [{
            'comparator': lambda product, filter_value: filter_value in product.name,
            'query_string_field': 'name'
        },{
            'comparator': lambda product, filter_value: filter_value == product.bar_code,
            'query_string_field': 'barCode',
        }
    ],
}


def __filter_promotions(request, promotions):
    has_filter = search_util.init_filters(request, PROMOTION_FILTERS)
    if not has_filter:
        #没有filter，直接返回
        return promotions

    filtered_promotions = []
    if request.GET.get('type', 'all') == 'coupon':
        promotions = search_util.filter_objects(promotions, PROMOTION_FILTERS['coupon'])
        coupon_type = request.GET.get('couponPromotionType', None)
        if coupon_type != '-1':
            coupon_type = coupon_type == '2'
            Promotion.fill_details(request.manager, promotions, {
                'with_concrete_promotion': True
            })
            promotions = [promotion for promotion in promotions if promotion.detail['limit_product'] == coupon_type]
        return promotions
        #过滤promotion集合
    promotions = search_util.filter_objects(promotions, PROMOTION_FILTERS['promotion'])
    Promotion.fill_details(request.manager, promotions, {
        'with_product': True
    })

    if not promotions:
        return filtered_promotions

    for promotion in promotions:
        products = search_util.filter_objects(promotion.products, PROMOTION_FILTERS['product'])
        if not products:
            #product filter没有通过，跳过该promotion
            print 'end in product filter'
            continue
        else:
            print 'pass product filter'
            filtered_promotions.append(promotion)

#         filtered_products = []
#         for product in products:
#             models = search_util.filter_objects(product.models, PROMOTION_FILTERS['model'])
#             if models:
#                 print 'pass model filter'
#                 filtered_products.append(product)
#             else:
#                 print 'end in model filter'
#
#         if filtered_products:
#             #promotion有通过了product filter和model filter的商品，将promotion放入结果
#             filtered_promotions.append(promotion)
#         else:
#             pass
    return filtered_promotions


@api(app='mall_promotion', resource='promotions', action='get')
@login_required
def get_promotions(request):
    """
    获得促销活动集合
    """
    name = request.GET.get('name', '')
    bar_code = request.GET.get('barCode', '')
    promotion_status = int(request.GET.get('promotionStatus', -1))
    start_date = request.GET.get('startDate', '')
    end_date = request.GET.get('endDate', '')
    type_str = request.GET.get('type', 'all')
    coupon_id = request.GET.get('couponId','')
    promotion_type = PROMOTIONSTR2TYPE[type_str]

    is_fetch_all_promotions = (not name) and (not bar_code) and (not start_date) and (not end_date) and (not coupon_id) and (promotion_status == -1) and (promotion_type == 'all')
    if is_fetch_all_promotions:
        #获取promotion列表
        if promotion_type == PROMOTION_TYPE_ALL:
            # 全部类型不查询优惠券数据
            promotions = [promotion for promotion in list(Promotion.objects.filter(owner=request.manager)) if promotion.status != PROMOTION_STATUS_DELETED and promotion.type != PROMOTION_TYPE_COUPON]
        else:
            promotions = [promotion for promotion in list(Promotion.objects.filter(owner=request.manager, type=promotion_type)) if promotion.status != PROMOTION_STATUS_DELETED]
        promotions.sort(lambda x,y: cmp(y.id, x.id))

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, promotions = paginator.paginate(promotions, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
        #id2promotion = dict([(promotion.id, promotion) for promotion in promotions])
        Promotion.fill_details(request.manager, promotions, {
            'with_product': True,
            'with_concrete_promotion': True
        })
    else:
        #获得promotion集合并过滤
        if promotion_type == PROMOTION_TYPE_ALL:
            # 全部类型不查询优惠券数据
            promotions = [promotion for promotion in list(Promotion.objects.filter(owner=request.manager).order_by('-id')) if promotion.status != PROMOTION_STATUS_DELETED and promotion.type != PROMOTION_TYPE_COUPON]
        else:
            promotions = [promotion for promotion in list(Promotion.objects.filter(owner=request.manager, type=promotion_type).order_by('-id')) if promotion.status != PROMOTION_STATUS_DELETED]
        # if promotion_type != PROMOTION_TYPE_COUPON:
        promotions = __filter_promotions(request, promotions)

        #
        if coupon_id:
            coupon_rule_id2promotion = dict([(promotion.detail_id, promotion) for promotion in promotions])
            coupon = Coupon.objects.filter(coupon_id=coupon_id)
            if coupon.count() > 0:
                promotions = [coupon_rule_id2promotion[coupon[0].coupon_rule_id]]
            else:
                promotions = []

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, promotions = paginator.paginate(promotions, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
        Promotion.fill_details(request.manager, promotions, {
            'with_product': True,
            'with_concrete_promotion': True
        })

    #获取返回数据
    promotions.sort(lambda x,y: cmp(y.id, x.id))
    items = []
    for promotion in promotions:
        if promotion.detail.has_key('money'):
            promotion.detail['money'] = str(promotion.detail['money'])
        data = {
            "id": promotion.id,
            "status": promotion.status_name,
            "name": promotion.name,
            "promotionTitle": promotion.promotion_title,
            "type": PROMOTION2TYPE[promotion.type],
            "start_date": promotion.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": promotion.end_date.strftime("%Y-%m-%d %H:%M"),
            "created_at": promotion.created_at.strftime("%Y-%m-%d"),
            "detail": promotion.detail,
            "products": []
        }
        if hasattr(promotion, 'products'):
            for product in promotion.products:
                data["products"].append({
                    'id': product.id,
                    'name': product.name,
                    'thumbnails_url': product.thumbnails_url,
                    'display_price': product.display_price,
                    'display_price_range': product.display_price_range,
                    'bar_code': product.bar_code,
                    'stocks': product.stocks,
                    'sales': product.sales,
                    'is_use_custom_model': product.is_use_custom_model,
                    'models': product.models[1:],
                    'standard_model': product.standard_model,
                    'current_used_model': product.current_used_model,
                    'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M'),
                    "detail_link": '/mall/product/update/?id=%d&source=onshelf' % product.id
                })

            if len(data['products']) == 1:
                data['product'] = data['products'][0]
            else:
                data['product'] = []
        items.append(data)


    data = {
        "items": items,
        'pageinfo': paginator.to_dict(pageinfo),
        'sortAttr': 'id',
        'data': {}
    }
    response = create_response(200)
    response.data = data
    return response.get_response()


@api(app='mall_promotion', resource='usable_promotion_products', action='get')
@login_required
def get_usable_promotion_products(request):
    """
    获得促销活动可以选用的商品集合
    """
    name = request.GET.get("name", "")
    barCode = request.GET.get("barCode", "")
    filter_type = request.GET.get('filter_type', "all")
    selectedProductIds = request.GET.get("selectedProductIds", "").split('_')
    products = mall_models.Product.objects.filter(owner=request.manager, shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON, is_deleted=False)
    if name:
        products = products.filter(name__contains=name)
    if barCode:
        products = products.filter(bar_code=barCode)

    #进行分页
    count_per_page = int(request.GET.get('count_per_page', 10))
    cur_page = int(request.GET.get('page', '1'))
    pageinfo, products = paginator.paginate(products, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

    products = list(products)
    mall_models.Product.fill_details(request.manager, products, {
        "with_product_model": True,
        "with_model_property_info": True,
        'with_sales': True
    })
    id2product = {}
    for product in products:
        data = product.format_to_dict()
        data['can_select'] = True
        id2product[product.id] = data

    #获得已经与promotion关联的product
    if filter_type == 'all':
        promotions = list(Promotion.objects.exclude(type=PROMOTION_TYPE_INTEGRAL_SALE).filter(owner=request.manager, status__in=[PROMOTION_STATUS_NOT_START, PROMOTION_STATUS_STARTED]))
    elif filter_type == 'integral_sale':
        promotions = list(Promotion.objects.filter(owner=request.manager, type=PROMOTION_TYPE_INTEGRAL_SALE, status__in=[PROMOTION_STATUS_NOT_START, PROMOTION_STATUS_STARTED]))

    id2promotion = dict([(promotion.id, promotion) for promotion in promotions])
    promotion_ids = [promotion.id for promotion in promotions]
    for relation in ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids):
        product_id = relation.product_id
        product_data = id2product.get(product_id, None)
        if not product_data:
            continue
        promotion = id2promotion.get(relation.promotion_id, None)
        if promotion:
            product_data['promotion_name'] = promotion.name
        product_data['can_select'] = False

    # 将已选择的商品id改为 can_select 改为 False
    for product_id in selectedProductIds:
        try:
            product_data = id2product.get(int(product_id), None)
            if not product_data:
                continue
            product_data['can_select'] = False
        except:
            pass

    items = id2product.values()
    items.sort(lambda x,y: cmp(x['id'], y['id']))

    data = {
        "items": items,
        'pageinfo': paginator.to_dict(pageinfo),
        'sortAttr': 'id',
        'data': {}
    }
    response = create_response(200)
    response.data = data
    return response.get_response()


########################################################################
# get_promotion_products: 获得促销活动包括的商品详情
########################################################################
@api(app='mall_promotion', resource='promotion_products', action='get')
@login_required
def get_promotion_products(request):
    promotion_id = request.GET['id']
    promotion = Promotion.objects.get(id=promotion_id)
    Promotion.fill_details(request.manager, [promotion], {
        'with_product': True
    })

    data = []
    for product in promotion.products:
        data.append({
            "id": product.id,
            "name": product.name,
            "thumbnails_url": product.thumbnails_url,
            "bar_code": product.bar_code,
            "stocks": product.stocks,
            "sales": -1,
            "display_price": product.display_price,
            "display_price_range": product.display_price_range,
            "is_use_custom_model": product.is_use_custom_model,
            "current_used_model": product.current_used_model,
            "standard_model": product.standard_model,
            "models": product.models[1:]
        })

    response = create_response(200)
    response.data = data
    return response.get_response()


########################################################################
# finish_promotions: 结束促销活动
########################################################################
@api(app='mall_promotion', resource='promotions', action='finish')
@login_required
def finish_promotions(request):
    promotion_type = PROMOTIONSTR2TYPE[request.POST['type']]

    ids = request.POST.getlist('ids[]')
    start = request.POST.get('start', '')
    status = None
    if start == 'true':
        status = PROMOTION_STATUS_STARTED
    else:
        status = PROMOTION_STATUS_FINISHED
    Promotion.objects.filter(owner=request.manager, id__in=ids).update(status=status)
    if promotion_type == PROMOTION_TYPE_COUPON:
        ruleIds = [promotion.detail_id for promotion in Promotion.objects.filter(owner=request.manager, id__in=ids)]
        CouponRule.objects.filter(owner=request.manager, id__in=ruleIds).update(is_active=False, remained_count=0)
        Coupon.objects.filter(owner=request.manager, coupon_rule_id__in=ruleIds, status=COUPON_STATUS_UNGOT).update(status=COUPON_STATUS_Expired)

    if start == 'true':
        pass
    else:
        #发送finish_promotion event
        from webapp.handlers import event_handler_util
        event_data = {
           "id": ','.join(ids),
           "type": promotion_type
        }
        event_handler_util.handle(event_data, 'finish_promotion')

    response = create_response(200)
    return response.get_response()


########################################################################
# delete_promotion: 删除促销活动
########################################################################
@api(app='mall_promotion', resource='promotions', action='delete')
@login_required
def delete_promotions(request):
    promotion_type = PROMOTIONSTR2TYPE[request.POST['type']]
    ids = request.POST.getlist('ids[]')
    if promotion_type == PROMOTION_TYPE_ALL:
        Promotion.objects.filter(owner=request.manager, id__in=ids).update(status=PROMOTION_STATUS_DELETED)
    else:
        Promotion.objects.filter(owner=request.manager, type=promotion_type, id__in=ids).update(status=PROMOTION_STATUS_DELETED)

    response = create_response(200)
    return response.get_response()

